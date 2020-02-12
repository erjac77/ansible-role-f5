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
module: f5bigip_ltm_monitor_snmp_dca_base
short_description: BIG-IP ltm monitor snmp dca base module
description:
    - Configures a base Simple Network Management Protocol (SNMP) Data Center Audit monitor.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Gabriel Fortin (@GabrielFortin)"
options:
    community:
        description:
            - Specifies the community name that the BIG-IP system must use to authenticate with the host server through
              SNMP.
        default: public
    cpu_coefficient:
        description:
            - Specifies the coefficient that the system uses to calculate the weight of the CPU threshold in the dynamic
              ratio load balancing algorithm.
        default: 1.5
    defaults_from:
        description:
            - Specifies the name of the monitor from which you want your custom monitor to inherit settings.
        default: snmp_dca_base
    interval:
        description:
            - Specifies the frequency at which the system issues the monitor check.
        default: 10
    time_until_up:
        description:
            - Specifies the amount of time, in seconds, after the first successful response before a node is marked up.
        default: 0
    timeout:
        description:
            - Specifies the number of seconds the target has in which to respond to the monitor request.
        default: 30
    user_defined:
        description:
            - Specifies any user-defined command-line arguments and variables that the external program requires.
    version:
        description:
            - Specifies the version of SNMP that the host server uses.
extends_documentation_fragment:
    - f5_common
    - f5_app_service
    - f5_description
    - f5_name
    - f5_partition
    - f5_state
"""

EXAMPLES = """
- name: Create LTM Monitor SNMP DCA Base
  f5bigip_ltm_monitor_snmp_dca_base:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: my_snmp_dca_base_monitor
    partition: Common
    description: My snmp dca base monitor
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
            app_service=dict(type="str"),
            community=dict(type="str"),
            cpu_coefficient=dict(type="int"),
            defaults_from=dict(type="str"),
            description=dict(type="str"),
            interval=dict(type="int"),
            time_until_up=dict(type="int"),
            timeout=dict(type="int"),
            user_defined=dict(type="str"),
            version=dict(type="int"),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpLtmMonitorSnmpDcaBase(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "create": self._api.tm.ltm.monitor.snmp_dca_bases.snmp_dca_base.create,
            "read": self._api.tm.ltm.monitor.snmp_dca_bases.snmp_dca_base.load,
            "update": self._api.tm.ltm.monitor.snmp_dca_bases.snmp_dca_base.update,
            "delete": self._api.tm.ltm.monitor.snmp_dca_bases.snmp_dca_base.delete,
            "exists": self._api.tm.ltm.monitor.snmp_dca_bases.snmp_dca_base.exists,
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpLtmMonitorSnmpDcaBase(
            check_mode=module.check_mode, **module.params
        )
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
