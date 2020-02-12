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
module: f5bigip_ltm_auth_ocsp_responder
short_description: BIG-IP ltm auth ocsp responder
description:
    - Configures Online Certificate System Protocol (OCSP) responder objects.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Gabriel Fortin (@GabrielFortin)"
options:
    allow_certs:
        description:
            - Enables or disables the addition of certificates to an OCSP request.
        default: enabled
        choices: ['enabled', 'disabled']
    ca_file:
        description:
            - Specifies the name of the file containing trusted CA certificates used to verify the signature on the OCSP
              response.
    ca_path:
        description:
            - Specifies the name of the path containing trusted CA certificates used to verify the signature on the OCSP
              response.
    cert_id_digest:
        description:
            - Specifies a specific algorithm identifier, either sha1 or md5.
        default: sha1
        choices: ['sha1', 'md5']
    chain:
        description:
            - Specifies whether the system constructs a chain from certificates in the OCSP response.
        default: enabled
        choices: ['enabled', 'disabled']
    check_certs:
        description:
            - Enables or disables verification of an OCSP response certificate.
        default: enabled
        choices: ['enabled', 'disabled']
    explicit:
        description:
            - Specifies that the Local Traffic Manager explicitly trusts that the OCSP response signer's certificate is
              authorized for OCSP response signing.
        default: enabled
        choices: ['enabled', 'disabled']
    ignore_aia:
        description:
            - Specifies whether the system ignores the URL contained in the certificate's AIA fields, and always uses
              the URL specified by the responder instead.
        default: disabled
        choices: ['enabled', 'disabled']
    intern:
        description:
            - Specifies whether the system ignores certificates contained in an OCSP response when searching for the
              signer's certificate.
        default: enabled
        choices: ['enabled', 'disabled']
    nonce:
        description:
            - Specifies whether the system verifies an OCSP response signature or the nonce values.
        default: enabled
        choices: ['enabled', 'disabled']
    sign_digest:
        description:
            - Specifies the algorithm for signing the request, using the signing certificate and key.
        default: sha1
    sign_key:
        description:
            - Specifies the key that the system uses to sign an OCSP request.
    sign_key_pass_phrase:
        description:
            - Specifies the passphrase that the system uses to encrypt the sign key.
    sign_other:
        description:
            - Adds a list of additional certificates to an OCSP request.
    signer:
        description:
            - Specifies a certificate used to sign an OCSP request.
    status_age:
        description:
            - Specifies the age of the status of the OCSP responder.
    trust_other:
        description:
            - Instructs the BIG-IP local traffic management system to trust the certificates specified with the
              verify-other option.
        default: 0
    url:
        description:
            - Specifies the URL used to contact the OCSP service on the responder.
        required: true
    va_file:
        description:
            - Specifies the name of the file containing explicitly trusted responder certificates.
    validity_period:
        description:
            - Specifies the number of seconds used to specify an acceptable error range.
        default: 300
    verify:
        description:
            - Enables or disables verification of an OCSP response signature or the nonce values.
        default: enabled
        choices: ['enabled', 'disabled']
    verify_cert:
        description:
            - Specifies that the system makes additional checks to see if the signer's certificate is authorized to
              provide the necessary status information.
        default: enabled
        choices: ['enabled', 'disabled']
    verify_other:
        description:
            - Specifies the name of the file used to search for an OCSP response signing certificate when the
              certificate has been omitted from the response.
    verify_sig:
        description:
            - Specifies that the system checks the signature on the OCSP response.
        default: enabled
        choices: ['enabled', 'disabled']
extends_documentation_fragment:
    - f5_common
    - f5_app_service
    - f5_description
    - f5_name
    - f5_partition
    - f5_state
"""

EXAMPLES = """
- name: Create LTM AUTH CRLDP Server
  f5bigip_ltm_auth_crldp_server:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: my_crldp_server
    partition: Common
    host: 10.0.0.4
    port: 389
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
            allow_certs=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            app_service=dict(type="str"),
            ca_file=dict(type="str"),
            ca_path=dict(type="str"),
            cert_id_digest=dict(type="str", choices=["md5", "sha1"]),
            chain=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            check_certs=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            description=dict(type="str"),
            explicit=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            ignore_aia=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            intern=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            nonce=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            sign_digest=dict(type="str", choices=["md5", "sha1"]),
            sign_key=dict(type="str"),
            sign_key_pass_phrase=dict(type="str", no_log=True),
            sign_other=dict(type="list"),
            signer=dict(type="str"),
            status_age=dict(type="int"),
            trust_other=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            url=dict(type="str"),
            va_file=dict(type="str"),
            validity_period=dict(type="int"),
            verify=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            verify_cert=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            verify_other=dict(type="str"),
            verify_sig=dict(type="str", choices=F5_ACTIVATION_CHOICES),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpLtmAuthOcspResponder(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "create": self._api.tm.ltm.auth.ocsp_responders.ocsp_responder.create,
            "read": self._api.tm.ltm.auth.ocsp_responders.ocsp_responder.load,
            "update": self._api.tm.ltm.auth.ocsp_responders.ocsp_responder.update,
            "delete": self._api.tm.ltm.auth.ocsp_responders.ocsp_responder.delete,
            "exists": self._api.tm.ltm.auth.ocsp_responders.ocsp_responder.exists,
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpLtmAuthOcspResponder(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
