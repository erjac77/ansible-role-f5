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
module: f5bigip_sys_provision
short_description: BIG-IP sys provision module
description:
    - Configures provisioning on the BIG-IP system.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Gabriel Fortin (@GabrielFortin)"
options:
    cpu_ratio:
        description:
            - Use this option only when the level option is set to custom.
    disk_ratio:
        description:
            - Use this option only when the level option is set to custom.
    level:
        description:
            - Specifies the level of resources that you want to provision for a module.
        choices: ['custom', 'dedicated', 'minimum', 'nominal', 'none']
    memory_ratio:
        description:
            - Use this option only when the level option is set to custom.
    name:
        description:
            - Specifies which module to use.
        required: true
        choices: ['afm', 'am', 'apm', 'asm', 'avr', 'fps', 'gtm', 'lc', 'ltm', 'pem', 'swg']
extends_documentation_fragment:
    - f5_common
"""

EXAMPLES = """
- name: Provision GTM with minimal resources
  f5bigip_sys_provision:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: gtm
    level: minimal
    state: present
  delegate_to: localhost
"""

RETURN = """ # """

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.erjac77.network.f5.common import F5_PROVIDER_ARGS
from ansible.module_utils.erjac77.network.f5.bigip import F5BigIpUnnamedObject


class ModuleParams(object):
    @property
    def argument_spec(self):
        argument_spec = dict(
            cpu_ratio=dict(type="int"),
            disk_ratio=dict(type="int"),
            level=dict(
                type="str",
                choices=["custom", "dedicated", "minimum", "nominal", "none"],
            ),
            memory_ratio=dict(type="int"),
            name=dict(
                type="str",
                choices=[
                    "afm",
                    "am",
                    "apm",
                    "asm",
                    "avr",
                    "fps",
                    "gtm",
                    "lc",
                    "ltm",
                    "pem",
                    "swg",
                ],
            ),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpSysProvision(F5BigIpUnnamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "afm_read": self._api.tm.sys.provision.afm.load,
            "afm_update": self._api.tm.sys.provision.afm.update,
            "am_read": self._api.tm.sys.provision.am.load,
            "am_update": self._api.tm.sys.provision.am.update,
            "apm_read": self._api.tm.sys.provision.apm.load,
            "apm_update": self._api.tm.sys.provision.apm.update,
            "asm_read": self._api.tm.sys.provision.asm.load,
            "asm_update": self._api.tm.sys.provision.asm.update,
            "avr_read": self._api.tm.sys.provision.avr.load,
            "avr_update": self._api.tm.sys.provision.avr.update,
            "fps_read": self._api.tm.sys.provision.fps.load,
            "fps_update": self._api.tm.sys.provision.fps.update,
            "gtm_read": self._api.tm.sys.provision.gtm.load,
            "gtm_update": self._api.tm.sys.provision.gtm.update,
            "lc_read": self._api.tm.sys.provision.lc.load,
            "lc_update": self._api.tm.sys.provision.lc.update,
            "ltm_read": self._api.tm.sys.provision.ltm.load,
            "ltm_update": self._api.tm.sys.provision.ltm.update,
            "pem_read": self._api.tm.sys.provision.pem.load,
            "pem_update": self._api.tm.sys.provision.pem.update,
            "swg_read": self._api.tm.sys.provision.swg.load,
        }

    def _read(self):
        if self._params["name"] == "afm":
            return self._methods["afm_read"]()
        elif self._params["name"] == "am":
            return self._methods["am_read"]()
        elif self._params["name"] == "apm":
            return self._methods["apm_read"]()
        elif self._params["name"] == "asm":
            return self._methods["asm_read"]()
        elif self._params["name"] == "avr":
            return self._methods["avr_read"]()
        elif self._params["name"] == "fps":
            return self._methods["fps_read"]()
        elif self._params["name"] == "gtm":
            return self._methods["gtm_read"]()
        elif self._params["name"] == "lc":
            return self._methods["lc_read"]()
        elif self._params["name"] == "ltm":
            return self._methods["ltm_read"]()
        elif self._params["name"] == "pem":
            return self._methods["pem_read"]()
        elif self._params["name"] == "swg":
            return self._methods["swg_read"]()


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpSysProvision(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
