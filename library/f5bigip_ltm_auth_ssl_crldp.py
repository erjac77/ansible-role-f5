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
module: f5bigip_ltm_auth_ssl_crldp
short_description: BIG-IP ltm auth ssl crldp module
description:
    - Configures a Secure Socket Layer (SSL) Certificate Revocation List Distribution Point (CRLDP) configuration object
      for implementing SSL CRLDP to manage certificate revocation.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Gabriel Fortin (@GabrielFortin)"
options:
    cache_timeout:
        description:
            - Specifies the number of seconds that CRLs are cached.
        default: 86400
    connection_timeout:
        description:
            - Specifies the number of seconds before the connection times out.
        default: 15
    servers:
        description:
            - Specifies a host name or IP address for the secure CRLDP server.
    update_interval:
        description:
            - Specifies an update interval for CRL distribution points that ensures that CRL status is checked at
              regular intervals, regardless of the CRL timeout value.
        default: 0
    use_issuer:
        description:
            - Specifies whether the system extracts the CRL distribution point from the client certificate.
        default: disabled
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
- name: Create LTM AUTH SSL CRLDP
  f5bigip_ltm_auth_ssl_crldp:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: my_ssl_crldp
    partition: Common
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
            cache_timeout=dict(type="int"),
            connection_timeout=dict(type="int"),
            description=dict(type="str"),
            servers=dict(type="list"),
            update_interval=dict(type="int"),
            use_issuer=dict(type="str", choices=F5_ACTIVATION_CHOICES),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpLtmAuthSslCrldp(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "create": self._api.tm.ltm.auth.ssl_crldps.ssl_crldp.create,
            "read": self._api.tm.ltm.auth.ssl_crldps.ssl_crldp.load,
            "update": self._api.tm.ltm.auth.ssl_crldps.ssl_crldp.update,
            "delete": self._api.tm.ltm.auth.ssl_crldps.ssl_crldp.delete,
            "exists": self._api.tm.ltm.auth.ssl_crldps.ssl_crldp.exists,
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpLtmAuthSslCrldp(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
