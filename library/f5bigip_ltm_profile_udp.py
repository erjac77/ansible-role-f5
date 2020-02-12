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
module: f5bigip_ltm_profile_udp
short_description: BIG-IP ltm profile udp module
description:
    - Configures a User Datagram Protocol (UDP) profile.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Gabriel Fortin (@GabrielFortin)"
options:
    allow_no_payload:
        description:
            - Provides the ability to allow the passage of datagrams that contain header information, but no essential
              data.
        default: disabled
        choices: ['disabled', 'enabled']
    datagram_load_balancing:
        description:
            - Provides the ability to load balance UDP datagram by datagram.
        default: disabled
        choices: ['disabled', 'enabled']
    defaults_from:
        description:
            - Specifies the profile that you want to use as the parent profile.
        default: udp
    idle_timeout:
        description:
            - Specifies the number of seconds that a connection is idle before the connection is eligible for deletion.
        default: 60
    ip_tos_to_client:
        description:
            - Specifies the Type of Service level that the traffic management system assigns to UDP packets when sending
              them to clients.
    link_qos_to_client:
        description:
            - Specifies the Quality of Service level that the system assigns to UDP packets when sending them to
              clients.
        default: 0
    no_checksum:
        description:
            - Enables or disables checksum processing.
        default: disabled
        choices: ['disabled', 'enabled']
    proxy_mss:
        description:
            - Specifies, when enabled, that the system advertises the same mss to the server as was negotiated with the
              client.
        default: disabled
        choices: ['disabled', 'enabled']
extends_documentation_fragment:
    - f5_common
    - f5_app_service
    - f5_description
    - f5_name
    - f5_partition
    - f5_state
"""

EXAMPLES = """
- name: Create LTM Profile UDP
  f5bigip_ltm_profile_udp:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: my_udp_profile
    partition: Common
    description: My udp profile
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
            allow_no_payload=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            app_service=dict(type="str"),
            datagram_load_balancing=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            defaults_from=dict(type="str"),
            description=dict(type="str"),
            idle_timeout=dict(type="int"),
            ip_tos_to_client=dict(type="int"),
            link_qos_to_client=dict(type="int"),
            no_checksum=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            proxy_mss=dict(type="str", choices=F5_ACTIVATION_CHOICES),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpLtmProfileUdp(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "create": self._api.tm.ltm.profile.udps.udp.create,
            "read": self._api.tm.ltm.profile.udps.udp.load,
            "update": self._api.tm.ltm.profile.udps.udp.update,
            "delete": self._api.tm.ltm.profile.udps.udp.delete,
            "exists": self._api.tm.ltm.profile.udps.udp.exists,
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpLtmProfileUdp(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
