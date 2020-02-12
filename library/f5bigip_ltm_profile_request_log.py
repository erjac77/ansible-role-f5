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
module: f5bigip_ltm_profile_request_log
short_description: BIG-IP ltm profile request log module
description:
    - Configures a Request-Logging profile.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Gabriel Fortin (@GabrielFortin)"
options:
    defaults_from:
        description:
            - Specifies the default values from this profile.
    log_request_logging_errors:
        description:
            - Enables secondary logging should the primary lack sufficient available bandwidth.
        choices: ['disabled', 'enabled']
    log_response_by_default:
        description:
            - Indicates if response logging may be overridden via iRule.
        choices: ['disabled', 'enabled']
    log_response_logging_error:
        description:
            - Enables secondary logging should the primary lack sufficient available bandwidth.
        choices: ['disabled', 'enabled']
    proxy_close_on_error:
        description:
            - Specifies, if enabled, that the logging profile will close the connection after sending its
              proxy-response.
        choices: ['disabled', 'enabled']
    proxy_respond_on_logging_error:
        description:
            - Specifies that the logging profile respond directly (for example, with an HTTP 502) if the logging fails.
        choices: ['disabled', 'enabled']
    proxy_response:
        description:
            - Specifies the response to send on logging errors.
    request_log_error_pool:
        description:
            - Specifies the name of the pool from which to select log servers.
    request_log_error_protocol:
        description:
            - Specifies the HighSpeedLogging protocol to use when logging.
        choices: ['TCP', 'UDP', 'none']
    request_log_error_template:
        description:
            - Specifies the template to use when generating log messages.
    request_log_pool:
        description:
            - Specifies the name of the pool from which to select log servers.
    request_log_protocol:
        description:
            - Specifies the HighSpeedLogging protocol to use when logging.
        choices: ['TCP', 'UDP', 'none']
    request_log_template:
        description:
            - Specifies the template to use when generating log messages.
    request_logging:
        description:
            - Enables or disables logging before the response is returned to the client.
        choices: ['disabled', 'enabled']
    response_log_error_pool:
        description:
            - Specifies the name of the pool from which to select log servers.
        choices: ['TCP', 'UDP', 'none']
    response_log_error_protocol:
        description:
            - Specifies the HighSpeedLogging protocol to use when logging.
    response_log_error_template:
        description:
            - Specifies the template to use when generating log messages.
    response_log_pool:
        description:
            - Specifies the name of the pool from which to select log servers.
    response_log_protocol:
        description:
            - Specifies the HighSpeedLogging protocol to use when logging.
        choices: ['TCP', 'UDP', 'none']
    response_log_template:
        description:
            - Specifies the template to use when generating log messages.
    response_logging:
        description:
            - Enables or disables logging before the response is returned to the client.
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
- name: Create LTM Profile Request Log
  f5bigip_ltm_profile_request_log:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: my_request_log_profile
    partition: Common
    description: My request log profile
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
            log_request_logging_errors=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            log_response_by_default=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            log_response_logging_error=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            proxy_close_on_error=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            proxy_respond_on_logging_error=dict(
                type="str", choices=F5_ACTIVATION_CHOICES
            ),
            proxy_response=dict(type="str"),
            request_log_error_pool=dict(type="str"),
            request_log_error_protocol=dict(type="str", choices=["TCP", "UDP", "none"]),
            request_log_error_template=dict(type="str"),
            request_log_pool=dict(type="str"),
            request_log_protocol=dict(type="str", choices=["TCP", "UDP", "none"]),
            request_log_template=dict(type="str"),
            request_logging=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            response_log_error_pool=dict(type="str"),
            response_log_error_protocol=dict(
                type="str", choices=["TCP", "UDP", "none"]
            ),
            response_log_error_template=dict(type="str"),
            response_log_pool=dict(type="str"),
            response_log_protocol=dict(type="str", choices=["TCP", "UDP", "none"]),
            response_log_template=dict(type="str"),
            response_logging=dict(type="str", choices=F5_ACTIVATION_CHOICES),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpLtmProfileRequestLog(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "create": self._api.tm.ltm.profile.request_logs.request_log.create,
            "read": self._api.tm.ltm.profile.request_logs.request_log.load,
            "update": self._api.tm.ltm.profile.request_logs.request_log.update,
            "delete": self._api.tm.ltm.profile.request_logs.request_log.delete,
            "exists": self._api.tm.ltm.profile.request_logs.request_log.exists,
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpLtmProfileRequestLog(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
