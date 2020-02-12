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
module: f5bigip_ltm_monitor_soap
short_description: BIG-IP ltm monitor soap module
description:
    - Configures a Simple Object Access Protocol (SOAP) monitor.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Gabriel Fortin (@GabrielFortin)"
options:
    debug:
        description:
            - Specifies whether the monitor sends error messages and additional information to a log file created and
              labeled specifically for this monitor.
        default: no
        choices: ['no', 'yes']
    defaults_from:
        description:
            - Specifies the type of monitor you want to use to create the new monitor.
        default: soap
    destination:
        description:
            - Specifies the IP address and service port of the resource that is the destination of this monitor.
    expect_fault:
        description:
            - Specifies whether the value of the method option causes the monitor to expect a SOAP fault message.
        default: no
        choices: ['no', 'yes']
    interval:
        description:
            - Specifies, in seconds, the frequency at which the system issues the monitor check when either the resource
              is down or the status of the resource is unknown.
        default: 5
    manual_resume:
        description:
            - Specifies whether the system automatically changes the status of a resource to up at the next successful
              monitor check.
        default: disabled
        choices: ['disabled', 'enabled']
    method:
        description:
            - Specifies the method by which the monitor contacts the resource.
    namespace:
        description:
            - Specifies the name space for the Web service you are monitoring, for example, http://example.com/.
    parameter_name:
        description:
            - If the method has a parameter, specifies the name of that parameter.
    parameter_type:
        description:
            - Specifies the parameter type.
        default: bool
        choices: ['bool', 'int', 'long', 'string']
    parameter_value:
        description:
            - Specifies the value for the parameter.
    password:
        description:
            - Specifies the password if the monitored target requires authentication.
    protocol:
        description:
            - Specifies the protocol that the monitor uses to communicate with the target, http or https.
        default: http
        choices: ['http', 'https']
    return_type:
        description:
            - ['bool', 'char', 'double', 'int', 'long', 'short', 'string']
        default: bool
    return_value:
        description:
            - Specifies the value for the returned parameter.
    soap_action:
        description:
            - Specifies the value for the SOAPAction header.
        default: ''
    time_until_up:
        description:
            - Specifies the amount of time, in seconds, after the first successful response before a node is marked up.
        default: 0
    timeout:
        description:
            - Specifies the number of seconds the target has in which to respond to the monitor request.
        default: 16
    up_interval:
        description:
            - Specifies, in seconds, the frequency at which the system issues the monitor check when the resource is up.
        default: 0
    url_path:
        description:
            - Specifies the URL for the Web service that you are monitoring, for example, /services/myservice.aspx.
    username:
        description:
            - Specifies the user name if the monitored target requires authentication.
extends_documentation_fragment:
    - f5_common
    - f5_app_service
    - f5_description
    - f5_name
    - f5_partition
    - f5_state
"""

EXAMPLES = """
- name: Create LTM Monitor SOAP
  f5bigip_ltm_monitor_soap:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: my_soap_monitor
    partition: Common
    description: My soap monitor
    state: present
  delegate_to: localhost
"""

RETURN = """ # """

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.erjac77.network.f5.common import F5_ACTIVATION_CHOICES
from ansible.module_utils.erjac77.network.f5.common import F5_NAMED_OBJ_ARGS
from ansible.module_utils.erjac77.network.f5.common import F5_POLAR_CHOICES
from ansible.module_utils.erjac77.network.f5.common import F5_PROVIDER_ARGS
from ansible.module_utils.erjac77.network.f5.bigip import F5BigIpNamedObject


class ModuleParams(object):
    @property
    def argument_spec(self):
        argument_spec = dict(
            app_service=dict(type="str"),
            debug=dict(type="str", choices=F5_POLAR_CHOICES),
            defaults_from=dict(type="str"),
            description=dict(type="str"),
            destination=dict(type="str"),
            expect_fault=dict(type="str", choices=F5_POLAR_CHOICES),
            interval=dict(type="int"),
            manual_resume=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            method=dict(type="str"),
            namespace=dict(type="str"),
            parameter_name=dict(type="str"),
            parameter_type=dict(type="str", choices=["bool", "int", "long", "string"]),
            parameter_value=dict(type="str"),
            password=dict(type="str", no_log=True),
            protocol=dict(type="str", choices=["http", "https"]),
            return_type=dict(
                type="str",
                choices=["bool", "char", "double", "int", "long", "short", "string"],
            ),
            return_value=dict(type="str"),
            soap_action=dict(type="str"),
            time_until_up=dict(type="int"),
            timeout=dict(type="int"),
            up_interval=dict(type="int"),
            url_path=dict(type="str"),
            username=dict(type="str"),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpLtmMonitorSoap(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "create": self._api.tm.ltm.monitor.soaps.soap.create,
            "read": self._api.tm.ltm.monitor.soaps.soap.load,
            "update": self._api.tm.ltm.monitor.soaps.soap.update,
            "delete": self._api.tm.ltm.monitor.soaps.soap.delete,
            "exists": self._api.tm.ltm.monitor.soaps.soap.exists,
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpLtmMonitorSoap(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
