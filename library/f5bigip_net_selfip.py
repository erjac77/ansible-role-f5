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
module: f5bigip_net_selfip
short_description: BIG-IP net selfip module
description:
    - Configures a self IP address for a VLAN.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Eric Jacob (@erjac77)"
options:
    address [ip address/netmask]:
        description:
            - Specifies the IP address and netmask to be assigned to the system. Must appear in the format [ip
              address/mask].
    allow_service:
        description:
    traffic_group:
        description:
            - Specifies the traffic group of the self IP address.
        default: traffic-group-local-only
    vlan:
        description:
            - Specifies the VLAN for which you are setting a self IP address.
        default: traffic-group-local-only
extends_documentation_fragment:
    - f5_common
    - f5_app_service
    - f5_description
    - f5_name
    - f5_partition
    - f5_state
"""

EXAMPLES = """
- name: Create NET Self IP
  f5bigip_net_selfip:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: my_self_ip
    address: 10.10.10.11/24
    vlan: internal
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
            address=dict(type="str"),
            allow_service=dict(type="list"),
            app_service=dict(type="str"),
            description=dict(type="str"),
            fw_enforced_policy=dict(type="str"),
            # fw_rules=dict(type='list'),
            fw_staged_policy=dict(type="str"),
            traffic_group=dict(type="str"),
            vlan=dict(type="str"),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpNetSelfip(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "create": self._api.tm.net.selfips.selfip.create,
            "read": self._api.tm.net.selfips.selfip.load,
            "update": self._api.tm.net.selfips.selfip.update,
            "delete": self._api.tm.net.selfips.selfip.delete,
            "exists": self._api.tm.net.selfips.selfip.exists,
        }

    def _read(self):
        selfip = self._methods["read"](
            name=self._params["name"], partition=self._params["partition"]
        )
        selfip.vlan = self._strip_partition(selfip.vlan)
        return selfip


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpNetSelfip(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
