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
module: f5bigip_sys_folder
short_description: BIG-IP sys folder module
description:
    - Configure folders (directory structure) on the BIG-IP system.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Eric Jacob (@erjac77)"
options:
    device_group:
        description:
            - Adds this folder and all configuration items in this folder to a device group for device failover or
              config-sync purposes.
    no_ref_check:
        description:
            - Specifies whether strict device group reference validation is performed on configuration items in the
              folder.
        default: false
    traffic_group:
        description:
            - Adds this folder and its configuration items to an existing traffic group.
        default: false
extends_documentation_fragment:
    - f5_common
    - f5_app_service
    - f5_description
    - f5_name
    - f5_state
"""

EXAMPLES = """
- name: Create SYS Folder
  f5bigip_sys_folder:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: my_folder
    description: My folder
    sub_path: /
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
            app_service=dict(type="str"),
            description=dict(type="str"),
            device_group=dict(type="str"),
            no_ref_check=dict(type="bool"),
            traffic_group=dict(type="str"),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        argument_spec.update(dict(sub_path=dict(type="str", default="/")))
        del argument_spec["partition"]
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpSysFolder(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "create": self._api.tm.sys.folders.folder.create,
            "read": self._api.tm.sys.folders.folder.load,
            "update": self._api.tm.sys.folders.folder.update,
            "delete": self._api.tm.sys.folders.folder.delete,
            "exists": self._api.tm.sys.folders.folder.exists,
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpSysFolder(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
