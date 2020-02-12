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
module: f5bigip_gtm_pool
short_description: BIG-IP gtm pool module
description:
    - Configures load balancing pools for the Global Traffic Manager.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Eric Jacob (@erjac77)"
options:
    alternate_mode:
        description:
            - Specifies the load balancing mode that the system uses to load balance name resolution requests among the
              members of this pool, if the preferred method is unsuccessful in picking a pool.
        default: round-robin
        choices: [
            'drop-packet', 'fallback-ip', 'global-availability', 'none', 'packet-rate', 'ratio', 'return-to-dns',
            'round-robin', 'static-persistence', 'topology', 'virtual-server-capacity', 'virtual-server-score'
        ]
    canonical_name:
        description:
            - Specifies the canonical name of the zone.
    disabled:
        description:
            - Specifies whether the data center and its resources are available for load balancing.
        default: false
    dynamic_ratio:
        description:
            - Enables or disables a dynamic ratio load balancing algorithm for this pool.
        default: disabled
        choices: ['disabled', 'enabled']
    enabled:
        description:
            - Specifies whether the data center and its resources are available for load balancing.
        default: true
    fallback_ipv4:
        description:
            - Specifies the IPv4 address of the server to which the system directs requests in the event that the load
              balancing methods configured for this pool fail to return a valid virtual server.
        default: '::'
    fallback_ipv6:
        description:
            - Specifies the IPv6 address of the server to which the system directs requests in the event that the load
              balancing methods configured for this pool fail to return a valid virtual server.
        default: '::'
    fallback_mode:
        description:
            - Specifies the load balancing mode that the system uses to load balance name resolution requests among the
              members of this pool, if the preferred and alternate modes are unsuccessful in picking a pool.
        default: return-to-dns
        choices: [
            'completion-rate', 'cpu', 'drop-packet', 'fallback-ip', 'fewest-hops', 'global-availability',
            'kilobytes-per-second', 'least-connections', 'lowest-round-trip-time', 'none', 'packet-rate',
            'quality-of-service', 'ratio', 'return-to-dns', 'round-robin', 'static-persistence', 'topology',
            'virtual-server-capacity', 'virtual-server-score'
        ]
    limit_max_bps:
        description:
            - Specifies the maximum allowable data throughput rate, in bits per second, for the virtual servers in the
              pool.
        default: 0
    limit_max_bps_status:
        description:
            - Enables or disables the limit-max-bps option for this pool.
        default: disabled
        choices: ['disabled', 'enabled']
    limit_max_connections:
        description:
            - Specifies the number of current connections allowed for the virtual servers in the pool.
        default: 0
    limit_max_connections_status:
        description:
            - Enables or disables the limit-max-connections option for this pool.
        default: disabled
        choices: ['disabled', 'enabled']
    limit_max_pps:
        description:
            - Specifies the maximum allowable data transfer rate, in packets per second, for the virtual servers in the
              pool.
        default: 0
    limit_max_pps_status:
        description:
            - Enables or disables the limit-max-pps option for this pool.
        default: disabled
        choices: ['disabled', 'enabled']
    load_balancing_mode:
        description:
            - Specifies the preferred load balancing mode that the system uses to load balance name resolution requests
              among the members of this pool.
        default: round-robin
        choices: [
            'completion-rate', 'cpu', 'drop-packet', 'fallback-ip', 'fewest-hops', 'global-availability',
            'kilobytes-per-second', 'least-connections', 'lowest-round-trip-time', 'packet-rate',
            'quality-of-service', 'ratio', 'return-to-dns', 'round-robin', 'static-persistence', 'topology',
            'virtual-server-capacity', 'virtual-server-score'
        ]
    manual_resume:
        description:
            - Enables or disables the manual resume function for this pool.
        default: disabled
        choices: ['disabled', 'enabled']
    max_addresses_returned:
        description:
            - Specifies the maximum number of available virtual servers that the system lists in an A record response.
        default: 1
    members:
        description:
            - Specifies the vs-name of the pool members.
    monitor:
        description:
            - Specifies the health monitors that the system uses to determine whether it can use this pool for load
              balancing.
    qos_hit_ratio:
        description:
            - Assigns a weight to the Hit Ratio performance factor for the Quality of Service dynamic load balancing
              mode.
        default: 5
    qos_hops:
        description:
            - Assigns a weight to the Hops performance factor when the value of the either the load-balancing-mode or
              fallback-mode options is quality-of-service.
        default: 0
    qos_kilobytes_second:
        description:
            - Assigns a weight to the Kilobytes per Second performance factor when the value of the either the
              load-balancing-mode or fallback-mode options is quality-of-service.
        default: 3
    qos_lcs:
        description:
            - Assigns a weight to the Link Capacity performance factor when the value of the either the
              load-balancing-mode or fallback-mode options is quality-of-service.
        default: 30
    qos_packet_rate:
        description:
            - Assigns a weight to the Packet Rate performance factor when the value of the either the
              load-balancing-mode or fallback-mode options is quality-of-service.
        default: 1
    qos_rtt:
        description:
            - Assigns a weight to the Round Trip Time performance factor when the value of the either the
              load-balancing-mode or fallback-mode options is quality-of-service.
        default: 50
    qos_topology:
        description:
            - Assigns a weight to the Topology performance factor when the value of the either the load-balancing-mode
              or fallback-mode options is quality-of-service.
        default: 0
    qos_vs_capacity:
        description:
            - Assigns a weight to the Virtual Server performance factor when the value of the either the
              load-balancing-mode or fallback-mode options is quality-of-service.
        default: 0
    qos_vs_score:
        description:
            - Assigns a weight to the Virtual Server Score performance factor when the value of the either the
              load-balancing-mode or fallback-mode options is quality-of-service.
        default: 0
    ttl:
        description:
            - Specifies the number of seconds that the IP address, once found, is valid.
        default: 30
    verify_member_availability:
        description:
            - Specifies that the system verifies the availability of the members before sending a connection to those
              resources.
        default: enabled
        choices: ['disabled', 'enabled']
