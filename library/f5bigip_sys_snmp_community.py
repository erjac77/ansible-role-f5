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
module: f5bigip_sys_snmp_community
short_description: BIG-IP sys snmp community module
description:
    - Configures the simple network management protocol (SNMP) communities.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Eric Jacob (@erjac77)"
options:
    access:
        description:
            - Specifies the community access level to the MIB.
        default: ro
        choices: ['ro', 'rw']
    community_name:
        description:
            - Specifies the name of the community that you are configuring for the snmpd daemon.
        default: public
    ipv6:
        description:
            - Specifies to enable or disable IPv6 addresses for the community that you are configuring.
        default: disabled
        choices: ['enabled', 'disabled']
    oid_subset:
        description:
            - Specifies to restrict access by the community to every object below the specified object identifier (OID).
    source:
        description:
            - Specifies the source addresses with the specified community name that can access the management
              information base (MIB).
        default: default
extends_documentation_fragment:
    - f5_common
    - f5_description
    - f5_name
    - f5_state
"""

EXAMPLES = """
- name: Add SYS SNMP community
  f5bigip_sys_snmp_community:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: community1
    access: ro
    community_name: mycommunity1
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
            access=dict(type="str", choices=["ro", "rw"]),
            community_name=dict(type="str"),
            description=dict(type="str"),
            ipv6=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            oid_subset=dict(type="str"),
            source=dict(type="str"),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        del argument_spec["partition"]
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpSysSnmpCommunity(F5BigIpNamedObject):
    def _set_crud_methods(self):
        snmp = self._api.tm.sys.snmp.load()
        self._methods = {
            "create": snmp.communities_s.community.create,
            "read": snmp.communities_s.community.load,
            "update": snmp.communities_s.community.update,
            "delete": snmp.communities_s.community.delete,
            "exists": snmp.communities_s.community.exists,
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpSysSnmpCommunity(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
