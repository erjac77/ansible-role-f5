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
module: f5bigip_net_tunnel_gre
short_description: BIG-IP net tunnel gre module
description:
    - Configures a Generic Router Encapsulation (GRE) profile.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Gabriel Fortin (@GabrielFortin)"
options:
    defaults_from:
        description:
            - Specifies the existing profile from which the system imports settings for the new profile.
        default: gre
    encapsulation:
        description:
            - Specifies the flavor of GRE header to use for encapsulation.
        default: standard
        choices: ['standard', 'nvgre']
    flooding_type:
        description:
            - Specifies the flooding type to use to transmit broadcast and unknown destination frames.
        choices: ['none', 'multipoint']
    rx_csum:
        description:
            - Specifies whether the system verifies the checksum on received packets.
        default: disabled
        choices: ['disabled', 'enabled']
    tx_csum:
        description:
            - Specifies whether the system includes a checksum on transmitted packets.
        default: disabled
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
- name: Create NET Tunnel GRE
  f5bigip_net_tunnel_gre:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: my_gre_tunnel
    partition: Common
    description: My gre tunnel
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
            defaults_from=dict(type="str"),
            description=dict(type="str"),
            encapsulation=dict(type="str", choices=["standard", "nvgre"]),
            flooding_type=dict(type="str", choices=["none", "multipoint"]),
            rx_csum=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            tx_csum=dict(type="str", choices=F5_ACTIVATION_CHOICES),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpNetTunnelGre(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "create": self._api.tm.net.tunnels.gres.gre.create,
            "read": self._api.tm.net.tunnels.gres.gre.load,
            "update": self._api.tm.net.tunnels.gres.gre.update,
            "delete": self._api.tm.net.tunnels.gres.gre.delete,
            "exists": self._api.tm.net.tunnels.gres.gre.exists,
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpNetTunnelGre(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
