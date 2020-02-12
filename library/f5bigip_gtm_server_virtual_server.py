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
module: f5bigip_gtm_server_virtual_server
short_description: BIG-IP gtm server virtual-server module
description:
    - Configures a virtual servers.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Eric Jacob (@erjac77)"
options:
    depends_on:
        description:
            - Specifies the vs-name of the server on which this virtual server depends.
    destination:
        description:
            - Specifies the IP address and port of the virtual server.
    disabled:
        description:
            - Specifies whether the data center and its resources are available for load balancing.
        default: false
    enabled:
        description:
            - Specifies whether the data center and its resources are available for load balancing.
        default: true
    explicit_link_name:
        description:
            - Specifies the explicit link name for the virtual server.
    limit_max_bps:
        description:
            - Specifies the maximum allowable data throughput rate, in bits per second, for this server.
        default: 0
    limit_max_bps_status:
        description:
            - Enables or disables the limit-max-bps option for this virtual server.
        default: disabled
        choices: ['disabled', 'enabled']
    limit_max_connections:
        description:
            - Specifies the number of current connections allowed for this virtual server.
        default: 0
    limit_max_connections_status:
        description:
            - Enables or disables the limit-max-connections option for this virtual server.
        default: disabled
        choices: ['disabled', 'enabled']
    limit_max_pps:
        description:
            - Specifies the maximum allowable data transfer rate, in packets per second, for this virtual server.
        default: 0
    limit_max_pps_status:
        description:
            - Enables or disables the limit-max-pps option for this virtual server.
        default: disabled
        choices: ['disabled', 'enabled']
    ltm_name:
        description:
            - The virtual server name found on the LTM.
    monitor:
        description:
            - Specifies the monitor you want to assign to this virtual server.
    server:
        description:
            - Specifies the server in which the virtual-server belongs.
        required: true
    translation_address:
        description:
            - Specifies the public address that this virtual server translates into when the Global Traffic Manager
              communicates between the network and the Internet.
        default: '::'
    translation_port:
        description:
            - Specifies the translation port number or service name for the virtual server, if necessary.
        default: 0
extends_documentation_fragment:
    - f5_common
    - f5_app_service
    - f5_description
    - f5_name
    - f5_state
"""

EXAMPLES = """
- name: Create GTM Server VS
  f5bigip_gtm_server_virtual_server:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: my_vs
    destination: '10.10.20.201:80'
    server: my_server
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
            depends_on=dict(type="list"),
            description=dict(type="str"),
            destination=dict(type="str"),
            disabled=dict(type="bool"),
            enabled=dict(type="bool"),
            explicit_link_name=dict(type="str"),
            limit_max_bps=dict(type="int"),
            limit_max_bps_status=dict(type="str", choices=[F5_ACTIVATION_CHOICES]),
            limit_max_connections=dict(type="int"),
            limit_max_connections_status=dict(
                type="str", choices=[F5_ACTIVATION_CHOICES]
            ),
            limit_max_pps=dict(type="int"),
            limit_max_pps_status=dict(type="str", choices=[F5_ACTIVATION_CHOICES]),
            ltm_name=dict(type="str"),
            monitor=dict(type="str"),
            server=dict(type="str"),
            translation_address=dict(type="str"),
            translation_port=dict(type="str"),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        del argument_spec["partition"]
        return argument_spec

    @property
    def supports_check_mode(self):
        return True

    @property
    def mutually_exclusive(self):
        return [["disabled", "enabled"]]


class F5BigIpGtmServerVirtualServer(F5BigIpNamedObject):
    def _set_crud_methods(self):
        server = self._api.tm.gtm.servers.server.load(
            **self._get_resource_id_from_path(self._params["server"])
        )
        self._methods = {
            "create": server.virtual_servers_s.virtual_server.create,
            "read": server.virtual_servers_s.virtual_server.load,
            "update": server.virtual_servers_s.virtual_server.update,
            "delete": server.virtual_servers_s.virtual_server.delete,
            "exists": server.virtual_servers_s.virtual_server.exists,
        }
        del self._params["server"]


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
        mutually_exclusive=params.mutually_exclusive,
    )

    try:
        obj = F5BigIpGtmServerVirtualServer(
            check_mode=module.check_mode, **module.params
        )
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
