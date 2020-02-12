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
module: f5bigip_ltm_nat
short_description: BIG-IP ltm nat module
description:
    - Configures network address translation (NAT) for the Local Traffic Manager.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Gabriel Fortin (@GabrielFortin)"
options:
    arp:
        description:
            - Enables or disables Address Resolution Protocol (ARP).
        choices: ['enabled', 'disabled']
    auto_lasthop:
        description:
            - When enabled, allows the system to send return traffic to the MAC address that transmitted the request,
              even if the routing table points to a different network or interface.
        choices: ['default', 'enabled', 'disabled']
    disabled:
        description:
            - Enables or disables the specified interface.
        type: bool
        default: false
    enabled:
        description:
            - Enables or disables the specified interface.
        type: bool
        default: true
    originating_address:
        description:
            - Specifies the IP address from which traffic is being initiated.
    traffic_group:
        description:
            - Specifies the traffic group of the failover device group on which the NAT is active.
    translation_address:
        description:
            - Specifies the IP address that is translated or mapped, and the IP address to which it is translated or
              mapped.
    vlans:
        description:
            - Specifies a list of existing VLANs on which access to the NAT is enabled or disabled.
    vlans_disabled:
        description:
            - Indicates the NAT is disabled on the list of VLANs.
        type: bool
    vlans_enabled:
        description:
            - Indicates the NAT is enabled on the list of VLANs.
        type: bool
extends_documentation_fragment:
    - f5_common
    - f5_app_service
    - f5_description
    - f5_name
    - f5_partition
    - f5_state
"""

EXAMPLES = """
- name: Create LTM NAT
  f5bigip_ltm_nat:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: my_nat
    partition: Common
    description: My nat
    originating_address: 10.0.1.43
    translation_address: 10.10.10.253
    vlans_enabled: true
    vlans: external
    state: present
  delegate_to: localhost
"""

RETURN = """ # """

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.erjac77.network.f5.common import F5_ACTIVATION_CHOICES
from ansible.module_utils.erjac77.network.f5.common import F5_NAMED_OBJ_ARGS
from ansible.module_utils.erjac77.network.f5.common import F5_PROVIDER_ARGS
from ansible.module_utils.erjac77.network.f5.bigip import F5BigIpNamedObject


class ModuleParams(object):
    @property
    def argument_spec(self):
        argument_spec = dict(
            app_service=dict(type="str"),
            arp=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            auto_lasthop=dict(type="str", choices=["default", "enabled", "disabled"]),
            description=dict(type="str"),
            disabled=dict(type="bool"),
            enabled=dict(type="bool"),
            originating_address=dict(type="str"),
            traffic_group=dict(type="str"),
            translation_address=dict(type="str"),
            vlans=dict(type="list"),
            vlans_disabled=dict(type="bool"),
            vlans_enabled=dict(type="bool"),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True

    @property
    def mutually_exclusive(self):
        return [["enabled", "disabled"], ["vlans_disabled", "vlans_enabled"]]


class F5BigIpLtmNat(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "create": self._api.tm.ltm.nats.nat.create,
            "read": self._api.tm.ltm.nats.nat.load,
            "update": self._api.tm.ltm.nats.nat.update,
            "delete": self._api.tm.ltm.nats.nat.delete,
            "exists": self._api.tm.ltm.nats.nat.exists,
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
        mutually_exclusive=params.mutually_exclusive,
    )

    try:
        obj = F5BigIpLtmNat(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
