#!/usr/bin/env python
#
# Copyright 2018 Red Hat Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import argparse
from configparser import ConfigParser
import logging
import logging.handlers
import os
import sys
import time


from keystoneauth1 import loading
from keystoneauth1 import session

from novaclient import client
from novaclient.exceptions import ClientException


config = ConfigParser(strict=False)

debug = os.getenv('__OS_DEBUG', 'false')

if debug.lower() == 'true':
    loglevel = logging.DEBUG
else:
    loglevel = logging.INFO

LOG = logging.getLogger('nova_wait_for_api_service')
LOG_FORMAT = ('%(asctime)s.%(msecs)03d %(levelname)s '
              '%(name)s %(message)s')
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
LOG.handlers.clear()
LOG.setLevel(loglevel)
LOG.propagate = True
formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT)
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)
LOG.addHandler(stream_handler)

iterations = 60
timeout = 10
nova_cfg = '/etc/nova/nova.conf'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='%(prog)s [options]')
    parser.add_argument('-k', '--insecure',
                        action="store_false",
                        dest='insecure',
                        default=True,
                        help='Allow insecure connection when using SSL')

    args = parser.parse_args()
    LOG.debug('Running with parameter insecure = %s',
              args.insecure)

    if os.path.isfile(nova_cfg):
        try:
            config.read(nova_cfg)
        except Exception:
            LOG.exception('Error while reading nova.conf:')
    else:
        LOG.error('Nova configuration file %s does not exist', nova_cfg)
        sys.exit(1)

    loader = loading.get_plugin_loader('password')
    auth = loader.load_from_options(
        auth_url=config.get('neutron',
                            'auth_url'),
        username=config.get('neutron',
                            'username'),
        password=config.get('neutron',
                            'password'),
        project_name=config.get('neutron',
                                'project_name'),
        project_domain_name=config.get('neutron',
                                       'project_domain_name'),
        user_domain_name=config.get('neutron',
                                    'user_domain_name'))
    sess = session.Session(auth=auth, verify=args.insecure)

    # Wait until this host is listed in the service list
    for i in range(iterations):
        try:
            nova = client.Client('2.11', session=sess, endpoint_type='internal')
            nova.versions.list()
            LOG.info('Nova-api service active')
            sys.exit(0)
        except ClientException:
            LOG.info('Waiting for nova-api service')
        except Exception:
            LOG.exception(
                'Error while waiting for nova-api service')
        time.sleep(timeout)
sys.exit(1)

# vim: set et ts=4 sw=4 :
