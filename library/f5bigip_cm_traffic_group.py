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
module: f5bigip_cm_traffic_group
short_description: BIG-IP cm traffic-group module
description:
    - Manages a traffic group.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Eric Jacob (@erjac77)"
options:
    auto_failback_enabled:
        description:
            - Specifies whether the traffic group fails back to the default device.
        default: disabled
        choices: ['enabled', 'disabled']
    auto_failback_time:
        description:
            - Specifies the time required to fail back.
        default: 0
    ha_group:
        description:
            - This specifies the name of the HA group that the traffic group uses to decide the active device within the
              traffic group.
    ha_load_factor:
        description:
            - Specifies a number for this traffic group that represents the load this traffic group presents to the
              system relative to other traffic groups.
        default: 1
    ha_order:
        description:
            - This list of devices specifies the order in which the devices will become active for the traffic group
              when a failure occurs.
    mac:
        description:
            - Specifies a MAC address for the traffic group.
extends_documentation_fragment:
    - f5_common
    - f5_app_service
    - f5_description
    - f5_name
    - f5_partition
    - f5_state
"""

EXAMPLES = """
- name: Create CM Traffic Group
  f5bigip_cm_traffic_group:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: my_traffic_group
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
            auto_failback_enabled=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            auto_failback_time=dict(type="int"),
            description=dict(type="str"),
            ha_group=dict(type="str"),
            ha_load_factor=dict(type="int"),
            ha_order=dict(type="list"),
            mac=dict(type="str"),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpCmTrafficGroup(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "create": self._api.tm.cm.traffic_groups.traffic_group.create,
            "read": self._api.tm.cm.traffic_groups.traffic_group.load,
            "update": self._api.tm.cm.traffic_groups.traffic_group.update,
            "delete": self._api.tm.cm.traffic_groups.traffic_group.delete,
            "exists": self._api.tm.cm.traffic_groups.traffic_group.exists,
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpCmTrafficGroup(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
