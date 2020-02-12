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
module: f5bigip_ltm_profile_http2
short_description: BIG-IP ltm profile http2 module
description:
    - Configures a HTTP/2 protocol profile.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Gabriel Fortin (@GabrielFortin)"
options:
    activation_modes:
        description:
            - Specifies what will cause a connection to be treated as a HTTP/2 connection.
        default: { npn alpn }
        choices: ['npn', 'alpn', 'always']
    concurrent_streams_per_connection:
        description:
            - Specifies how many concurrent requests are allowed to be outstanding on a single HTTP/2 connection.
    connection_idle_timeout:
        description:
            - Specifies how many seconds a HTTP/2 connection is left open idly before it is shutdown.
    defaults_from:
        description:
            - Specifies the profile that you want to use as the parent profile.
        default: http2
    frame_size:
        description:
            - Specifies the size of the data frames, in bytes, that HTTP/2 will send to the client.
        default: 2048
    header_table_size:
        description:
            - Specifies the size of the header table, in KB.
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
    receive_window:
        description:
            - Specifies the receive window, in KB.
    write_size:
        description:
            - Specifies the total size of combined data frames, in bytes, HTTP/2 will send in a single write.
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
- name: Create LTM Profile HTTP2
  f5bigip_ltm_profile_http2:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: my_http2_profile
    partition: Common
    description: My http2 profile
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
            activation_modes=dict(type="str", choices=["npn", "alpn", "always"]),
            app_service=dict(type="str"),
            concurrent_streams_per_connection=dict(type="int"),
            connection_idle_timeout=dict(type="int"),
            defaults_from=dict(type="str"),
            description=dict(type="str"),
            frame_size=dict(type="int"),
            header_table_size=dict(type="int"),
            insert_header=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            insert_header_name=dict(type="str"),
            receive_window=dict(type="int"),
            write_size=dict(type="int"),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpLtmProfileHttp2(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "create": self._api.tm.ltm.profile.http2s.http2.create,
            "read": self._api.tm.ltm.profile.http2s.http2.load,
            "update": self._api.tm.ltm.profile.http2s.http2.update,
            "delete": self._api.tm.ltm.profile.http2s.http2.delete,
            "exists": self._api.tm.ltm.profile.http2s.http2.exists,
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpLtmProfileHttp2(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
