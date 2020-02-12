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
module: f5bigip_ltm_profile_rtsp
short_description: BIG-IP ltm profile rtsp module
description:
    - Configures an RTSP (realtime streaming protocol) profile.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Gabriel Fortin (@GabrielFortin)"
options:
    check_source:
        description:
            - When enabled the system uses the source attribute in the transport header to establish the target address
              of the RTP stream, and before the response is forwarded to the client, updates the value of the source
              attribute to be the virtual address of the BIG-IP system.
        default: enabled
        choices: ['disabled', 'enabled']
    defaults_from:
        description:
            - Specifies the profile that you want to use as the parent profile.
        default: rtsp
    idle_timeout:
        description:
            - Specifies the number of seconds that a connection is idle before the connection is eligible for deletion.
        default: 300
    log_profile:
        description:
            - Specify the name of the ALG log profile which controls the logging of ALG .
    log_publisher:
        description:
            - Specify the name of the log publisher which logs translation events.
    max_header_size:
        description:
            - Specifies the maximum size of an RTSP request or response header that the RTSP filter accepts before
              dropping the connection.
        default: 4096
    max_queued_data:
        description:
            - Specifies the maximum amount of data that the RTSP filter buffers before dropping the connection.
        default: 32768
    multicast_redirect:
        description:
            - Specifies whether to enable or disable multicast redirect.
        default: disabled
        choices: ['disabled', 'enabled']
    proxy:
        description:
            - Specifies whether the RTSP filter is associated with an RTSP proxy configuration.
    proxy_header:
        description:
            - When the proxy option is set, specifies the name of the header in the RTSP proxy configuration that is
              passed from the client-side virtual server to the server-side virtual server.
    real_http_persistence:
        description:
            - Specifies whether to enable or disable real HTTP persistence.
        default: enabled
        choices: ['disabled', 'enabled']
    rtcp_port:
        description:
            - Specifies the number of the port to use for the Real Time Control Protocol (RTCP) service.
        default: 0
    rtp_port:
        description:
            - Specifies the number of the port to use for the RTP service.
    session_reconnect:
        description:
            - Specifies whether to enable or disable session reconnect.
        default: disabled
        choices: ['disabled', 'enabled']
    unicast_redirect:
        description:
            - Specifies whether to enable or disable unicast redirect.
        default: disabled
        choices: ['disabled', 'enabled']
extends_documentation_fragment:
    - f5_common
    - f5_app_service
    - f5_description
    - f5_name
    - f5_partition
    - f5_state
"""

EXAMPLES = """
- name: Create LTM Profile RTSP
  f5bigip_ltm_profile_rtsp:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: my_rtsp_profile
    partition: Common
    description: My rtsp profile
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
            check_source=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            defaults_from=dict(type="str"),
            description=dict(type="str"),
            idle_timeout=dict(type="int"),
            log_profile=dict(type="str"),
            log_publisher=dict(type="str"),
            max_header_size=dict(type="int"),
            max_queued_data=dict(type="int"),
            multicast_redirect=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            proxy=dict(type="str"),
            proxy_header=dict(type="str"),
            real_http_persistence=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            rtcp_port=dict(type="int"),
            rtp_port=dict(type="int"),
            session_reconnect=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            unicast_redirect=dict(type="str", choices=F5_ACTIVATION_CHOICES),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpLtmProfileRtsp(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "create": self._api.tm.ltm.profile.rtsps.rtsp.create,
            "read": self._api.tm.ltm.profile.rtsps.rtsp.load,
            "update": self._api.tm.ltm.profile.rtsps.rtsp.update,
            "delete": self._api.tm.ltm.profile.rtsps.rtsp.delete,
            "exists": self._api.tm.ltm.profile.rtsps.rtsp.exists,
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpLtmProfileRtsp(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
