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
module: f5bigip_net_route_domain
short_description: BIG-IP net route-domain module
description:
    - Configures route-domains for traffic management.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Eric Jacob (@erjac77)"
options:
    bwc_policy:
        description:
            - Configures the bandwidth control policy for the route-domain.
    connection_limit:
        description:
            - Configures the connection limit for the route domain.
        default: 0
    flow_eviction_policy:
        description:
            - Specifies a flow eviction policy for the route domain to use, to select which flows to evict when the
              number of connections approaches the connection limit on the route domain.
    id:
        description:
            - Specifies a unique numeric identifier for the route-domain.
    parent:
        description:
            - Specifies the route domain the system searches when it cannot find a route in the configured domain.
    strict:
        description:
            - Specifies whether the system allows a connection to span route domains.
        default: enabled
        choices: ['disabled', 'enabled']
    vlans:
        description:
            - Specifies VLANs, by name, for the system to use in the route domain.
extends_documentation_fragment:
    - f5_common
    - f5_app_service
    - f5_description
    - f5_name
    - f5_partition
    - f5_state
"""

EXAMPLES = """
- name: Create NET Route-Domain
  f5bigip_net_route_domain:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: my_route_domain
    partition: Common
    id: 1234
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
            bwc_policy=dict(type="str"),
            connection_limit=dict(type="int"),
            description=dict(type="str"),
            flow_eviction_policy=dict(type="str"),
            fw_enforced_policy=dict(type="str"),
            # fw_rules=dict(type='list'),
            fw_staged_policy=dict(type="str"),
            id=dict(type="int"),
            parent=dict(type="str"),
            routing_protocol=dict(type="list"),
            strict=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            vlans=dict(type="list"),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpNetRouteDomain(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "create": self._api.tm.net.route_domains.route_domain.create,
            "read": self._api.tm.net.route_domains.route_domain.load,
            "update": self._api.tm.net.route_domains.route_domain.update,
            "delete": self._api.tm.net.route_domains.route_domain.delete,
            "exists": self._api.tm.net.route_domains.route_domain.exists,
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpNetRouteDomain(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
