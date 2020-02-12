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
module: f5bigip_ltm_profile_response_adapt
short_description: BIG-IP ltm profile response adapt module
description:
    - Configures a HTTP response adaptation profile.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Gabriel Fortin (@GabrielFortin)"
options:
    allow_http_10:
        description:
            - Specifies whether to forward HTTP version 1.
        default: no
        choices: ['no', 'yes']
    defaults_from:
        description:
            - Specifies the profile that you want to use as the parent profile.
        default: responseadapt
    enabled:
        description:
            - Enables adaptation of HTTP responses.
        default: yes
        choices: ['no', 'yes']
    internal_virtual:
        description:
            - Specifies the name of the internal virtual server to use for adapting the HTTP response.
    preview_size:
        description:
            - Specifies the maximum size of the preview buffer.
        default: 1024
    service_down_action:
        description:
            - Specifies the action to take if the internal virtual server does not exist or returns an error.
        default: ignore
        choices: ['ignore', 'reset', 'drop']
    timeout:
        description:
            - Specifies a timeout in milliseconds.
        default: 0
extends_documentation_fragment:
    - f5_common
    - f5_app_service
    - f5_name
    - f5_partition
    - f5_state
"""

EXAMPLES = """
- name: Create LTM Profile Response Adapt
  f5bigip_ltm_profile_response_adapt:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: my_response_adapt_profile
    partition: Common
    description: My response adapt profile
    state: present
  delegate_to: localhost
"""

RETURN = """ # """

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.erjac77.network.f5.common import F5_NAMED_OBJ_ARGS
from ansible.module_utils.erjac77.network.f5.common import F5_POLAR_CHOICES
from ansible.module_utils.erjac77.network.f5.common import F5_PROVIDER_ARGS
from ansible.module_utils.erjac77.network.f5.bigip import F5BigIpNamedObject


class ModuleParams(object):
    @property
    def argument_spec(self):
        argument_spec = dict(
            allow_http_10=dict(type="str", choices=F5_POLAR_CHOICES),
            app_service=dict(type="str"),
            defaults_from=dict(type="str"),
            enabled=dict(type="str", choices=F5_POLAR_CHOICES),
            internal_virtual=dict(type="str"),
            preview_size=dict(type="int"),
            service_down_action=dict(type="str", choices=["ignore", "reset", "drop"]),
            timeout=dict(type="int"),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpLtmProfileResponseAdapt(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "create": self._api.tm.ltm.profile.response_adapts.response_adapt.create,
            "read": self._api.tm.ltm.profile.response_adapts.response_adapt.load,
            "update": self._api.tm.ltm.profile.response_adapts.response_adapt.update,
            "delete": self._api.tm.ltm.profile.response_adapts.response_adapt.delete,
            "exists": self._api.tm.ltm.profile.response_adapts.response_adapt.exists,
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpLtmProfileResponseAdapt(
            check_mode=module.check_mode, **module.params
        )
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
