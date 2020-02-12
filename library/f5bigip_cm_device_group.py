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
module: f5bigip_cm_device_group
short_description: BIG-IP cm device-group module
description:
    - Configures device groups.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Eric Jacob (@erjac77)"
options:
    asm_sync:
        description:
            - Specifies whether to synchronize ASM configurations of device group members.
        default: disabled
        choices: ['enabled', 'disabled']
    auto_sync:
        description:
            - Specifies whether the device group automatically synchronizes configuration data to its members.
        default: disabled
        choices: ['enabled', 'disabled']
    devices:
        description:
            - Manages the set of devices that are associated with a device group.
    full_load_on_sync:
        description:
            - Specifies that the entire configuration for a device group is sent when configuration synchronization is
              performed.
        default: false
        type: bool
    incremental_config_sync_size_max:
        description:
            - Specifies the maximum size (in KB) to devote to incremental config sync cached transactions.
        default: 1024
    network_failover:
        description:
            - When the device group type is failover, specifies whether network failover is used.
        default: enabled
        choices: ['enabled', 'disabled']
    save_on_auto_sync:
        description:
            - Specifies whether to save the configuration on the remote devices following an automatic configuration
              synchronization.
        default: false
        type: bool
    type:
        description:
            - Specifies the type of device group.
        default: sync-only
        choices: ['sync-only', 'sync-failover']
extends_documentation_fragment:
    - f5_common
    - f5_description
    - f5_name
    - f5_state
"""

EXAMPLES = """
- name: Create CM Device Group
  f5bigip_cm_device_group:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: my_device_group
    devices:
      - bigip01.localhost
      - bigip02.localhost
    network_failover: enabled
    type: sync-failover
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
            asm_sync=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            auto_sync=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            description=dict(type="str"),
            devices=dict(type=list),
            full_load_on_sync=dict(type="bool"),
            incremental_config_sync_size_max=dict(type="int"),
            network_failover=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            save_on_auto_sync=dict(type="bool"),
            type=dict(type="str", choices=["sync-only", "sync-failover"]),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        del argument_spec["partition"]
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpCmDeviceGroup(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "create": self._api.tm.cm.device_groups.device_group.create,
            "read": self._api.tm.cm.device_groups.device_group.load,
            "update": self._api.tm.cm.device_groups.device_group.update,
            "delete": self._api.tm.cm.device_groups.device_group.delete,
            "exists": self._api.tm.cm.device_groups.device_group.exists,
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpCmDeviceGroup(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
