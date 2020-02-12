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
module: f5bigip_cm_device
short_description: BIG-IP cm device module
description:
    - Manages a device.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Eric Jacob (@erjac77)"
options:
    comment:
        description:
            - Specifies user comments about the device.
    configsync_ip:
        description:
            - Specifies the IP address used for configuration synchronization.
    contact:
        description:
            - Specifies administrator contact information.
    ha_capacity:
        description:
            - Specifies a number that represents the relative capacity of the device to be active for a number of
              traffic groups.
        default: 0
        choices: range(0, 100000)
    hostname:
        description:
            - Specifies a hostname for the device.
    location:
        description:
            - Specifies the physical location of the device.
    mirror_ip:
        description:
            - Specifies the IP address used for state mirroring.
    mirror_secondary_ip:
        description:
            - Specifies the secondary IP address used for state mirroring.
    multicast_interface:
        description:
            - Specifies the interface name used for the failover multicast IP address.
    multicast_ip:
        description:
            - Specifies the multicast IP address used for failover.
    multicast_port:
        description:
            - Specifies the multicast port used for failover.
    unicast-address:
        description:
            - Displays the set of unicast IP addresses used for failover.
extends_documentation_fragment:
    - f5_common
    - f5_description
    - f5_name
    - f5_state
"""

EXAMPLES = """
- name: Configure CM Device Properties
  f5bigip_cm_device:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: bigip01.localhost
    comment: My lab device
    configsync_ip: 10.10.30.11
    contact: 'admin@localhost'
    description: My device
    location: Central Office
    mirror_ip: 10.10.30.11
    mirror_secondary_ip: 10.10.10.11
    multicast_interface: eth0
    multicast_ip: 224.0.0.245
    multicast_port: 62960
    unicast_address:
      - { ip: 10.10.30.11, port: 1026 }
      - { ip: 10.10.20.11, port: 1026 }
    state: present
  delegate_to: localhost
"""

RETURN = """ # """

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six.moves import range
from ansible.module_utils.erjac77.network.f5.common import F5_NAMED_OBJ_ARGS
from ansible.module_utils.erjac77.network.f5.common import F5_PROVIDER_ARGS
from ansible.module_utils.erjac77.network.f5.bigip import F5BigIpNamedObject


class ModuleParams(object):
    @property
    def argument_spec(self):
        argument_spec = dict(
            comment=dict(type="str"),
            configsync_ip=dict(type="str"),
            contact=dict(type="str"),
            description=dict(type="str"),
            ha_capacity=dict(type="int", choices=range(0, 100000)),
            hostname=dict(type="str"),
            location=dict(type="str"),
            mirror_ip=dict(type="str"),
            mirror_secondary_ip=dict(type="str"),
            multicast_interface=dict(type="str"),
            multicast_ip=dict(type="str"),
            multicast_port=dict(type="int"),
            unicast_address=dict(type="list"),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        del argument_spec["partition"]
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpCmDevice(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "create": self._api.tm.cm.devices.device.create,
            "read": self._api.tm.cm.devices.device.load,
            "update": self._api.tm.cm.devices.device.update,
            "delete": self._api.tm.cm.devices.device.delete,
            "exists": self._api.tm.cm.devices.device.exists,
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpCmDevice(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
