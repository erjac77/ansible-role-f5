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
module: f5bigip_ltm_profile_mssql
short_description: BIG-IP ltm profile mssql module
description:
    - Configures a profile to manage mssql(tds) database traffic.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Gabriel Fortin (@GabrielFortin)"
options:
    defaults_from:
        description:
            - Specifies the profile that you want to use as the parent profile.
        default: mssql
    read_pool:
        description:
            - Specifies the pool of MS SQL database servers to which the system sends ready-only requests.
    read_write_split_by_command:
        description:
            - When enabled, the system decides which pool to send the client requests the by the content in the message.
        default: disabled
        choices: ['disabled', 'enabled']
    read_write_split_by_user:
        description:
            - When enabled, the system decides which pool to send the client requests the by user name.
        default: disabled
        choices: ['disabled', 'enabled']
    user_can_write_by_default:
        description:
            - Specifies whether users have write access by default.
        default: true
        choices: ['false', 'true']
    user_list:
        description:
            - Specifies the users who have read-only access to the MS SQL if user-can-write-by-default is true, or the
              users who have write access to the MS SQL database if user-can-write-by-default is false.
    write_persist_timer:
        description:
            - Specify how many minimum time in milliseconds the connection will be persisted to write-pool after
              connection switch to write pool.
    write_pool:
        description:
            - Specifies the pool of MS SQL database servers to which the system sends requests that are not read-only.
extends_documentation_fragment:
    - f5_common
    - f5_app_service
    - f5_description
    - f5_name
    - f5_partition
    - f5_state
"""

EXAMPLES = """
- name: Create LTM Profile MSSQL
  f5bigip_ltm_profile_mssql:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: my_mssql_profile
    partition: Common
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
            read_pool=dict(type="str"),
            read_write_split_by_command=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            read_write_split_by_user=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            user_can_write_by_default=dict(type="str", choices=["false", "true"]),
            user_list=dict(type="list"),
            write_persist_timer=dict(type="int"),
            write_pool=dict(type="str"),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpLtmProfileMssql(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "create": self._api.tm.ltm.profile.mssqls.mssql.create,
            "read": self._api.tm.ltm.profile.mssqls.mssql.load,
            "update": self._api.tm.ltm.profile.mssqls.mssql.update,
            "delete": self._api.tm.ltm.profile.mssqls.mssql.delete,
            "exists": self._api.tm.ltm.profile.mssqls.mssql.exists,
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpLtmProfileMssql(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
