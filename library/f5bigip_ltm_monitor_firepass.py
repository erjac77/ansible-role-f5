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
module: f5bigip_ltm_monitor_firepass
short_description: BIG-IP ltm monitor firepass module
description:
    - Configures a FirePass monitor.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Gabriel Fortin (@GabrielFortin)"
options:
    cipherlist:
        description:
            - Specifies the list of ciphers for this monitor.
        default: HIGH:!ADH
    concurrency_limit:
        description:
            - Specifies the maximum percentage of licensed connections currently in use under which the monitor marks
              the FirePass system up.
        default: 95
    defaults_from:
        description:
            - Specifies the name of the monitor from which you want your custom monitor to inherit settings.
        default: firepass
    destination:
        description:
            - Specifies the IP address and service port of the resource that is the destination of this monitor.
    interval:
        description:
            - Specifies, in seconds, the frequency at which the system issues the monitor check when either the resource
              is down or the status of the resource is unknown.
        default: 5
    max_load_average:
        description:
            - Specifies the number that the monitor uses to mark the FirePass system up or down.
        default: 12.0
    password:
        description:
            - Specifies the password, if the monitored target requires authentication.
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
    username:
        description:
            - Specifies the username, if the monitored target requires authentication.
        default: gtmuser
extends_documentation_fragment:
    - f5_common
    - f5_app_service
    - f5_description
    - f5_name
    - f5_partition
    - f5_state
"""

EXAMPLES = """
- name: Create LTM Monitor Firepass
  f5bigip_ltm_monitor_firepass:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: my_firepass_monitor
    partition: Common
    description: My firepass monitor
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
            cipherlist=dict(type="list"),
            concurrency_limit=dict(type="int"),
            defaults_from=dict(type="str"),
            description=dict(type="str"),
            destination=dict(type="str"),
            interval=dict(type="int"),
            max_load_average=dict(type="int"),
            password=dict(type="str", no_log=True),
            time_until_up=dict(type="int"),
            timeout=dict(type="int"),
            up_interval=dict(type="int"),
            username=dict(type="str"),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpLtmMonitorFirepass(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "create": self._api.tm.ltm.monitor.firepass_s.firepass.create,
            "read": self._api.tm.ltm.monitor.firepass_s.firepass.load,
            "update": self._api.tm.ltm.monitor.firepass_s.firepass.update,
            "delete": self._api.tm.ltm.monitor.firepass_s.firepass.delete,
            "exists": self._api.tm.ltm.monitor.firepass_s.firepass.exists,
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpLtmMonitorFirepass(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
