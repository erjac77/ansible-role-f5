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
module: f5bigip_ltm_profile_one_connect
short_description: BIG-IP ltm one-connect profile module
description:
    - Configures a one-connect profile.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Gabriel Fortin (@GabrielFortin)"
options:
    defaults_from:
        description:
            - Specifies the profile that you want to use as the parent profile.
        default: oneconnect
    idle_timeout_override:
        description:
            - Specifies the number of seconds that a connection is idle before the connection flow is eligible for
              deletion.
        default: disabled
        choices: ['enabled', 'disabled']
    port:
        description:
            - Specifies a service for the data channel port used for this one-connect profile.
    share_pools:
        description:
            - Indicates that connections may be shared not only within a virtual server, but also among similar virtual
              servers (e.g. those that differ only in destination address).
        choices: ['enabled', 'disabled']
    max_age:
        description:
            - Specifies the maximum age, in number of seconds, of a connection in the connection reuse pool.
        default: 86400
    max_reuse:
        description:
            - Specifies the maximum number of times that a server connection can be reused.
        default: 1000
    max_size:
        description:
            - Specifies the maximum number of connections that the system holds in the connection reuse pool.
        default: 10000
    source_mask:
        description:
            - Specifies a source IP mask.
        default: 0.0.0.0
    limit_type:
        description:
            - Connection limits with OneConnect are different from straight TCP connection limits.
        choices: ['none', 'idle', 'strict']
extends_documentation_fragment:
    - f5_common
    - f5_app_service
    - f5_description
    - f5_name
    - f5_partition
    - f5_state
"""

EXAMPLES = """
- name: Create LTM OneConnect profile
  f5bigip_ltm_profile_one_connect:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: my_one_connect_profile
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
            share_pools=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            max_age=dict(type="int"),
            max_reuse=dict(type="int"),
            max_size=dict(type="int"),
            source_mask=dict(type="str"),
            limit_type=dict(type="str", choices=["none", "idle", "strict"]),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpLtmProfileOneConnect(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "create": self._api.tm.ltm.profile.one_connects.one_connect.create,
            "read": self._api.tm.ltm.profile.one_connects.one_connect.load,
            "update": self._api.tm.ltm.profile.one_connects.one_connect.update,
            "delete": self._api.tm.ltm.profile.one_connects.one_connect.delete,
            "exists": self._api.tm.ltm.profile.one_connects.one_connect.exists,
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpLtmProfileOneConnect(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
