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
module: f5bigip_util_unix_rm
short_description: BIG-IP util unix rm module
description:
    - Removes files or directories.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Gabriel Fortin (@GabrielFortin)"
    - "Eric Jacob (@erjac77)"
options:
    path:
        description:
            - Specifies the path of the file that is to be removed.
        required: true
extends_documentation_fragment:
    - f5_common
"""

EXAMPLES = """
- name: Removes a file
  f5bigip_util_unix_rm:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    path: /var/config/rest/downloads/data.dat
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
        argument_spec = dict(path=dict(type="str", required=True))
        argument_spec.update(F5_PROVIDER_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpUtilUnixRm(F5BigIpUnnamedObject):
    def _set_crud_methods(self):
        self._methods = {"run": self._api.tm.util.unix_rm.exec_cmd}

    def flush(self):
        result = dict(changed=False, stdout=list())

        if self._check_mode:
            result["changed"] = True
            return result

        try:
            output = self._methods["run"]("run", utilCmdArgs=self._params["path"])
            result["changed"] = True
        except Exception as exc:
            err_msg = "Cannot remove the file."
            err_msg += ' The error message was "{0}".'.format(str(exc))
            raise AnsibleF5Error(err_msg)

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
        obj = F5BigIpUtilUnixRm(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
