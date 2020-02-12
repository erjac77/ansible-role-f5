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
module: f5bigip_sys_httpd
short_description: BIG-IP sys httpd module
description:
    - Configures the HTTP daemon for the BIG-IP system.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Eric Jacob (@erjac77)"
options:
    allow:
        description:
            - Configures IP addresses and hostnames for the HTTP clients from which the httpd daemon accepts requests.
        default: all
    auth_name:
        description:
            - Specifies the name for the authentication realm.
        default: BIG-IP
    auth_pam_dashboard_timeout:
        description:
            - Specifies whether idle timeout while viewing the dashboard is enforced or not.
        default: off
        choices: ['on', 'off']
    auth_pam_idle_timeout:
        description:
            - Specifies the number of seconds of inactivity that can elapse before the GUI session is automatically
              logged out.
        default: 1200
    auth_pam_validate_ip:
        description:
            - Specifies whether the check for consistent inbound IP for the entire web session is enforced or not.
        default: on
        choices: ['on', 'off']
    fast_cgitimeout:
        description:
            - Specifies, in seconds, the timeout for FastCGI.
        default: 300
    hostname_lookup:
        description:
            - Specifies whether to lookup hostname or not.
        default: off
        choices: ['on', 'off']
    log_level:
        description:
            - Specifies the minimum httpd message level to include in the system log.
        default: warn
        choices: ['alert', 'crit', 'debug', 'emerg', 'err', 'info', 'notice', 'warning']
    redirect_http_to_https:
        description:
            - Specifies whether the system should redirect HTTP requests targeted at the configuration utility to HTTPS.
        default: disabled
        choices: ['enabled', 'disabled']
    request_header_max_timeout:
        description:
            - Specifies, in seconds, the maximum time allowed to receive all of the .request headers
        default: 40
    request_header_min_rate:
        description:
            - Specifies, in bytes per second, the minimum average rate at which the request headers must be received.
        default: 500
    request_header_timeout:
        description:
            - Specifies, in seconds, the time allowed to receive all of the request headers.
        default: 20
    request_body_max_timeout:
        description:
            - Specifies, in seconds, the maximum time allowed to receive all of the request body.
        default: 0 (no limit)
    request_body_min_rate:
        description:
            - Specifies, in bytes per second, the minimum average rate at which the request body must be received.
        default: 500
    request_body_timeout:
        description:
            - Specifies, in seconds, the time allowed for reading all of the request body.
        default: 60
    ssl_ca_cert_file:
        description:
            - Specifies the name of the file that contains the SSL Certificate Authority (CA) certificate file.
    ssl_certchainfile:
        description:
            - Specifies the name of the file that contains the SSL certificate chain.
    ssl_certfile:
        description:
            - Specifies the name of the file that contains the SSL certificate.
        default: /etc/httpd/conf/ssl.crt/server.crt
    ssl_certkeyfile:
        description:
            - Specifies the name of the file that contains the SSL certificate key.
        default: /etc/httpd/conf/ssl.key/server.key
    ssl_ciphersuite:
        description:
            - Specifies the ciphers that the system uses.
        default: 'ALL:!ADH:!EXPORT:!eNULL:!MD5:!DES:RC4+RSA:+HIGH:+MEDIUM:+LOW:+SSLv2'
    ssl_include:
        description:
            - TODO
    ssl_ocsp_default_responder:
        description:
            - Specifies the default responder URI for OCSP validation.
        default: http://localhost.localdomain
    ssl_ocsp_enable:
        description:
            - Specifies OCSP validation of the client certificate chain.
        default: off
        choices: ['on', 'off']
    ssl_ocsp_override_responder:
        description:
            - Specifies the force use of default responder URI for OCSP validation.
        default: off
        choices: ['on', 'off']
    ssl_ocsp_responder_timeout:
        description:
            - Specifies the maximum allowable time in seconds for OCSP response.
        default: 300
    ssl_ocsp_response_max_age:
        description:
            - Specifies the maximum allowable age ("freshness") for OCSP responses.
        default: -1
    ssl_ocsp_response_time_skew:
        description:
            - Specifies the maximum allowable time skew in seconds for OCSP response validation.
        default: 300
    ssl_protocol:
        description:
            - The list of SSL protocols to accept on the management console.
        default: all -SSLv2
    ssl_verify_client:
        description:
            - Specifies if the client certificate needs to be verified for SSL session establishment.
        default: no
        choices: ['yes', 'no']
    ssl_verify_depth:
        description:
            - Specifies maximum depth of CA certificates in client certificate verification.
        default: 10
extends_documentation_fragment:
    - f5_common
    - f5_description
"""

EXAMPLES = """
- name: Set SYS HTTPD allow clients
  f5bigip_sys_httpd:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    allow:
      - 172.16.227.0/24
      - 10.0.0.0/8
  delegate_to: localhost

- name: Reset SYS HTTPD allow clients
  f5bigip_sys_httpd:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    allow:
      - ALL
      - 127.
  delegate_to: localhost
"""

RETURN = """ # """

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.erjac77.network.f5.common import F5_ACTIVATION_CHOICES
from ansible.module_utils.erjac77.network.f5.common import F5_PROVIDER_ARGS
from ansible.module_utils.erjac77.network.f5.common import F5_SEVERITY_CHOICES
from ansible.module_utils.erjac77.network.f5.common import F5_SWITCH_CHOICES
from ansible.module_utils.erjac77.network.f5.bigip import F5BigIpUnnamedObject


class ModuleParams(object):
    @property
    def argument_spec(self):
        argument_spec = dict(
            allow=dict(type="list"),
            auth_name=dict(type="str"),
            auth_pam_dashboard_timeout=dict(type="str", choices=F5_SWITCH_CHOICES),
            auth_pam_idle_timeout=dict(type="int"),
            auth_pam_validate_ip=dict(type="str", choices=F5_SWITCH_CHOICES),
            description=dict(type="str"),
            fastcgi_timeout=dict(type="int"),
            hostname_lookup=dict(type="str", choices=F5_SWITCH_CHOICES),
            log_level=dict(type="str", choices=F5_SEVERITY_CHOICES),
            redirect_http_to_https=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            request_header_max_timeout=dict(type="int"),
            request_header_min_rate=dict(type="int"),
            request_header_timeout=dict(type="int"),
            request_body_max_timeout=dict(type="int"),
            request_body_min_rate=dict(type="int"),
            request_body_timeout=dict(type="int"),
            ssl_ca_cert_file=dict(type="str"),
            ssl_certchainfile=dict(type="str"),
            ssl_certfile=dict(type="str"),
            ssl_certkeyfile=dict(type="str"),
            ssl_ciphersuite=dict(type="str"),
            ssl_include=dict(type="str"),
            ssl_ocsp_enable=dict(
                type="str", choices=["no", "require", "optional", "optional-no-ca"]
            ),
            ssl_ocsp_default_responder=dict(type="str"),
            ssl_ocsp_override_responder=dict(type="str", choices=F5_SWITCH_CHOICES),
            ssl_ocsp_responder_timeout=dict(type="int"),
            ssl_ocsp_response_max_age=dict(type="int"),
            ssl_ocsp_response_time_skew=dict(type="int"),
            ssl_protocol=dict(type="str"),
            ssl_verify_client=dict(type="str"),
            ssl_verify_depth=dict(type="int"),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpSysHttpd(F5BigIpUnnamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "read": self._api.tm.sys.httpd.load,
            "update": self._api.tm.sys.httpd.update,
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpSysHttpd(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
