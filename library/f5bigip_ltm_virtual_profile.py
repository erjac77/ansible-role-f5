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
module: f5bigip_ltm_virtual_profile
short_description: BIG-IP ltm virtual profile module
description:
    - Configures profiles on the specified virtual server to direct and manage traffic.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Eric Jacob (@erjac77)"
options:
    context:
        description:
            - Specifies that the profile is either a clientside or serverside (or both) profile.
        default: all
        choices: ['all', 'clientside', 'serverside']
    virtual:
        description:
            - Specifies the full path of the virtual to which the profile belongs.
        required: true
extends_documentation_fragment:
    - f5_common
    - f5_app_service
    - f5_description
    - f5_name
    - f5_partition
    - f5_state
"""

EXAMPLES = """
- name: Add LTM HTTP Profile to VS
  f5bigip_ltm_virtual_profile:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: http
    partition: Common
    virtual: /Common/my_http_vs
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
            context=dict(type="str", choices=["all", "clientside", "serverside"]),
            virtual=dict(type="str"),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpLtmVirtualProfile(F5BigIpNamedObject):
    def _set_crud_methods(self):
        virtual = self._api.tm.ltm.virtuals.virtual.load(
            **self._get_resource_id_from_path(self._params["virtual"])
        )
        self._methods = {
            "create": virtual.profiles_s.profiles.create,
            "read": virtual.profiles_s.profiles.load,
            "update": virtual.profiles_s.profiles.update,
            "delete": virtual.profiles_s.profiles.delete,
            "exists": virtual.profiles_s.profiles.exists,
        }
        del self._params["virtual"]


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpLtmVirtualProfile(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
