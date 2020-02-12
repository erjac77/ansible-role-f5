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
module: f5bigip_ltm_auth_crldp_server
short_description: BIG-IP ltm auth crldp server
description:
    - Creates a Certificate Revocation List Distribution Point (CRDLP) server for implementing a CRLDP authentication
      module.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Gabriel Fortin (@GabrielFortin)"
options:
    base_dn:
        description:
            - Specifies the LDAP base directory name for certificates that specify the CRL distribution point in
              directory name format (dirName).
    host:
        description:
            - Specifies an IP address for the CRLDP server.
        required: true
    port:
        description:
            - Specifies the port for CRLDP authentication traffic.
        default: 389
    reverse_dn:
        description:
            - Specifies in which order the system attempts to match the value of the base-dn option to the value of the
              X509v3 attribute crlDistributionPoints.
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
            app_service=dict(type="str"),
            base_dn=dict(type="str"),
            description=dict(type="str"),
            host=dict(type="str"),
            port=dict(type="int"),
            reverse_dn=dict(type="str", choices=F5_ACTIVATION_CHOICES),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpLtmAuthCrldpServer(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "create": self._api.tm.ltm.auth.crldp_servers.crldp_server.create,
            "read": self._api.tm.ltm.auth.crldp_servers.crldp_server.load,
            "update": self._api.tm.ltm.auth.crldp_servers.crldp_server.update,
            "delete": self._api.tm.ltm.auth.crldp_servers.crldp_server.delete,
            "exists": self._api.tm.ltm.auth.crldp_servers.crldp_server.exists,
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpLtmAuthCrldpServer(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
