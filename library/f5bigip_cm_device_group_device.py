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
module: f5bigip_cm_device_group_device
short_description: BIG-IP cm device-group device module
description:
    - Configures a set of devices to the device group.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Eric Jacob (@erjac77)"
options:
    device_group:
        description:
            - Specifies the device group in which the device belongs.
        required: true
extends_documentation_fragment:
    - f5_common
    - f5_description
    - f5_name
    - f5_state
"""

EXAMPLES = """
- name: Add CM Device Group member
  f5bigip_cm_device_group_device:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: bigip01.localhost
    device_group: my_device_group
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
        argument_spec = dict(device_group=dict(type="str"))
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        del argument_spec["partition"]
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpCmDeviceGroupDevice(F5BigIpNamedObject):
    def _set_crud_methods(self):
        device_group = self._api.tm.cm.device_groups.device_group.load(
            name=self._params["deviceGroup"]
        )
        self._methods = {
            "create": device_group.devices_s.devices.create,
            "read": device_group.devices_s.devices.load,
            "update": device_group.devices_s.devices.update,
            "delete": device_group.devices_s.devices.delete,
            "exists": device_group.devices_s.devices.exists,
        }
        del self._params["deviceGroup"]


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpCmDeviceGroupDevice(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
