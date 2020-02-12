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
module: f5bigip_gtm_monitor_bigip
short_description: BIG-IP gtm bigip monitor module
description:
    - Configures a BIG-IP monitor.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Eric Jacob (@erjac77)"
options:
    aggregate_dynamic_ratios:
        description:
            - Specifies the monitor's response to a query. By default, the BIG-IP monitor uses the gtm_score value as
              the vs_score for a Local Traffic Manager virtual server.
        default: none
        choices: ['average-members', 'average-nodes', 'none', 'sum-members', 'sum-nodes']
    defaults_from:
        description:
            - Specifies the name of the monitor from which you want your custom monitor to inherit settings.
        default: bigip
    destination:
        description:
            - Specifies the IP address and service port of the resource that is the destination of this monitor.
        default: '*:*'
    ignore_down_response:
        description:
            - Specifies whether the monitor ignores a down response from the system it is monitoring.
        default: disabled
        choices: ['disabled', 'enabled']
    interval:
        description:
            - Specifies the frequency at which the system issues the monitor check.
        default: 30
    timeout:
        description:
            - Specifies the number of seconds the target has in which to respond to the monitor request.
        default: 90
extends_documentation_fragment:
    - f5_common
    - f5_app_service
    - f5_description
    - f5_name
    - f5_partition
    - f5_state
"""

EXAMPLES = """
- name: Create GTM BIG-IP Monitor
  f5bigip_gtm_monitor_bigip:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: my_bigip_monitor
    partition: Common
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
            aggregate_dynamic_ratios=dict(
                type="str",
                choices=[
                    "average-members",
                    "average-nodes",
                    "none",
                    "sum-members",
                    "sum-nodes",
                ],
            ),
            app_service=dict(type="str"),
            defaults_from=dict(type="str"),
            description=dict(type="str"),
            destination=dict(type="str"),
            ignore_down_response=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            interval=dict(type="int"),
            timeout=dict(type="int"),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpGtmMonitorBigip(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "create": self._api.tm.gtm.monitor.bigips.bigip.create,
            "read": self._api.tm.gtm.monitor.bigips.bigip.load,
            "update": self._api.tm.gtm.monitor.bigips.bigip.update,
            "delete": self._api.tm.gtm.monitor.bigips.bigip.delete,
            "exists": self._api.tm.gtm.monitor.bigips.bigip.exists,
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpGtmMonitorBigip(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
