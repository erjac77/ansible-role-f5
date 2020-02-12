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
module: f5bigip_ltm_monitor_sip
short_description: BIG-IP ltm monitor sip module
description:
    - Configures a Session Initiation Protocol (SIP) monitor.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Gabriel Fortin (@GabrielFortin)"
options:
    cert:
        description:
            - Specifies a fully-qualified path for a client certificate that the monitor sends to the target SSL server.
    cipherlist:
        description:
            - Specifies the list of ciphers for this monitor.
        default: DEFAULT:+SHA:+3DES:+kEDH
    compatibility:
        description:
            - Specifies, when enabled, that the SSL options setting (in OpenSSL) is set to ALL.
        default: enabled
        choices: ['disabled', 'enabled']
    debug:
        description:
            - Specifies whether the monitor sends error messages and additional information to a log file created and
              labeled specifically for this monitor.
        default: no
        choices: ['no', 'yes']
    defaults_from:
        description:
            - Specifies the name of the monitor from which you want your custom monitor to inherit settings.
        default: sip
    destination:
        description:
            - Specifies the IP address and service port of the resource that is the destination of this monitor.
    filter:
        description:
            - Specifies the SIP status codes that the target can return to be considered up.
        choices: ['any', 'none', 'status']
    filter_neg:
        description:
            - Specifies the SIP status codes that the target can return to be considered down.
        choices: ['any', 'none', 'status']
    headers:
        description:
            - Specifies the set of SIP headers in the SIP message that is sent to the target
    interval:
        description:
            - Specifies, in seconds, the frequency at which the system issues the monitor check when either the resource
              is down or the status of the resource is unknown.
        default: 5
    key:
        description:
            - Specifies the key if the monitored target requires authentication
    manual_resume:
        description:
            - Specifies whether the system automatically changes the status of a resource to up at the next successful
              monitor check.
        default: disabled
        choices: ['disabled', 'enabled']
    mode:
        description:
            - Specifies the protocol that the monitor uses to communicate with the target.
        default: udp
        choices: ['sips', 'tcp', 'tls', 'udp']
    request:
        description:
            - Specifies the SIP request line in the SIP message that is sent to the target.
    time_until_up:
        description:
            - Specifies the amount of time, in seconds, after the first successful response before a node is marked up.
    up_interval:
        description:
            - Specifies, in seconds, the frequency at which the system issues the monitor check when the resource is up.
        default: 0
    username:
        description:
            - Specifies the username, if the monitored target requires authentication.
extends_documentation_fragment:
    - f5_common
    - f5_app_service
    - f5_description
    - f5_name
    - f5_partition
    - f5_state
"""

EXAMPLES = """
- name: Create LTM Monitor SIP
  f5bigip_ltm_monitor_sip:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: my_sip_monitor
    partition: Common
    description: My sip monitor
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
            cert=dict(type="str"),
            cipherlist=dict(type="list"),
            compatibility=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            debug=dict(type="str", choices=F5_POLAR_CHOICES),
            defaults_from=dict(type="str"),
            description=dict(type="str"),
            destination=dict(type="str"),
            filter=dict(type="str", choices=["any", "none", "status"]),
            filter_neg=dict(type="str", choices=["any", "none", "status"]),
            headers=dict(type="str"),
            interval=dict(type="int"),
            key=dict(type="str"),
            manual_resume=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            mode=dict(type="str", choices=["sips", "tcp", "tls", "udp"]),
            request=dict(type="str"),
            time_until_up=dict(type="int"),
            up_interval=dict(type="int"),
            username=dict(type="str"),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpLtmMonitorSip(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "create": self._api.tm.ltm.monitor.sips.sip.create,
            "read": self._api.tm.ltm.monitor.sips.sip.load,
            "update": self._api.tm.ltm.monitor.sips.sip.update,
            "delete": self._api.tm.ltm.monitor.sips.sip.delete,
            "exists": self._api.tm.ltm.monitor.sips.sip.exists,
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpLtmMonitorSip(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
