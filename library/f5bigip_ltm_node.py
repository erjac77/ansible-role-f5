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
module: f5bigip_ltm_node
short_description: BIG-IP ltm node module
description:
    - Configures node addresses and services.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Eric Jacob (@erjac77)"
options:
    address:
        description:
            - Specifies the IP address for the node.
        required: true
    connection_limit:
        description:
            - Specifies the maximum number of connections that a node or node address can handle.
        default: 0
    dynamic_ratio:
        description:
            - Sets the dynamic ratio number for the node.
        default: 1
    fqdn:
        description:
            - Specifies the attributes for defining a fully qualified domain name for the node.
    logging:
        description:
            - Specifies whether the monitor applied should log its actions.
        default: disabled
        choices: ['enabled', 'disabled']
    metadata:
        description:
            - Associates user defined data, each of which has a name and value pair and persistence.
        default: persistent
    monitor:
        description:
            - Specifies the monitors that the BIG-IP system is to associate with the node.
    rate_limit:
        description:
            - Specifies the maximum number of connections per second allowed for a node or node address.
        default: disabled (or 0)
    ratio:
        description:
            - Specifies the fixed ratio value used for a node during Ratio load balancing.
        default: 1
    session:
        description:
            - Specifies the ability of the client to persist to the node when making new connections.
        default: user-enabled
        choices: ['user-enabled', 'user-disabled']
    state_user:
        description:
            - Specifies the current state of the node.
        default: user-up
        choices: ['user-down', 'user-up']
extends_documentation_fragment:
    - f5_common
    - f5_app_service
    - f5_description
    - f5_name
    - f5_partition
    - f5_state
"""

EXAMPLES = """
- name: Create LTM Node
  f5bigip_ltm_node:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: my_node
    partition: Common
    description: My node
    address: 10.10.10.101
    monitor: /Common/icmp
    state: present
  delegate_to: localhost

- name: Force LTM Node Offline
  f5bigip_ltm_node:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: my_node
    partition: Common
    session: user-disabled
    state_user: user-down
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
            address=dict(type="str"),
            app_service=dict(type="str"),
            connection_limit=dict(type="int"),
            description=dict(type="str"),
            dynamic_ratio=dict(type="int"),
            fqdn=dict(type="str"),
            logging=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            metadata=dict(type="list"),
            monitor=dict(type="str"),
            rate_limit=dict(type="str"),
            ratio=dict(type="int"),
            session=dict(type="str", choices=["user-enabled", "user-disabled"]),
            state_user=dict(type="str", choices=["user-down", "user-up"]),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True

    @property
    def tr(self):
        # Translation dict for conflictual params
        return {"state_user": "state"}


class F5BigIpLtmNode(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "create": self._api.tm.ltm.nodes.node.create,
            "read": self._api.tm.ltm.nodes.node.load,
            "update": self._api.tm.ltm.nodes.node.update,
            "delete": self._api.tm.ltm.nodes.node.delete,
            "exists": self._api.tm.ltm.nodes.node.exists,
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpLtmNode(
            check_mode=module.check_mode, tr=params.tr, **module.params
        )
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
