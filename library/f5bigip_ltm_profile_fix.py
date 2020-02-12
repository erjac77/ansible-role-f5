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
module: f5bigip_ltm_profile_fix
short_description: BIG-IP ltm profile fix module
description:
    - Configures a Financial Information eXchange Protocol (FIX) profile.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Gabriel Fortin (@GabrielFortin)"
options:
    error_action:
        description:
            - Specifies the error handling method.
        choices: ['drop_connection', 'dont_forward']
    full_logon_parsing:
        description:
            - Enable or disable logon message is always fully parsed.
        default: true
        choices: ['true', 'false']
    message_log_publisher:
        description:
            - Specifies the publisher for message logging.
    quick_parsing:
        description:
            - Enable or disable quick parsing which parses the basic standard fields and validates message length and
              checksum.
        default: false
        choices: ['true', 'false']
    report_log_publisher:
        description:
            - Specifies the publisher for error message and status report.
    response_parsing:
        description:
            - Enable or disable response parsing which parses the messages from FIX server.
        default: false
        choices: ['true', 'false']
    sender_tag_class:
        description:
            - Specifies the tag substitution map between sender id and tag substitution data group.
    statistics_sample_interval:
        description:
            - Specifies the sample interval in seconds of the message rate.
extends_documentation_fragment:
    - f5_common
    - f5_app_service
    - f5_description
    - f5_name
    - f5_partition
    - f5_state
"""

EXAMPLES = """
- name: Create LTM Profile FIX
  f5bigip_ltm_profile_fix:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: my_fix_profile
    partition: Common
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
            error_action=dict(type="str", choices=["drop_connection", "dont_forward"]),
            full_logon_parsing=dict(type="str", choices=["true", "false"]),
            message_log_publisher=dict(type="str"),
            quick_parsing=dict(type="str", choices=["true", "false"]),
            report_log_publisher=dict(type="str"),
            response_parsing=dict(type="str", choices=["true", "false"]),
            sender_tag_class=dict(type="dict"),
            statistics_sample_interval=dict(type="int"),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpLtmProfileFix(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "create": self._api.tm.ltm.profile.fixs.fix.create,
            "read": self._api.tm.ltm.profile.fixs.fix.load,
            "update": self._api.tm.ltm.profile.fixs.fix.update,
            "delete": self._api.tm.ltm.profile.fixs.fix.delete,
            "exists": self._api.tm.ltm.profile.fixs.fix.exists,
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpLtmProfileFix(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
