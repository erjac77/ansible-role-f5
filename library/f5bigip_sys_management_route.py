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
module: f5bigip_sys_management_route
short_description: BIG-IP sys management route module
description:
    - Configures route settings for the management interface (MGMT).
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Eric Jacob (@erjac77)"
options:
    gateway:
        description:
            - Specifies that the system forwards packets to the destination through the gateway with the specified IP
              address.
    mtu:
        description:
            - Specifies the maximum transmission unit (MTU) for the management interface.
    network:
        description:
            - The subnet and netmask to be used for the route.
extends_documentation_fragment:
    - f5_common
    - f5_description
    - f5_name
    - f5_state
"""

EXAMPLES = """
- name: Sets the management interface default gateway IP address
  f5bigip_sys_management_route:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: default
    gateway: 10.10.10.254
    state: present
  delegate_to: localhost

- name: Creates a management route
  f5bigip_sys_management_route:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: my_mgmt_route
    network: 10.10.20.0/24
    gateway: 10.10.10.254
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
            description=dict(type="str"),
            gateway=dict(type="str"),
            mtu=dict(type="int"),
            network=dict(type="str"),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        del argument_spec["partition"]
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpSysManagementRoute(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "create": self._api.tm.sys.management_routes.management_route.create,
            "read": self._api.tm.sys.management_routes.management_route.load,
            "update": self._api.tm.sys.management_routes.management_route.update,
            "delete": self._api.tm.sys.management_routes.management_route.delete,
            "exists": self._api.tm.sys.management_routes.management_route.exists,
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpSysManagementRoute(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
