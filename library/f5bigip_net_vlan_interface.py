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
module: f5bigip_net_vlan_interface
short_description: BIG-IP net vlan interface module
description:
    - Configures a tagged or untagged interface and trunk for a VLAN.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Eric Jacob (@erjac77)"
options:
    tag_mode:
        description:
            - Specifies the tag mode of the interface or trunk associated with.
        choices: ['customer', 'service', 'double', 'none']
    tagged:
        description:
            - Specifies the type of the interface.
        choices: ['true', 'false']
    untagged:
        description:
            - Specifies the type of the interface.
        choices: ['true', 'false']
    vlan:
        description:
            - Specifies the vlan in which the interface belongs.
        required: true
extends_documentation_fragment:
    - f5_common
    - f5_app_service
    - f5_name
    - f5_partition
    - f5_state
"""

EXAMPLES = """
- name: Add NET VLAN Interface
  f5bigip_net_vlan_interface:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: 1.1
    untagged: true
    tag_mode: none
    vlan: /Common/internal
    state: present
  delegate_to: localhost
"""

RETURN = """ # """

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.erjac77.network.f5.common import F5_NAMED_OBJ_ARGS
from ansible.module_utils.erjac77.network.f5.common import F5_PROVIDER_ARGS
from ansible.module_utils.erjac77.network.f5.bigip import F5BigIpNamedObject


class ModuleParams(object):
    @property
    def argument_spec(self):
        argument_spec = dict(
            tag_mode=dict(
                type="str", choices=["customer", "service", "double", "none"]
            ),
            tagged=dict(type="bool"),
            untagged=dict(type="bool"),
            vlan=dict(type="str", required=True),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        del argument_spec["partition"]
        return argument_spec

    @property
    def supports_check_mode(self):
        return True

    @property
    def mutually_exclusive(self):
        return [["tagged", "untagged"]]


class F5BigIpNetVlanInterface(F5BigIpNamedObject):
    def _set_crud_methods(self):
        vlan = self._api.tm.net.vlans.vlan.load(
            **self._get_resource_id_from_path(self._params["vlan"])
        )
        self._methods = {
            "create": vlan.interfaces_s.interfaces.create,
            "read": vlan.interfaces_s.interfaces.load,
            "update": vlan.interfaces_s.interfaces.update,
            "delete": vlan.interfaces_s.interfaces.delete,
            "exists": vlan.interfaces_s.interfaces.exists,
        }
        del self._params["vlan"]


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
        mutually_exclusive=params.mutually_exclusive,
    )

    try:
        obj = F5BigIpNetVlanInterface(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
