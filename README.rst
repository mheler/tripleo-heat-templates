========================
Team and repository tags
========================

.. image:: https://governance.openstack.org/tc/badges/tripleo-heat-templates.svg
    :target: https://governance.openstack.org/tc/reference/tags/index.html

.. Change things from this point on

======================
tripleo-heat-templates
======================

Heat templates to deploy OpenStack using OpenStack.

* Free software: Apache License (2.0)
* Documentation: https://docs.openstack.org/tripleo-docs/latest/
* Source: https://opendev.org/openstack/tripleo-heat-templates
* Bugs: https://bugs.launchpad.net/tripleo
* Release notes: https://docs.openstack.org/releasenotes/tripleo-heat-templates/

Features
--------

The ability to deploy a multi-node, role based OpenStack deployment using
OpenStack Heat. Notable features include:

 * Choice of deployment/configuration tooling: puppet, (soon) docker

 * Role based deployment: roles for the controller, compute, ceph, swift,
   and cinder storage

 * physical network configuration: support for isolated networks, bonding,
   and standard ctlplane networking

Directories
-----------

A description of the directory layout in TripleO Heat Templates.

 * environments: contains heat environment files that can be used with -e
                 on the command like to enable features, etc.

 * extraconfig: templates used to enable 'extra' functionality. Includes
                functionality for distro specific registration and upgrades.

 * firstboot: example first_boot scripts that can be used when initially
              creating instances.

 * network: heat templates to help create isolated networks and ports

 * puppet: templates mostly driven by configuration with puppet. To use these
           templates you can use the overcloud-resource-registry-puppet.yaml.

 * validation-scripts: validation scripts useful to all deployment
                       configurations

 * roles: example roles that can be used with the tripleoclient to generate
          a roles_data.yaml for a deployment See the
          `roles/README.rst <roles/README.rst>`_ for additional details.

Service testing matrix
----------------------

The configuration for the CI scenarios will be defined in `tripleo-heat-templates/ci/`
and should be executed according to the following table:

+----------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
|        -       | scn000 | scn001 | scn002 | scn003 | scn004 | scn006 | scn007 | scn009 | scn010 | scn013 | non-ha | ovh-ha |
+================+========+========+========+========+========+========+========+========+========+========+========+========+
| keystone       |    X   |    X   |    X   |    X   |    X   |    X   |    X   |        |    X   |    X   |    X   |    X   |
+----------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| glance         |        |  rbd   | swift  |  file  |   rgw  |   file |   file |        |   rbd  |   file |   file |   file |
+----------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| cinder         |        |  rbd   | iscsi  |        |        |        |        |        |        |        |        |        |
+----------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| heat           |        |    X   |    X   |        |        |        |        |        |        |        |        |        |
+----------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| ironic         |        |        |        |        |        |    X   |        |        |        |        |        |        |
+----------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| mysql          |   X    |    X   |    X   |    X   |    X   |    X   |    X   |        |    X   |    X   |    X   |    X   |
+----------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| neutron        |        |  ovn   |   ovn  |   ovn  |   ovn  |   ovn  |   ovs  |        |   ovn  |   ovn  |   ovn  |   ovn  |
+----------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| neutron-bgpvpn |        |        |        |        |   wip  |        |        |        |        |        |        |        |
+----------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| neutron-l2gw   |        |        |        |        |   wip  |        |        |        |        |        |        |        |
+----------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| om-rpc         |        | rabbit | rabbit |  amqp1 | rabbit | rabbit | rabbit |        | rabbit | rabbit | rabbit | rabbit |
+----------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| om-notify      |        | rabbit | rabbit | rabbit | rabbit | rabbit | rabbit |        | rabbit | rabbit | rabbit | rabbit |
+----------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| redis          |        |    X   |    X   |        |        |        |        |        |        |        |        |        |
+----------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| haproxy        |        |    X   |    X   |    X   |    X   |    X   |    X   |        |    X   |    X   |    X   |    X   |
+----------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| memcached      |        |    X   |    X   |    X   |    X   |    X   |    X   |        |    X   |    X   |    X   |    X   |
+----------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| pacemaker      |        |    X   |    X   |    X   |    X   |    X   |    X   |        |    X   |    X   |    X   |    X   |
+----------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| nova           |        |  qemu  |  qemu  |  qemu  |  qemu  | ironic |  qemu  |        |  qemu  |  qemu  |  qemu  |  qemu  |
+----------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| placement      |        |    X   |    X   |    X   |    X   |    X   |    X   |        |    X   |    X   |    X   |    X   |
+----------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| ntp            |   X    |    X   |    X   |    X   |    X   |    X   |    X   |    X   |    X   |    X   |    X   |    X   |
+----------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| snmp           |   X    |    X   |    X   |    X   |    X   |    X   |    X   |    X   |    X   |    X   |    X   |    X   |
+----------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| timezone       |   X    |    X   |    X   |    X   |    X   |    X   |    X   |    X   |    X   |    X   |    X   |    X   |
+----------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| swift          |        |        |    X   |        |        |        |        |        |        |        |        |        |
+----------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| aodh           |        |    X   |    X   |        |        |        |        |        |        |        |        |        |
+----------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| ceilometer     |        |    X   |    X   |        |        |        |        |        |        |        |        |        |
+----------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| gnocchi        |        |  rbd   |  swift |        |        |        |        |        |        |        |        |        |
+----------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| barbican       |        |        |    X   |        |        |        |        |        |        |        |        |        |
+----------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| cephrgw        |        |        |        |        |    X   |        |        |        |        |        |        |        |
+----------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| cephmds        |        |        |        |        |    X   |        |        |        |        |        |        |        |
+----------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| manila         |        |        |        |        |    X   |        |        |        |        |        |        |        |
+----------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| collectd       |        |    X   |        |        |        |        |        |        |        |        |        |        |
+----------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| designate      |        |        |        |    X   |        |        |        |        |        |        |        |        |
+----------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| octavia        |        |        |        |        |        |        |        |        |    X   |    X   |        |        |
+----------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| Extra Firewall |        |        |        |    X   |        |        |        |        |        |        |        |        |
+----------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
