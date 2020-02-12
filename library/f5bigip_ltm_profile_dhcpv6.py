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
module: f5bigip_ltm_profile_dhcpv6
short_description: BIG-IP ltm profile dhcpv6 module
description:
    - Configures a Dynamic Host Configuration Protocol for IPv6 (DHCPv6) profile.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Gabriel Fortin (@GabrielFortin)"
options:
    authentication:
        description:
            - Manages the subscriber authentication attributes.
        suboptions:
            enabled:
                description:
                    - To enable or disable subscriber authentication.
                default: false
                choices: ['true', 'false']
            user_name:
                description:
                    - Manages the authentication user name's attributes.
                suboptions:
                    format:
                        description:
                            - Specifies the user-name format.
                        choices: ['mac-address', 'mac-and-relay-id', 'tcl-snippet']
                    suboption_id1:
                        description:
                            - The relay-agent option (option 82) first suboption ID.
                        default: 1
                    suboption_id2:
                        description:
                            - The relay-agent option (option 82) second suboption ID.
                        default: 2
                    separator1:
                        description:
                            - A string that is used to concatenate the MAC address and the relay-agent info option
                              (option 82) to create the authentication user-name.
                        default: '@'
                    separator2:
                        description:
                            - A string that is used to concatenate the relay-agent info option (option 82) suboptions 1
                              and 2 to create the authentication user-name.
                        default: '@'
                    tcl_snippet:
                        description:
                            - A tcl snippet to format the user name.
            virtual:
                description:
                    - Specifies the authentication virtual server name.
    default_lease_time:
        description:
            - Provides the default value in seconds of DHCPv6 lease time in case it was missing in the client-server
              exchange.
        default: 86400
    defaults_from:
        description:
            - Specifies the profile that you want to use as the parent profile.
        default: dhcpv6
    idle_timeout:
        description:
            - Specifies the number of seconds that a connection is idle before the connection is eligible for deletion.
        default: 60
    mode:
        description:
            - Specifies the operation mode of the DHCP virtual.
        default: relay
        choices: ['relay', 'forwarding']
    remote_id_option:
        description:
            - Manages the DHCPv6 relay agent remote-id option (option 37) attributes.
        suboptions:
            add:
                description:
                    - Specifies if the user wants the DHCP relay agent to insert option 37 or not.
                default: false
                choices: ['true', 'false']
            remove:
                description:
                    - Specifies if the user wants the DHCP relay agent to remove option 37 from the server-to-client
                      traffic or not.
                default: false
                choices: ['true', 'false']
            enterprise_number:
                description:
                    - Specifies the enterprise number of the inserted remote-id option (option 37).
            value:
                description:
                    - A string to represent the remote-id option value.
    subscriber_discovery:
        description:
            - Manages the subscriber discovery attributes.
        suboptions:
            enabled:
                description:
                    - To enable or disable subscriber discovery.
                default: false
                choices: ['true', 'false']
            subscriber_id:
                description:
                    - Manages the subscriber-id attributes.
                suboptions:
                    format:
                        description:
                            - Specifies the user-name format.
                        choices: ['mac-address', 'mac-and-relay-id', 'tcl-snippet']
                    suboption_id1:
                        description:
                            - The relay-agent option (option 82) first suboption ID.
                        default: 1
                    suboption_id2:
                        description:
                            - The relay-agent option (option 82) second suboption ID.
                        default: 2
                    separator1:
                        description:
                            - A string that is used to concatenate the MAC address and the relay-agent info option
                              (option 82) to create the authentication user-name.
                        default: '@'
                    separator2:
                        description:
                            - A string that is used to concatenate the relay-agent info option (option 82) suboptions 1
                              and 2 to create the authentication user-name.
                        default: '@'
                    tcl_snippet:
                        description:
                            - A tcl snippet to format the user name.
    subscriber_id_option:
        description:
            - Manages the DHCPv6 relay agent subscriber-id option (option 38) attributes.
        suboptions:
            add:
                description:
                    - Specifies if the user wants the DHCP relay agent to insert option 38 or not.
                default: false
                choices: ['true', 'false']
            remove:
                description:
                    - Specifies if the user wants the DHCP relay agent to remove option 38 from the server-to-client
                      traffic or not.
                default: false
                choices: ['true', 'false']
            value:
                description:
                    - A string to represent the subscriber-id option value.
    transaction_timeout:
        description:
            - Specifies DHCPv6 transaction timeout, in seconds.
        default: 45
extends_documentation_fragment:
    - f5_common
    - f5_app_service
    - f5_description
    - f5_name
    - f5_partition
    - f5_state
"""

EXAMPLES = """
- name: Create LTM Profile DHCPv6
  f5bigip_ltm_profile_dhcpv6:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: my_dhcpv6_profile
    partition: Common
    description: My dhcpv6 profile
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
            app_service=dict(type="str"),
            authentication=dict(type="dict"),
            default_lease_time=dict(type="int"),
            defaults_from=dict(type="str"),
            description=dict(type="str"),
            idle_timeout=dict(type="int"),
            mode=dict(type="str", choices=["relay", "forwarding"]),
            remote_id_option=dict(type="dict"),
            subscriber_discovery=dict(type="dict"),
            subscriber_id_option=dict(type="dict"),
            transaction_timeout=dict(type="int"),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpLtmProfileDhcpv6(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "create": self._api.tm.ltm.profile.dhcpv6s.dhcpv6.create,
            "read": self._api.tm.ltm.profile.dhcpv6s.dhcpv6.load,
            "update": self._api.tm.ltm.profile.dhcpv6s.dhcpv6.update,
            "delete": self._api.tm.ltm.profile.dhcpv6s.dhcpv6.delete,
            "exists": self._api.tm.ltm.profile.dhcpv6s.dhcpv6.exists,
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpLtmProfileDhcpv6(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
