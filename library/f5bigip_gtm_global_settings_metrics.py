#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2016 Eric Jacob <erjac77@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = """
---
module: f5bigip_gtm_global_settings_metrics
short_description: BIG-IP gtm global-settings metrics module
description:
    - Configures the metrics settings for the Global Traffic Manager.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Gabriel Fortin (@GabrielFortin)"
options:
    default_probe_limit:
        description:
            - Specifies the number of probe attempts that the system performs before removing the path from the metrics.
        default: 12
    hops_ttl:
        description:
            - Specifies the number of seconds that the system considers traceroute utility data to be valid for name
              resolution and load balancing.
        default: 604800
        choices: range(hops_timeout, infinity)
    hops_packet_length:
        description:
            - Specifies the length of packets, in bytes, that the system sends to a local DNS server to determine the
              path information between the two systems.
        default: 64
    hops_sample_count:
        description:
            - Specifies the number of packets that the system sends to a local DNS server to determine the path
              information between those two systems.
        default: 3
    hops_timeout:
        description:
            - Specifies the number of seconds that the big3d daemon waits for a probe.
        default: 3
    inactive_ldns_ttl:
        description:
            - Specifies the number of seconds that an inactive LDNS remains in the cache.
        default: 2419200
        choices: range(60, 4294967296)
    ldns_update_interval:
        description:
            - Specifies the number of seconds that a tmm will wait before sending an update for a LDNS which has been
              accessed.
        default: 20
    inactive_paths_ttl:
        description:
            - Specifies the number of seconds that a path remains in the cache after its last access.
        default: 604800
        choices: range(60, 4294967296)
    max_synchronous_monitor_requests:
        description:
            - Specifies how many monitors can attempt to verify the availability of a given resource at the same time.
        default: 20
    metrics_caching:
        description:
            - Specifies the interval (in seconds) at which the system dumps path and other metrics data.
        default: 3600
        choices: range(0, 604801)
    metrics_collection_protocols:
        description:
            - Specifies the protocols that the system uses to collect metrics information relevant to LDNS servers.
        choices: ['dns_dot', 'dns_rev', 'icmp', 'tcp', 'udp']
    path_ttl:
        description:
            - Specifies the number of seconds that the system considers path data to be valid for name resolution and
              load balancing purposes.
        default: 2400
        choices: range(paths_retry, infinity)
    paths_retry:
        description:
            - Specifies the interval (in seconds) at which the system retries the path data.
        default: 120
    port:
        description:
            - Specifies the port on which the listener listens for connections.
extends_documentation_fragment:
    - f5_common
"""

EXAMPLES = """
- name: Create GTM Global Settings Metrics
  f5bigip_gtm_global_settings_metrics:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    default_probe_limit: 10
  delegate_to: localhost
"""

RETURN = """ # """

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six.moves import range
from ansible.module_utils.erjac77.network.f5.common import F5_PROVIDER_ARGS
from ansible.module_utils.erjac77.network.f5.bigip import F5BigIpUnnamedObject


class ModuleParams(object):
    @property
    def argument_spec(self):
        argument_spec = dict(
            default_probe_limit=dict(type="int"),
            hops_ttl=dict(type="int"),
            hops_packet_length=dict(type="int"),
            hops_sample_count=dict(type="int"),
            hops_timeout=dict(type="int"),
            inactive_ldns_ttl=dict(type="int", choices=range(60, 4294967296)),
            ldns_update_interval=dict(type="int"),
            inactive_paths_ttl=dict(type="int", choices=range(60, 4294967296)),
            max_synchronous_monitor_requests=dict(type="int"),
            metrics_caching=dict(type="int", choices=range(0, 604801)),
            metrics_collection_protocols=dict(
                type="str", choices=["dns_dot", "dns_rev", "icmp", "tcp", "udp"]
            ),
            path_ttl=dict(type="int"),
            paths_retry=dict(type="int"),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpGtmGlobalSettingsMetrics(F5BigIpUnnamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "read": self._api.tm.gtm.global_settings.metrics.load,
            "update": self._api.tm.gtm.global_settings.metrics.update,
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpGtmGlobalSettingsMetrics(
            check_mode=module.check_mode, **module.params
        )
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
