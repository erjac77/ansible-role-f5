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
module: f5bigip_net_route
short_description: BIG-IP net route module
description:
    - Configures a route for traffic management.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Eric Jacob (@erjac77)"
options:
    blackhole:
        description:
            - Specifies that the system drops traffic that is addressed to the specified destination.
    gw:
        description:
            - Specifies a gateway address for the system.
    interface:
        description:
            - Specifies the tunnel, VLAN or VLAN group to which the system sends traffic.
    mtu:
        description:
            - Sets a specific maximum transition unit (MTU).
    network:
        description:
            - Specifies the destination subnet and mask using CIDR notation.
    pool:
        description:
            - Specifies a pool to which the system sends traffic.
extends_documentation_fragment:
    - f5_common
    - f5_description
    - f5_name
    - f5_partition
    - f5_state
"""

EXAMPLES = """
- name: Create NET Route
  f5bigip_net_route:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: my_route
    partition: Common
    network: 10.0.0.0/8
    gw: 10.10.20.1
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
            blackhole=dict(type="bool"),
            description=dict(type="str"),
            gw=dict(type="str"),
            interface=dict(type="str"),
            mtu=dict(type="int"),
            network=dict(type="str"),
            pool=dict(type="str"),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True

    @property
    def mutually_exclusive(self):
        return [["blackhole", "gw", "interface", "pool"]]


class F5BigIpNetRoute(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "create": self._api.tm.net.routes.route.create,
            "read": self._api.tm.net.routes.route.load,
            "update": self._api.tm.net.routes.route.update,
            "delete": self._api.tm.net.routes.route.delete,
            "exists": self._api.tm.net.routes.route.exists,
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
        mutually_exclusive=params.mutually_exclusive,
    )

    try:
        obj = F5BigIpNetRoute(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
