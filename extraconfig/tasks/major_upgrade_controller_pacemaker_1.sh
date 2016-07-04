#!/bin/bash

set -eu

cluster_sync_timeout=1800

if pcs status 2>&1 | grep -E '(cluster is not currently running)|(OFFLINE:)'; then
    echo_error "ERROR: upgrade cannot start with some cluster nodes being offline"
    exit 1
fi


# We want to disable fencing during the cluster --stop as it might fence
# nodes where a service fails to stop, which could be fatal during an upgrade
# procedure. So we remember the stonith state. If it was enabled we reenable it
# at the end of this script
STONITH_STATE=$(pcs property show stonith-enabled | grep "stonith-enabled" | awk '{ print $2 }')
pcs property set stonith-enabled=false

if [ "$(hiera -c /etc/puppet/hiera.yaml bootstrap_nodeid)" = "$(facter hostname)" ]; then
    pcs resource disable httpd
    check_resource httpd stopped 1800
    pcs resource disable openstack-core
    check_resource openstack-core stopped 1800
    pcs resource disable redis
    check_resource redis stopped 600
    pcs resource disable mongod
    check_resource mongod stopped 600
    pcs resource disable rabbitmq
    check_resource rabbitmq stopped 600
    pcs resource disable memcached
    check_resource memcached stopped 600
    pcs resource disable galera
    check_resource galera stopped 600
    # Disable all VIPs before stopping the cluster, so that pcs doesn't use one as a source address:
    #   https://bugzilla.redhat.com/show_bug.cgi?id=1330688
    for vip in $(pcs resource show | grep ocf::heartbeat:IPaddr2 | grep Started | awk '{ print $1 }'); do
      pcs resource disable $vip
      check_resource $vip stopped 60
    done
    pcs cluster stop --all
fi

# Swift isn't controled by pacemaker
systemctl_swift stop

tstart=$(date +%s)
while systemctl is-active pacemaker; do
    sleep 5
    tnow=$(date +%s)
    if (( tnow-tstart > cluster_sync_timeout )) ; then
        echo_error "ERROR: cluster shutdown timed out"
        exit 1
    fi
done

# install sahara and gnocchi packages
# https://bugs.launchpad.net/tripleo/+bug/1597674
yum -y install openstack-gnocchi-api openstack-gnocchi-indexer-sqlalchemy openstack-gnocchi-carbonara openstack-gnocchi-statsd openstack-gnocchi-metricd openstack-sahara openstack-sahara-api openstack-sahara-engine

yum -y install python-zaqarclient  # needed for os-collect-config
yum -y -q update


# Let's reset the stonith back to true if it was true, before starting the cluster
if [ $STONITH_STATE == "true" ]; then
    pcs -f /var/lib/pacemaker/cib/cib.xml property set stonith-enabled=true
fi

# Pin messages sent to compute nodes to kilo, these will be upgraded later
crudini  --set /etc/nova/nova.conf upgrade_levels compute "$upgrade_level_nova_compute"
# L->M upgrades moved the paste file from /usr/share/keystone to /etc/keystone. Keystone won't run without this
crudini --set /etc/keystone/keystone.conf paste_deploy config_file /etc/keystone/keystone-paste.ini
