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
module: f5bigip_ltm_snat_translation
short_description: BIG-IP ltm snat-translation module
description:
    - Explicitly defines the properties of a SNAT translation address.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Gabriel Fortin (@GabrielFortin)"
options:
    address:
        description:
            - The translation IP address.
    arp:
        description:
            - Indicates whether the system responds to ARP requests or sends gratuitous ARPs.
        default: enabled
        choices: ['enabled', 'disabled']
    connection_limit:
        description:
            - Specifies the number of connections a translation address must reach before it no longer initiates a
              connection.
        default: 0
    disabled:
        description:
            - Disables SNAT translation.
    enabled:
        description:
            - Enables SNAT translation.
    ip_idle_timeout:
        description:
            - Specifies the number of seconds that IP connections initiated using a SNAT address are allowed to remain
              idle before being automatically disconnected.
        default: indefinite
    tcp_idle_timeout:
        description:
            - Specifies the number of seconds that TCP connections initiated using a SNAT address are allowed to remain
              idle before being automatically disconnected.
        default: indefinite
    traffic_group:
        description:
            - Specifies the traffic group of the failover device group on which the SNAT is active.
    udp_idle_timeout:
        description:
            - Specifies the number of seconds that UDP connections initiated using a SNAT address are allowed to remain
              idle before being automatically disconnected.
        default: indefinite
extends_documentation_fragment:
    - f5_common
    - f5_app_service
    - f5_description
    - f5_name
    - f5_partition
    - f5_state
"""

EXAMPLES = """
- name: Create LTM Snat translation
  f5bigip_ltm_snat_translation:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: my_snat_translation
    partition: Common
    description: My snat translation
    address: 10.0.1.4
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
            address=dict(type="str"),
            app_service=dict(type="str"),
            arp=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            connection_limit=dict(type="int"),
            description=dict(type="str"),
            disabled=dict(type="bool"),
            enabled=dict(type="bool"),
            ip_idle_timeout=dict(type="int"),
            tcp_idle_timeout=dict(type="int"),
            traffic_group=dict(type="str"),
            udp_idle_timeout=dict(type="int"),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True

    @property
    def mutually_exclusive(self):
        return [["disabled", "enabled"]]


class F5BigIpLtmSnatTranslation(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "create": self._api.tm.ltm.snat_translations.snat_translation.create,
            "read": self._api.tm.ltm.snat_translations.snat_translation.load,
            "update": self._api.tm.ltm.snat_translations.snat_translation.update,
            "delete": self._api.tm.ltm.snat_translations.snat_translation.delete,
            "exists": self._api.tm.ltm.snat_translations.snat_translation.exists,
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
        mutually_exclusive=params.mutually_exclusive,
    )

    try:
        obj = F5BigIpLtmSnatTranslation(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
