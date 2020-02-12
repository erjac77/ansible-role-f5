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
module: f5bigip_util_clientssl_ciphers
short_description: BIG-IP util client ssl ciphers module
description:
    - Shows all ciphers that match the given cipher string.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Gabriel Fortin (@GabrielFortin)"
    - "Eric Jacob (@erjac77)"
options:
    cipher_string:
        description:
            - Specifies the cipher string.
        required: true
extends_documentation_fragment:
    - f5_common
"""

EXAMPLES = """
- name: Returns all ciphers matching the specified cipher string
  f5bigip_util_clientssl_ciphers:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    cipher_string: 'DEFAULT'
  delegate_to: localhost
"""

RETURN = """
stdout:
    description: The output of the command.
    returned: success
    type: list
    sample:
        - ['...', '...']
stdout_lines:
    description: A list of strings, each containing one item per line from the original output.
    returned: success
    type: list
    sample:
        - [['...', '...'], ['...'], ['...']]
"""

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.erjac77.network.f5.base import AnsibleF5Error
from ansible.module_utils.erjac77.network.f5.common import F5_PROVIDER_ARGS
from ansible.module_utils.erjac77.network.f5.bigip import F5BigIpUnnamedObject
from ansible.module_utils.erjac77.network.f5.utils import to_lines


class ModuleParams(object):
    @property
    def argument_spec(self):
        argument_spec = dict(cipher_string=dict(type="str", required=True))
        argument_spec.update(F5_PROVIDER_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpUtilClientSslCiphers(F5BigIpUnnamedObject):
    def _set_crud_methods(self):
        self._methods = {"run": self._api.tm.util.clientssl_ciphers.exec_cmd}

    def flush(self):
        result = dict(changed=False, stdout=list())

        try:
            output = self._methods["run"](
                "run", utilCmdArgs=self._params["cipherString"]
            )
            # result['changed'] = True
        except Exception:
            raise AnsibleF5Error("Could not execute the Client SSL Ciphers command.")

        if hasattr(output, "commandResult"):
            result["stdout"].append(str(output.commandResult))
        result["stdout_lines"] = list(to_lines(result["stdout"]))

        return result


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpUtilClientSslCiphers(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
