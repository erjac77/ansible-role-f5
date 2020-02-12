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
module: f5bigip_ltm_profile_sip
short_description: BIG-IP ltm profile sip module
description:
    - Configures a Session Initiation Protocol (SIP) profile.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Gabriel Fortin (@GabrielFortin)"
options:
    alg_enable:
        description:
            - Enables or disables the SIP ALG (Application Level Gateway) feature.
        default: disabled
        choices: ['disabled', 'enabled']
    community:
        description:
            - Specifies the community to which you want to assign the virtual server that you associate with this
              profile.
    defaults_from:
        description:
            - Specifies the profile that you want to use as the parent profile.
        default: sip
    dialog_aware:
        description:
            - Enables or disables the ability for the system to be aware of unauthorized use of the SIP dialog.
        default: disabled
        choices: ['disabled', 'enabled']
    dialog_establishment_timeout:
        description:
            - Indicates the timeout value for dialog establishment in a sip session.
        default: 10
    enable_sip_firewall:
        description:
            - Indicates whether to enable SIP firewall functionality or not.
        default: no
        choices: ['no', 'yes']
    insert_record_route_header:
        description:
            - Enables or disables the insertion of a Record-Route header, which indicates the next hop for the following
              SIP request messages.
        default: disabled
        choices: ['disabled', 'enabled']
    insert_via_header:
        description:
            - Enables or disables the insertion of a Via header, which indicates where the message originated.
        default: disabled
        choices: ['disabled', 'enabled']
    log_profile:
        description:
            - Specify the name of the ALG log profile which controls the logging of ALG .
    log_publisher:
        description:
            - Specify the name of the log publisher which logs translation events.
    max_media_sessions:
        description:
            - Indicates the maximum number of SDP media sessions that the BIG-IP system accepts.
        default: 6
    max_registrations:
        description:
            - Indicates the maximum number of registrations, the maximum allowable REGISTER messages can be recorded
              that the BIG-IP system accepts.
        default: 100
    max_sessions_per_registration:
        description:
            - Indicates the maximum number of calls or sessions can be made by a user for a single registration that the
              BIG-IP system accepts.
        default: 50
    max_size:
        description:
            - Specifies the maximum SIP message size that the BIG-IP system accepts.
        default: 65535
    registration_timeout:
        description:
            - Indicates the timeout value for a sip registration.
        default: 3600
    rtp_proxy_style:
        description:
            - Indicates the style in which the RTP will proxy the data.
        default: symmetric
        choices: ['symmetric', 'restricted-by-ip-address', 'any-location']
    secure_via_header:
        description:
            - Enables or disables the insertion of a Secure Via header, which indicates where the message originated.
        default: disabled
        choices: ['disabled', 'enabled']
    security:
        description:
            - Enables or disables security for the SIP profile.
        default: disabled
        choices: ['disabled', 'enabled']
    sip_session_timeout:
        description:
            - Indicates the timeout value for a sip session.
        default: 300
    terminate_on_bye:
        description:
            - Enables or disables the termination of a connection when a BYE transaction finishes.
        default: enabled
        choices: ['disabled', 'enabled']
    user_via_header:
        description:
            - Enables or disables the insertion of a Via header specified by a system administrator.
extends_documentation_fragment:
    - f5_common
    - f5_app_service
    - f5_description
    - f5_name
    - f5_partition
    - f5_state
"""

EXAMPLES = """
- name: Create LTM Profile sip
  f5bigip_ltm_profile_sip:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: my_sip_profile
    partition: Common
    description: My sip profile
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
            alg_enable=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            app_service=dict(type="str"),
            community=dict(type="str"),
            defaults_from=dict(type="str"),
            description=dict(type="str"),
            dialog_aware=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            dialog_establishment_timeout=dict(type="int"),
            enable_sip_firewall=dict(type="str", choices=F5_POLAR_CHOICES),
            insert_record_route_header=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            insert_via_header=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            log_profile=dict(type="str"),
            log_publisher=dict(type="str"),
            max_media_sessions=dict(type="int"),
            max_registrations=dict(type="int"),
            max_sessions_per_registration=dict(type="int"),
            max_size=dict(type="int"),
            registration_timeout=dict(type="int"),
            rtp_proxy_style=dict(
                type="str",
                choices=["symmetric", "restricted-by-ip-address", "any-location"],
            ),
            secure_via_header=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            security=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            sip_session_timeout=dict(type="int"),
            terminate_on_bye=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            user_via_header=dict(type="str"),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpLtmProfileSip(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "create": self._api.tm.ltm.profile.sips.sip.create,
            "read": self._api.tm.ltm.profile.sips.sip.load,
            "update": self._api.tm.ltm.profile.sips.sip.update,
            "delete": self._api.tm.ltm.profile.sips.sip.delete,
            "exists": self._api.tm.ltm.profile.sips.sip.exists,
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpLtmProfileSip(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
