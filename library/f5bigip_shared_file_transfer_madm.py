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
module: f5bigip_shared_file_transfer_madm
short_description: BIG-IP shared file transfer madm module
description:
    - Downloads files.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Gabriel Fortin (@GabrielFortin)"
options:
    file_name:
        description:
            - Specifies the name of the file to download.
        required: true
    download_path:
        description:
            - Specifies the path where the file will be downloaded.
        required: true
extends_documentation_fragment:
    - f5_common
"""

EXAMPLES = """
- name: Download file
  f5bigip_shared_file_transfer_madm:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    file_name: test.txt
    download_path: /var/test.txt
  delegate_to: localhost
"""

RETURN = """ # """

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.erjac77.network.f5.base import AnsibleF5Error
from ansible.module_utils.erjac77.network.f5.common import F5_PROVIDER_ARGS
from ansible.module_utils.erjac77.network.f5.bigip import F5BigIpUnnamedObject


class ModuleParams(object):
    @property
    def argument_spec(self):
        argument_spec = dict(
            file_name=dict(type="str", required=True),
            download_path=dict(type="str", required=True),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpSharedFileTransferMadm(F5BigIpUnnamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "download_file": self._api.shared.file_transfer.madm.download_file
        }

    def flush(self):
        result = dict(changed=False)

        if self._check_mode:
            result["changed"] = True
            return result

        try:
            self._methods["download_file"](
                self._params["fileName"], self._params["downloadPath"]
            )
            result["changed"] = True
        except Exception:
            raise AnsibleF5Error("Cannot download the file.")

        return result


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpSharedFileTransferMadm(
            check_mode=module.check_mode, **module.params
        )
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
