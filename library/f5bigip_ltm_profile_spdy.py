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
module: f5bigip_ltm_profile_spdy
short_description: BIG-IP ltm profile spdy module
description:
    - Configures a SPDY protocol profile.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Gabriel Fortin (@GabrielFortin)"
options:
    activation_mode:
        description:
            - Specifies what will cause a connection to be treated as a SPDY connection.
        default: npn
        choices: ['npn', 'always']
    compression_level:
        description:
            - Specifies the level of compression used by default.
        default: 5
    compression_window_size:
        description:
            - Specifies the size of the compression window, in KB.
        default: 8
    concurrent_streams_per_connection:
        description:
            - Specifies how many concurrent requests are allowed to be outstanding on a single SPDY connection.
    connection_idle_timeout:
        description:
            - Specifies how many seconds a SPDY connection is left open idly before it is shutdown.
    defaults_from:
        description:
            - Specifies the profile that you want to use as the parent profile.
        default: spdy
    frame_size:
        description:
            - Specifies the size of the data frames, in bytes, that SPDY will send to the client.
        default: 2048
    insert_header:
        description:
            - Specifies the name of the HTTP header controlled by insert-header.
        required: true
        default: disabled
        choices: ['disabled', 'enabled']
    insert_header_name:
        description:
            - Specifies the name of the HTTP header controlled by insert-header.
        required: true
        default: X-SPDY
    priority_handling:
        description:
            - Specifies how SPDY should handle priorities of concurrent streams within the same connection.
        default: strict
        choices: ['strict', 'fair']
    protocol_versions:
        description:
            - Specifies which SPDY protocols clients are allowed to use.
        default: { spdy3 spdy2 http1.1 }
        choices: ['spdy3', 'spdy2', 'http1.1']
    receive_window:
        description:
            - Specifies the receive window, in KB.
        default: 32
    write_size:
        description:
            - Specifies the total size of combined data frames, in bytes, SPDY will send in a single write.
        default: 16384
extends_documentation_fragment:
    - f5_common
    - f5_app_service
    - f5_description
    - f5_name
    - f5_partition
    - f5_state
"""

EXAMPLES = """
- name: Create LTM Profile spdy
  f5bigip_ltm_profile_spdy:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: my_spdy_profile
    partition: Common
    description: My spdy profile
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
            activation_mode=dict(type="str", choices=["npn", "always"]),
            app_service=dict(type="str"),
            compression_level=dict(type="int"),
            compression_window_size=dict(type="int"),
            concurrent_streams_per_connection=dict(type="int"),
            connection_idle_timeout=dict(type="int"),
            defaults_from=dict(type="str"),
            description=dict(type="str"),
            frame_size=dict(type="int"),
            insert_header=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            insert_header_name=dict(type="str"),
            priority_handling=dict(type="str", choices=["strict", "fair"]),
            protocol_versions=dict(type="dict"),
            receive_window=dict(type="int"),
            write_size=dict(type="int"),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpLtmProfileSpdy(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "create": self._api.tm.ltm.profile.spdys.spdy.create,
            "read": self._api.tm.ltm.profile.spdys.spdy.load,
            "update": self._api.tm.ltm.profile.spdys.spdy.update,
            "delete": self._api.tm.ltm.profile.spdys.spdy.delete,
            "exists": self._api.tm.ltm.profile.spdys.spdy.exists,
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpLtmProfileSpdy(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
