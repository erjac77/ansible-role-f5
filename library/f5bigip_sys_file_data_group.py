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
module: f5bigip_sys_file_data_group
short_description: BIG-IP sys file data-group module
description:
    - Configures an external class.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Eric Jacob (@erjac77)"
options:
    data_group_description:
        description:
            - Specifies descriptive text that identifies the component.
    data_group_name:
        description:
            - Specifies the name of the external data group that will be created within the ltm data-group module and
              reference the given data group file.
    separator:
        description:
            - Specifies a separator to use when defining the data group.
        default: :=
    source_path:
        description:
            - This optional attribute takes a URL.
    type:
        description:
            - Specifies the kind of data in the group.
        default: present
        choices: ['integer', 'ip', 'string']
extends_documentation_fragment:
    - f5_common
    - f5_app_service
    - f5_name
    - f5_partition
    - f5_state
"""

EXAMPLES = """
- name: Create LTM External Data-Group file
  f5bigip_sys_file_data_group:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: my_ext_dg_file
    partition: Common
    source_path: file:/var/config/rest/downloads/my_ext_dg.dat
    type: string
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
            data_group_description=dict(type="str"),
            data_group_name=dict(type="str"),
            separator=dict(type="str"),
            source_path=dict(type="str"),
            type=dict(type="str", choices=["integer", "ip", "string"]),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpSysFileDataGroup(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "create": self._api.tm.sys.file.data_groups.data_group.create,
            "read": self._api.tm.sys.file.data_groups.data_group.load,
            "update": self._api.tm.sys.file.data_groups.data_group.update,
            "delete": self._api.tm.sys.file.data_groups.data_group.delete,
            "exists": self._api.tm.sys.file.data_groups.data_group.exists,
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpSysFileDataGroup(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
