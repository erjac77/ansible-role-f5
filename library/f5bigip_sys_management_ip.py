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
module: f5bigip_sys_management_ip
short_description: BIG-IP sys management ip module
description:
    - Configures the ip address and netmask for the management interface (MGMT).
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Gabriel Fortin (@GabrielFortin)"
options:
    mask:
        description:
            - Specifies the netmask (IPv4) or prefixlen (IPv6).
        required: true
extends_documentation_fragment:
    - f5_common
    - f5_description
    - f5_name
    - f5_partition
    - f5_state
"""

EXAMPLES = """
- name: Create SYS Management IP
  f5bigip_sys_management_ip:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: 10.2.3.4
    mask: 24
    description: My management ip
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
        argument_spec = dict(description=dict(type="str"), mask=dict(type="str"))
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        del argument_spec["partition"]
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpSysManagementIp(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "create": self._api.tm.sys.management_ips.management_ip.create,
            "read": self._api.tm.sys.management_ips.management_ip.load,
            "exists": self._api.tm.sys.management_ips.management_ip.exists,
        }

    def modify(self):
        try:
            obj = self._methods["read"](name=self._params["name"])
            for k, v in self._params.iteritems():

                if hasattr(obj, k):
                    cur_val = v
                    new_val = getattr(obj, k)

                    if cur_val != new_val:
                        obj.modify(**self._params)
                        return True
        except Exception:
            pass

        return False

    def _create(self):
        self._params["name"] += "/" + self._params["mask"]

        try:
            self._methods["create"](**self._params)
        except Exception:
            return self.modify()

        return True


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpSysManagementIp(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
