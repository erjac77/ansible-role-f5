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
module: f5bigip_ltm_snat
short_description: BIG-IP ltm snat module
description:
    - You can use the snat component to configure a SNAT.
    - A SNAT defines the relationship between an externally visible IP address, SNAT IP address, or translated address,
      and a group of internal IP addresses, or originating addresses, of individual servers at your site.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Gabriel Fortin (@GabrielFortin)"
options:
    automap:
        description:
            - Specifies that the system translates the source IP address to an available self IP address when
              establishing connections through the virtual server.
        default: enabled
        choices: ['none', 'enabled']
    metadata:
        description:
            - Associates user defined data, each of which has name and value pair and persistence.
    mirror:
        description:
            - Enables or disables mirroring of SNAT connections.
    origins:
        description:
            - Specifies a set of IP addresses and subnets from which connections originate.
        required: true
    snatpool:
        description:
            - Specifies the name of a SNAT pool.
    source_port:
        description:
            - Specifies whether the system preserves the source port of the connection.
        default: preserve
        choices: ['change', 'preserve', 'preserve-strict']
    translation:
        description:
            - Specifies the name of a translated IP address.
    vlans:
        description:
            - Specifies the name of the VLAN to which you want to assign the SNAT.
    vlans_disabled:
        description:
            - Disables the SNAT on all VLANs.
    vlans_enabled:
        description:
            - Enables the SNAT on all VLANs.
extends_documentation_fragment:
    - f5_common
    - f5_app_service
    - f5_description
    - f5_name
    - f5_partition
    - f5_state
"""

EXAMPLES = """
- name: Create LTM Snat
  f5bigip_ltm_snat:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: my_snat
    partition: Common
    description: My snat
    vlans: external
    vlans_enabled: true
    state: present
  delegate_to: localhost
"""

RETURN = """ # """

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.erjac77.network.f5.common import F5_NAMED_OBJ_ARGS
from ansible.module_utils.erjac77.network.f5.common import F5_PROVIDER_ARGS
from ansible.module_utils.erjac77.network.f5.bigip import F5BigIpNamedObject


class ModuleParams(object):
    @property
    def argument_spec(self):
        argument_spec = dict(
            auto_lasthop=dict(type="str", default="default"),
            automap=dict(type="bool"),
            app_service=dict(type="str"),
            description=dict(type="str"),
            metadata=dict(type="list"),
            mirror=dict(
                type="str", choices=["none", "enabled", "disabled"], default="disabled"
            ),
            origins=dict(type="list"),
            snatpool=dict(type="str"),
            source_port=dict(
                type="str",
                choices=["change", "preserve", "preserve-strict"],
                default="preserve",
            ),
            translation=dict(type="str"),
            vlans=dict(type="str"),
            vlans_disabled=dict(type="bool", default=True),
            vlans_enabled=dict(type="bool"),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True

    @property
    def mutually_exclusive(self):
        return [["vlans_disabled", "vlans_enabled"], ["automap", "snatpool"]]


class F5BigIpLtmSnat(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "create": self._api.tm.ltm.snats.snat.create,
            "read": self._api.tm.ltm.snats.snat.load,
            "update": self._api.tm.ltm.snats.snat.update,
            "delete": self._api.tm.ltm.snats.snat.delete,
            "exists": self._api.tm.ltm.snats.snat.exists,
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
        mutually_exclusive=params.mutually_exclusive,
    )

    try:
        obj = F5BigIpLtmSnat(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
