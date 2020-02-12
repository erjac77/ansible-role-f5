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
module: f5bigip_sys_version
short_description: BIG-IP sys version module
description:
    - Displays software version information for the BIG-IP system.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Eric Jacob (@erjac77)"
extends_documentation_fragment:
    - f5_common
"""

EXAMPLES = """
- name: Gets software version information of the device
  f5bigip_sys_version:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
  delegate_to: localhost
  register: result

- name: Displays the software version running on the device
  debug:
    msg: "Version: {{ result.version }}"
"""

RETURN = """
build:
    description: The build number of the software
    returned: success
    type: string
    sample:
        - 0.0.249
date:
    description: The release date of the software
    returned: success
    type: string
    sample:
        - Wed Nov 30 16:04:00 PST 2016
edition:
    description: The edition of the software
    returned: success
    type: string
    sample:
        - Final
product:
    description: The system on which the software is running
    returned: success
    type: string
    sample:
        - BIG-IP
title:
    description: The software package
    returned: success
    type: string
    sample:
        - Main Package
version:
    description: The software version
    returned: success
    type: string
    sample:
        - 12.1.2
"""

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.erjac77.network.f5.base import AnsibleF5Error
from ansible.module_utils.erjac77.network.f5.common import F5_PROVIDER_ARGS
from ansible.module_utils.erjac77.network.f5.bigip import F5BigIpUnnamedObject


class ModuleParams(object):
    @property
    def argument_spec(self):
        argument_spec = dict()
        argument_spec.update(F5_PROVIDER_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpSysVersion(F5BigIpUnnamedObject):
    def _set_crud_methods(self):
        self._methods = {"read": self._api.tm.sys.version.load}

    def flush(self):
        result = dict(changed=False)

        try:
            version = self._methods["read"]()
            version_stats = version.entries["https://localhost/mgmt/tm/sys/version/0"][
                "nestedStats"
            ]["entries"]
        except Exception:
            raise AnsibleF5Error("Cannot display the version information.")

        result.update(
            build=version_stats["Build"]["description"],
            date=version_stats["Date"]["description"],
            edition=version_stats["Edition"]["description"],
            product=version_stats["Product"]["description"],
            title=version_stats["Title"]["description"],
            version=version_stats["Version"]["description"],
        )

        return result


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpSysVersion(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
