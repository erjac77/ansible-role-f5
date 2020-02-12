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
module: f5bigip_ltm_monitor_diameter
short_description: BIG-IP ltm monitor diameter module
description:
    - Configures a monitor for Diameter protocol resources.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Gabriel Fortin (@GabrielFortin)"
options:
    acct_application_id:
        description:
            - Specifies the ID of the accounting portion of a Diameter application.
    auth_application_id:
        description:
            - Specifies the ID of the authentication and authorization portion of a Diameter application.
    defaults_from:
        description:
            - Specifies the name of the monitor from which you want your custom monitor to inherit settings.
        default: diameter
    host_ip_address:
        description:
            - Specifies the IP address of the sender of the Diameter message for the Diameter protocol peer discovery
              feature.
    interval:
        description:
            - Specifies, in seconds, the frequency at which the system issues the monitor check when either the resource
              is down or the status of the resource is unknown.
        default: 10
    manual_resume:
        description:
            - Specifies whether the system automatically changes the status of a resource to up at the next successful
              monitor check.
        default: disabled
        choices: ['enabled', 'disabled']
    origin_host:
        description:
            - Specifies the IP address from which the Diameter message originates.
    origin_realm:
        description:
            - Specifies the realm in which the host from which the Diameter message originates resides.
        default: f5.com
    product_name:
        description:
            - Specifies the vendor-assigned name of the Diameter application.
        default: F5 BIGIP Diameter Health Monitoring
    time_until_up:
        description:
            - Specifies the amount of time, in seconds, after the first successful response before a node is marked up.
        default: 0
    timeout:
        description:
            - Specifies the number of seconds the target has in which to respond to the monitor request.
        default: 31
    up_interval:
        description:
            - Specifies, in seconds, the frequency at which the system issues the monitor check when the resource is up.
        default: 0
    vendor_id:
        description:
            - Specifies the IANA SMI Network Management Private Enterprise Code assigned to the vendor of the Diameter
              application.
        default: 3375
    vendor_specific_acct_application_id:
        description:
            - Specifies Specifies the ID of the vendor-specific accounting portion of a Diameter application.
    vendor_specific_auth_application_id:
        description:
            - Specifies the ID of the vendor-specific authentication and authorization portion of a Diameter
              application.
    vendor_specific_vendor_id:
        description:
            - Specifies the ID of a vendor-specific Diameter application.
extends_documentation_fragment:
    - f5_common
    - f5_app_service
    - f5_description
    - f5_name
    - f5_partition
    - f5_state
"""

EXAMPLES = """
- name: Create LTM Monitor Diameter
  f5bigip_ltm_monitor_diameter:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: my_diameter_monitor
    partition: Common
    description: My diameter monitor
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
            acct_application_id=dict(type="int"),
            app_service=dict(type="str"),
            auth_application_id=dict(type="int"),
            defaults_from=dict(type="str"),
            description=dict(type="str"),
            host_ip_address=dict(type="str"),
            interval=dict(type="int"),
            manual_resume=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            origin_host=dict(type="str"),
            origin_realm=dict(type="str"),
            product_name=dict(type="str"),
            time_until_up=dict(type="int"),
            timeout=dict(type="int"),
            up_interval=dict(type="int"),
            vendor_id=dict(type="int"),
            vendor_specific_acct_application_id=dict(type="int"),
            vendor_specific_auth_application_id=dict(type="int"),
            vendor_specific_vendor_id=dict(type="int"),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpLtmMonitorDiameter(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "create": self._api.tm.ltm.monitor.diameters.diameter.create,
            "read": self._api.tm.ltm.monitor.diameters.diameter.load,
            "update": self._api.tm.ltm.monitor.diameters.diameter.update,
            "delete": self._api.tm.ltm.monitor.diameters.diameter.delete,
            "exists": self._api.tm.ltm.monitor.diameters.diameter.exists,
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpLtmMonitorDiameter(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
