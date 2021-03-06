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
module: f5bigip_ltm_profile_ftp
short_description: BIG-IP ltm ftp profile module
description:
    - Configures an FTP profile.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Gabriel Fortin (@GabrielFortin)"
options:
    defaults_from:
        description:
            - Specifies the profile that you want to use as the parent profile.
        default: ftp
    port:
        description:
            - Specifies a service for the data channel port used for this FTP profile.
        default: ftp-data
    security:
        description:
            - Enables or disables secure FTP traffic for the BIG-IP Application Security Manager.
        default: disabled
        choices: ['enabled', 'disabled']
    translate_extended:
        description:
            - Translates RFC2428 extended requests EPSV and EPRT to PASV and PORT when communicating with IPv4 servers.
        default: enabled
        choices: ['enabled', 'disabled']
    inherit_parent_profile:
        description:
            - Enables the FTP data channel to inherit the TCP profile used by the control channel. If disabled, the data
              channel uses FastL4 (BigProto) only.
        choices: ['enabled', 'disabled']
    log_publisher:
        description:
            - Specify the name of the log publisher which logs translation events.
    log_profile:
        description:
            - Specify the name of the ALG log profile which controls the logging of ALG.
extends_documentation_fragment:
    - f5_common
    - f5_app_service
    - f5_description
    - f5_name
    - f5_partition
    - f5_state
"""

EXAMPLES = """
- name: Create LTM FTP Profile
  f5bigip_ltm_profile_ftp:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: my_ftp_profile
    partition: Common
    security: enabled
    translate_extended: disabled
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
            defaults_from=dict(type="str"),
            description=dict(type="str"),
            security=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            translate_extented=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            inherit_parent_profile=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            log_publisher=dict(type="str"),
            log_profile=dict(type="str"),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpLtmProfileFtp(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "create": self._api.tm.ltm.profile.ftps.ftp.create,
            "read": self._api.tm.ltm.profile.ftps.ftp.load,
            "update": self._api.tm.ltm.profile.ftps.ftp.update,
            "delete": self._api.tm.ltm.profile.ftps.ftp.delete,
            "exists": self._api.tm.ltm.profile.ftps.ftp.exists,
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpLtmProfileFtp(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
