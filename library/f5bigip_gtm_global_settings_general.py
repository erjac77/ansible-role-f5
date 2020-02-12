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
module: f5bigip_gtm_global_settings_general
short_description: BIG-IP gtm global-settings general module
description:
    - Configures the general settings for the Global Traffic Manager.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Gabriel Fortin (@GabrielFortin)"
options:
    automatic_configuration_save_timeout:
        description:
            - Sets the timeout, in seconds, indicating how long to wait after a GTM configuration change before
              automatically saving the GTM configuration to the bigip_gtm.conf.
        default: 15
    auto_discovery:
        description:
            - Specifies whether the auto-discovery process is activated for this system.
        default: no
        choices: ['yes', 'no']
    auto_discovery_interval:
        description:
            - Specifies the frequency, in seconds, between system attempts to discover network components.
        default: 30
    cache_ldns_servers:
        description:
            - Specifies whether the system retains, in cache, all local DNS servers that make requests.
        default: yes
        choices: ['yes', 'no']
    domain_name_check:
        description:
            - Specifies the parameters for the Global Traffic Manager to use when performing domain name checking.
        default: strict
        choices: ['allow_underscore', 'idn_compatible', 'none', 'strict']
    drain_persistent_requests:
        description:
            - Specifies, when set to yes, that when you disable a pool, load-balanced, persistent connections remain
              connected until the TTL expires.
        default: yes
        choices: ['yes', 'no']
    forward_status:
        description:
            - Specifies, when set to enabled, that the availability status change for GTM objects will be shared with
              subscribers.
        choices: ['enabled', 'disabled']
    gtm_sets_recursion:
        description:
            - Specifies, when set to yes, that the system enables recursive DNS queries, regardless of whether the
              requesting local DNS enabled recursive queries.
        default: no
        choices: ['yes', 'no']
    heartbeat_interval:
        description:
            - Specifies the frequency at which the Global Traffic Manager queries other BIG-IP systems for updated data.
        default: 10
        choices: range(0, 11)
    monitor_disabled_objects:
        description:
            - Specifies, when set to yes, that the system will continue to monitor objects even if the objects are
              disabled.
        default: no
        choices: ['yes', 'no']
    nethsm_timeout:
        description:
            - Time to wait on a NetHSM key creation operation for DNSSEC before retry.
        default: 20
    peer_leader:
        description:
            - Specifies the name of a GTM server to be used for executing certain features, such as creating DNSSEC
              keys.
    port:
        description:
            - Specifies the port on which the listener listens for connections.
    send_wildcard_rrs:
        description:
            - Specifies, when set to enable, that WideIPs or WideIP aliases that contain wildcards will autogenerate
              Resource Records in the BIND database.
        default: disable
        choices: ['enable', 'disable']
    static_persist_cidr_ipv4:
        description:
            - Specifies the number of bits of the IPv4 address that the system considers when using the Static Persist
              load balancing mode.
        default: 32
    static_persist_cidr_ipv6:
        description:
            - Specifies the number of bits of the IPv6 address that the system considers when using the Static Persist
              load balancing mode.
        default: 128
    synchronization:
        description:
            - Specifies whether this system is a member of a synchronization group.
        default: no
        choices: ['yes', 'no']
    synchronization_group_name:
        description:
            - Specifies the name of the synchronization group to which the system belongs.
        default: default
    synchronization_time_tolerance:
        description:
            - Specifies the number of seconds that one system clock can be out of sync with another system clock, in the
              synchronization group.
        default: 10
        choices: [0, range(5, 601)]
    synchronization_timeout:
        description:
            - Specifies the number of seconds that the system attempts to synchronize the Global Traffic Manager
              configuration with a synchronization group member.
        default: 180
    synchronize_zone_files:
        description:
            - Specifies whether the system synchronizes zone files among the synchronization group members.
        default: no
        choices: ['yes', 'no']
    synchronize_zone_files_timeout:
        description:
            - Specifies the number of seconds that a synchronization group member attempts to synchronize its zone files
              with a synchronization group member.
        default: 300
    topology_allow_zero_scores:
        description:
            - Specifies if topology load-balancing or QoS load-balancing with topology enabled will return pool members
              with zero topology scores.
        default: yes
        choices: ['yes', 'no']
    virtuals_depend_on_server_state:
        description:
            - Specifies whether the system marks a virtual server down when the server on which the virtual server is
              configured can no longer be reached via iQuery.
        default: yes
        choices: ['yes', 'no']
extends_documentation_fragment:
    - f5_common
"""

EXAMPLES = """
- name: Change GTM Global General Settings heartbeat interval
  f5bigip_gtm_global_settings_general:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    heartbeat_interval: 8
  delegate_to: localhost
"""

RETURN = """ # """

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six.moves import range
from ansible.module_utils.erjac77.network.f5.common import F5_ACTIVATION_CHOICES
from ansible.module_utils.erjac77.network.f5.common import F5_POLAR_CHOICES
from ansible.module_utils.erjac77.network.f5.common import F5_PROVIDER_ARGS
from ansible.module_utils.erjac77.network.f5.bigip import F5BigIpUnnamedObject


class ModuleParams(object):
    @property
    def argument_spec(self):
        argument_spec = dict(
            automatic_configuration_save_timeout=dict(type="int"),
            auto_discovery=dict(type="str", choices=F5_POLAR_CHOICES),
            auto_discovery_interval=dict(type="int"),
            cache_ldns_servers=dict(type="str", choices=F5_POLAR_CHOICES),
            domain_name_check=dict(
                type="str",
                choices=["allow_underscore", "idn_compatible", "none", "strict"],
            ),
            drain_persistent_requests=dict(type="str", choices=F5_POLAR_CHOICES),
            forward_status=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            gtm_sets_recursion=dict(type="str", choices=F5_POLAR_CHOICES),
            heartbeat_interval=dict(type="int", choices=range(0, 11)),
            monitor_disabled_objects=dict(type="str", choices=F5_POLAR_CHOICES),
            nethsm_timeout=dict(type="int"),
            peer_leader=dict(type="str"),
            send_wildcards_rrs=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            static_persist_cidr_ipv4=dict(type="int"),
            static_persist_cidr_ipv6=dict(type="int"),
            synchronization=dict(type="str", choices=F5_POLAR_CHOICES),
            synchronization_group_name=dict(type="str"),
            synchronization_time_tolerance=dict(type="int", choices=[0, range(5, 601)]),
            synchronization_timeout=dict(type="int"),
            synchronize_zone_files=dict(type="str", choices=F5_POLAR_CHOICES),
            synchronize_zone_files_timeout=dict(type="int"),
            topology_allow_zero_scores=dict(type="str", choices=F5_POLAR_CHOICES),
            virtuals_depend_on_server_state=dict(type="str", choices=F5_POLAR_CHOICES),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpGtmGlobalSettingsGeneral(F5BigIpUnnamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "read": self._api.tm.gtm.global_settings.general.load,
            "update": self._api.tm.gtm.global_settings.general.update,
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpGtmGlobalSettingsGeneral(
            check_mode=module.check_mode, **module.params
        )
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