extends_documentation_fragment:
    - f5_common
    - f5_app_service
    - f5_description
    - f5_name
    - f5_partition
    - f5_state
"""

EXAMPLES = """
- name: Create GTM Pool
  f5bigip_gtm_pool:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: my_pool
    partition: Common
    description: My pool
    load_balancing_mode: global-availability
    members:
      - my_server:my_vs1
      - my_server:my_vs2
    state: present
  delegate_to: localhost
"""

RETURN = """ # """

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.erjac77.network.f5.common import F5_ACTIVATION_CHOICES
from ansible.module_utils.erjac77.network.f5.common import F5_NAMED_OBJ_ARGS
from ansible.module_utils.erjac77.network.f5.common import F5_PROVIDER_ARGS
from ansible.module_utils.erjac77.network.f5.bigip import F5BigIpNamedObject
from f5.bigip.resource import OrganizingCollection


class ModuleParams(object):
    @property
    def argument_spec(self):
        argument_spec = dict(
            alternate_mode=dict(
                type="str",
                choices=[
                    "drop-packet",
                    "fallback-ip",
                    "global-availability",
                    "none",
                    "packet-rate",
                    "ratio",
                    "return-to-dns",
                    "round-robin",
                    "static-persistence",
                    "topology",
                    "virtual-server-capacity",
                    "virtual-server-score",
                ],
            ),
            app_service=dict(type="str"),
            canonical_name=dict(type="str"),
            description=dict(type="str"),
            disabled=dict(type="bool"),
            enabled=dict(type="bool"),
            dynamic_ratio=dict(type="str", choices=[F5_ACTIVATION_CHOICES]),
            fallback_ipv4=dict(type="str"),
            fallback_ipv6=dict(type="str"),
            fallback_mode=dict(
                type="str",
                choices=[
                    "completion-rate",
                    "cpu",
                    "drop-packet",
                    "fallback-ip",
                    "fewest-hops",
                    "global-availability",
                    "kilobytes-per-second",
                    "least-connections",
                    "lowest-round-trip-time",
                    "none",
                    "packet-rate",
                    "quality-of-service",
                    "ratio",
                    "return-to-dns",
                    "round-robin",
                    "static-persistence",
                    "topology",
                    "virtual-server-capacity",
                    "virtual-server-score",
                ],
            ),
            limit_max_bps=dict(type="int"),
            limit_max_bps_status=dict(type="str", choices=[F5_ACTIVATION_CHOICES]),
            limit_max_connections=dict(type="int"),
            limit_max_connections_status=dict(
                type="str", choices=[F5_ACTIVATION_CHOICES]
            ),
            limit_max_pps=dict(type="int"),
            limit_max_pps_status=dict(type="str", choices=[F5_ACTIVATION_CHOICES]),
            load_balancing_mode=dict(
                type="str",
                choices=[
                    "completion-rate",
                    "cpu",
                    "drop-packet",
                    "fallback-ip",
                    "fewest-hops",
                    "global-availability",
                    "kilobytes-per-second",
                    "least-connections",
                    "lowest-round-trip-time",
                    "packet-rate",
                    "quality-of-service",
                    "ratio",
                    "return-to-dns",
                    "round-robin",
                    "static-persistence",
                    "topology",
                    "virtual-server-capacity",
                    "virtual-server-score",
                ],
            ),
            manual_resume=dict(type="str", choices=[F5_ACTIVATION_CHOICES]),
            max_addresses_returned=dict(type="int"),
            members=dict(type="list"),
            # metadata=dict(type="list"),
            monitor=dict(type="str"),
            qos_hit_ratio=dict(type="int"),
            qos_hops=dict(type="int"),
            qos_kilobytes_second=dict(type="int"),
            qos_lcs=dict(type="int"),
            qos_packet_rate=dict(type="int"),
            qos_rtt=dict(type="int"),
            qos_topology=dict(type="int"),
            qos_vs_capacity=dict(type="int"),
            qos_vs_score=dict(type="int"),
            ttl=dict(type="int"),
            verify_member_availability=dict(
                type="str", choices=[F5_ACTIVATION_CHOICES]
            ),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True

    @property
    def mutually_exclusive(self):
        return [["disabled", "enabled"]]


class F5BigIpGtmPool(F5BigIpNamedObject):
    def _set_crud_methods(self):
        if isinstance(self._api.tm.gtm.pools, OrganizingCollection):
            self._methods = {
                "create": self._api.tm.gtm.pools.a_s.a.create,
                "read": self._api.tm.gtm.pools.a_s.a.load,
                "update": self._api.tm.gtm.pools.a_s.a.update,
                "delete": self._api.tm.gtm.pools.a_s.a.delete,
                "exists": self._api.tm.gtm.pools.a_s.a.exists,
            }
        else:
            self._methods = {
                "create": self._api.tm.gtm.pools.pool.create,
                "read": self._api.tm.gtm.pools.pool.load,
                "update": self._api.tm.gtm.pools.pool.update,
                "delete": self._api.tm.gtm.pools.pool.delete,
                "exists": self._api.tm.gtm.pools.pool.exists,
            }


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
        mutually_exclusive=params.mutually_exclusive,
    )

    try:
        obj = F5BigIpGtmPool(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
