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
module: f5bigip_ltm_profile_ocsp_stapling_params
short_description: BIG-IP ltm profile ocsp stapling params module
description:
    - Configures an OCSP Stapling Params profile.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Gabriel Fortin (@GabrielFortin)"
options:
    cache_error_timeout:
        description:
            - Specifies the lifetime of an error response in the cache, in seconds.
        default: 3600
    cache_timeout:
        description:
            - Specifies the lifetime of the OCSP response in the cache, in seconds.
        default: indefinite
    clock_skew:
        description:
            - Specifies the tolerable absolute difference in the clocks of the responder and the BIG-IP, in seconds.
        default: 300
    dns_resolver:
        description:
            - Specifies the DNS resolver object used for fetching the OCSP response.
        required: false
    proxy_server_pool:
        description:
            - Specifies the proxy server pool used for fetching the OCSP response.
    responder_url:
        description:
            - Specifies the absolute URL that overrides the OCSP responder URL obtained from the certificate's AIA
              extension(s).
    sign_hash:
        description:
            - Specifies the hash algorithm used for signing the OCSP request.
        default: sha256
        choices: ['sha256', 'sha1']
    signer_cert:
        description:
            - Specifies the certificate corresponding to the key used for signing the OCSP request.
    signer_key:
        description:
            - Specifies the passphrase of the key used for signing the OCSP request.
    signer_key_passphrase:
        description:
            - Specifies the passphrase of the key used for signing the OCSP request.
    status_age:
        description:
            - Specifies the allowed age of the OCSP response when nextUpdate time is omitted from the response.
        default: 300
    strict_resp_cert_check:
        description:
            - If enabled, the responder's certificate is checked for OCSP signing extension.
        default: disabled
        choices: ['disabled', 'enabled']
    timeout:
        description:
            - Specifies the time interval (in seconds) that the BIG-IP waits for before aborting the connection to the
              OCSP responder.
        default: 8
    trusted_ca:
        description:
            - Specifies the certificate-authority that signs the responder's certificate.
    trusted_responders:
        description:
            - Specifies the certificate(s) used for validating the OCSP response when the responder's certificate has
              been omitted from the response.
    use_proxy_server:
        description:
            - Specifies whether the proxy server pool or the DNS resolver should be used for the connection to the OCSP
              responder.
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
- name: Create LTM Profile OCSP Stapling Params
  f5bigip_ltm_profile_ocsp_stapling_params:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: my_ocsp_stapling_params_profile
    partition: Common
    dns_resolver: /Common/my_dns_resolver
    trusted_ca: /Common/ca-bundle.crt
    use_proxy_server: disabled
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
            cache_error_timeout=dict(type="int"),
            cache_timeout=dict(type="int"),
            clock_skew=dict(type="int"),
            description=dict(type="str"),
            dns_resolver=dict(type="str"),
            proxy_server_pool=dict(type="str"),
            responder_url=dict(type="str"),
            sign_hash=dict(type="str", choices=["sha1", "sha256"]),
            signer_cert=dict(type="str"),
            signer_key=dict(type="str"),
            signer_key_passphrase=dict(type="str", no_log=True),
            status_age=dict(type="int"),
            strict_resp_cert_check=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            timeout=dict(type="int"),
            trusted_ca=dict(type="str"),
            trusted_responders=dict(type="str"),
            use_proxy_server=dict(type="str", choices=F5_ACTIVATION_CHOICES),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpLtmProfileOcspStaplingParams(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "create": self._api.tm.ltm.profile.ocsp_stapling_params_s.ocsp_stapling_params.create,
            "read": self._api.tm.ltm.profile.ocsp_stapling_params_s.ocsp_stapling_params.load,
            "update": self._api.tm.ltm.profile.ocsp_stapling_params_s.ocsp_stapling_params.update,
            "delete": self._api.tm.ltm.profile.ocsp_stapling_params_s.ocsp_stapling_params.delete,
            "exists": self._api.tm.ltm.profile.ocsp_stapling_params_s.ocsp_stapling_params.exists,
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpLtmProfileOcspStaplingParams(
            check_mode=module.check_mode, **module.params
        )
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
