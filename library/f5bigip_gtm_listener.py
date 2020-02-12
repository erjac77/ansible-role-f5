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
module: f5bigip_gtm_listener
short_description: BIG-IP gtm listener module
description:
    - Configures a Global Traffic Manager listener.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Eric Jacob (@erjac77)"
options:
    address:
        description:
            - Specifies the IP address on which the system listens.
        required: true
    advertise:
        description:
            - Specifies whether to advertise the listener address to surrounding routers.
        default: no
        choices: ['yes', 'no']
    auto_lasthop:
        description:
            - Specifies whether to automatically map last hop for pools or not.
        default: default
        choices: ['default', 'enabled', 'disabled']
    disabled:
        description:
            - Specifies the state of the listener.
        default: false
    enabled:
        description:
            - Specifies the state of the listener.
        default: true
    fallback_persistence:
        description:
            - Specifies a fallback persistence profile for the listener to use when the default persistence profile is
              not available.
    ip_protocol:
        description:
            - Specifies the protocol on which this listener receives network traffic.
        default: udp
        choices: ['tcp', 'udp']
    last_hop_pool:
        description:
            - Specifies the name of the last hop pool that you want the listener to use to direct reply traffic to the
              last hop router.
    mask:
        description:
            - Specifies the netmask for a network listener only.
        default: ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff
    persist:
        description:
            - Specifies a list of profiles separated by spaces that the listener uses to manage connection persistence.
    pool:
        description:
            - Specifies a default pool to which you want the listener to automatically direct traffic.
        default: 5
    port:
        description:
            - Specifies the port on which the listener listens for connections.
    profiles:
        description:
            - Specifies the DNS, statistics and protocol profiles to use for this listener.
    rules:
        description:
            - Specifies a list of iRules, that customize the listener to direct and manage traffic.
    source_address_translation:
        description:
            - Specifies the type of source address translation enabled for the listener as well as the pool that the
              source address translation will use.
        suboptions:
            pool:
                description:
                    - Specifies the name of a SNAT pool used by the specified listener.
            type:
                description:
                    - Specifies the type of source address translation associated with the specified listener.
                choices: ['automap', 'none', 'snat']
    source_port:
        description:
            - Specifies whether the system preserves the source port of the connection.
        default: preserve
        choices: ['change', 'preserve', 'preserve-strict']
    translate_address:
        description:
            - Enables or disables address translation for the listener.
        default: disabled
        choices: ['enabled', 'disabled']
    translate_port:
        description:
            - Enables or disables port translation.
        default: disabled
        choices: ['enabled', 'disabled']
    vlans:
        description:
            - Specifies a list of VLANs on which traffic is either disabled or enabled, based on the vlans-disabled and
              vlans-enabled settings.
    vlans_disabled:
        description:
            - Specifies that traffic will not be accepted by this listener on the VLANS specified in the vlans option.
    vlans_enabled:
        description:
            - Specifies that traffic will be accepted by this listener only on the VLANS specified in the vlans option.
extends_documentation_fragment:
    - f5_common
    - f5_app_service
    - f5_description
    - f5_name
    - f5_partition
"""

EXAMPLES = """
- name: Create GTM Listener
  f5bigip_gtm_listener:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: my_listener
    partition: Common
    description: My listener
    address: 10.10.1.1
    persist:
      - { name: dest_addr, partition: Common, tmDefault: 'yes' }
    profiles:
      - /Common/dns
    source_address_translation:
      type: automap
    state: present
  delegate_to: localhost
"""

RETURN = """ # """

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.erjac77.network.f5.base import AnsibleF5Error
from ansible.module_utils.erjac77.network.f5.common import F5_ACTIVATION_CHOICES
from ansible.module_utils.erjac77.network.f5.common import F5_NAMED_OBJ_ARGS
from ansible.module_utils.erjac77.network.f5.common import F5_PROVIDER_ARGS
from ansible.module_utils.erjac77.network.f5.bigip import F5BigIpNamedObject


class ModuleParams(object):
    @property
    def argument_spec(self):
        argument_spec = dict(
            address=dict(type="str"),
            advertise=dict(type="str"),
            app_service=dict(type="str"),
            auto_lasthop=dict(type="str", choices=["default", F5_ACTIVATION_CHOICES]),
            description=dict(type="str"),
            disabled=dict(type="bool"),
            enabled=dict(type="bool"),
            fallback_persistence=dict(type="str"),
            ip_protocol=dict(type="str", choices=["tcp", "udp"]),
            last_hop_pool=dict(type="str"),
            mask=dict(type="str"),
            persist=dict(type="list"),
            pool=dict(type="str"),
            port=dict(type="int"),
            profiles=dict(type="list"),
            rules=dict(type="list"),
            source_address_translation=dict(type="dict"),
            source_port=dict(
                type="str", choices=["change", "preserve", "preserve-strict"]
            ),
            translate_address=dict(
                type="str", choices=["default", F5_ACTIVATION_CHOICES]
            ),
            translate_port=dict(type="str", choices=["default", F5_ACTIVATION_CHOICES]),
            vlans=dict(type="list"),
            vlans_disabled=dict(type="str", choices=["default", F5_ACTIVATION_CHOICES]),
            vlans_enabled=dict(type="str", choices=["default", F5_ACTIVATION_CHOICES]),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True

    @property
    def mutually_exclusive(self):
        return [["disabled", "enabled"], ["vlans_disabled", "vlans_enabled"]]


class F5BigIpGtmListener(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "create": self._api.tm.gtm.listeners.listener.create,
            "read": self._api.tm.gtm.listeners.listener.load,
            "update": self._api.tm.gtm.listeners.listener.update,
            "delete": self._api.tm.gtm.listeners.listener.delete,
            "exists": self._api.tm.gtm.listeners.listener.exists,
        }

    @property
    def source_address_translation(self):
        if self._params["sourceAddressTranslation"]:
            if (
                self._params["sourceAddressTranslation"]["type"] == "automap"
                and "pool" in self._params["sourceAddressTranslation"]
            ):
                raise AnsibleF5Error("Cannot specify a pool when using automap.")
        else:
            return None


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
        mutually_exclusive=params.mutually_exclusive,
    )

    try:
        obj = F5BigIpGtmListener(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
