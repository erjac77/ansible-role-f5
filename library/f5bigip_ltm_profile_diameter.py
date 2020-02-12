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
module: f5bigip_ltm_profile_diameter
short_description: BIG-IP ltm profile diameter module
description:
    - Configures a profile to manage Diameter network traffic.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Gabriel Fortin (@GabrielFortin)"
options:
    connection_prime:
        description:
            - When enabled, and the system receives a capabilities exchange request from the client, the system will
              establish connections and perform handshaking with all the servers prior to sending the capabilities
              exchange answer to the client.
        default: disabled
        choices: ['disabled', 'enabled']
    defaults_from:
        description:
            - Specifies the profile that you want to use as the parent profile.
        default: diameter
    destination_realm:
        description:
            - This attribute has been deprecated as of BIG-IP v11.
    handshake_timeout:
        description:
            - Specifies the handshake timeout in seconds.
        default: 10
        choices: range(0,4294967296)
    host_ip_rewrite:
        description:
            - When enabled and the message is a capabilities exchange request or capabilities exchange answer, rewrite
              the host-ip-address attribute with the system's egress IP address.
        default: enabled
        choices: ['disabled', 'enabled']
    max_retransmit_attempts:
        description:
            - Specifies the maximum number of retransmit attempts.
        default: 1
        choices: range(0,4294967296)
    max_watchdog_failure:
        description:
            - Specifies the maximum number of device watchdog failures that the traffic management system can take
              before it tears down the connection.
        default: 10
        choices: range(0,4294967296)
    origin_host_to_client:
        description:
            - Specifies the origin host to client of BIG-IP.
    origin_host_to_server:
        description:
            - Specifies the origin host to server of BIG-IP.
    origin_realm_to_client:
        description:
            - Specifies the origin realm of BIG-IP.
    origin_realm_to_server:
        description:
            - Specifies the origin realm to server of BIG-IP.
    overwrite_destination_host:
        description:
            - This attribute has been deprecated as of BIG-IP v11.
        default: enabled
        choices: ['disabled', 'enabled']
    parent_avp:
        description:
            - Specifies the name of the Diameter attribute that the system uses to indicate if the persist-avp option is
              embedded in a grouped avp.
        choices: range(0, 4294967296)
    persist_avp:
        description:
            - Specifies the name of the Diameter attribute that the system persists on.
    reset_on_timeout:
        description:
            - When it is enabled and the watchdog failures exceed the max watchdog failure, the system resets the
              connection.
        default: enabled
        choices: ['disabled', 'enabled']
    retransmit_timeout:
        description:
            - Specifies the retransmit timeout in seconds.
        default: 10
        choices: range(0, 4294967296)
    subscriber_aware:
        description:
            - When you enable this option, the system extracts available subscriber information, such as phone number or
              phone model, from diameter authentication and/or accounting packets.
        default: disabled
        choices: ['disabled', 'enabled']
    watchdog_timeout:
        description:
            - Specifies the watchdog timeout in seconds.
        default: 0
        choices: range(0, 4294967296)
extends_documentation_fragment:
    - f5_common
    - f5_app_service
    - f5_description
    - f5_name
    - f5_partition
    - f5_state
"""

EXAMPLES = """
- name: Create LTM Profile Diameter
  f5bigip_ltm_profile_diameter:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: my_diameter_profile
    partition: Common
    description: My diameter profile
    state: present
  delegate_to: localhost
"""

RETURN = """ # """

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six.moves import range
from ansible.module_utils.erjac77.network.f5.common import F5_ACTIVATION_CHOICES
from ansible.module_utils.erjac77.network.f5.common import F5_NAMED_OBJ_ARGS
from ansible.module_utils.erjac77.network.f5.common import F5_PROVIDER_ARGS
from ansible.module_utils.erjac77.network.f5.bigip import F5BigIpNamedObject


class ModuleParams(object):
    @property
    def argument_spec(self):
        argument_spec = dict(
            app_service=dict(type="str"),
            connection_prime=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            defaults_from=dict(type="str"),
            description=dict(type="str"),
            destination_realm=dict(type="str"),
            handshake_timeout=dict(type="int", choices=range(0, 4294967296)),
            host_ip_rewrite=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            max_retransmit_attempts=dict(type="int", choices=range(0, 4294967296)),
            max_watchdog_failure=dict(type="int", choices=range(0, 4294967296)),
            origin_host_to_client=dict(type="str"),
            origin_host_to_server=dict(type="str"),
            origin_realm_to_client=dict(type="str"),
            origin_realm_to_server=dict(type="str"),
            overwrite_destination_host=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            parent_avp=dict(type="str"),
            persist_avp=dict(type="str"),
            reset_on_timeout=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            retransmit_timeout=dict(type="int", choices=range(0, 4294967296)),
            subscriber_aware=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            watchdog_timeout=dict(type="int", choices=range(0, 4294967296)),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpLtmProfileDiameter(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "create": self._api.tm.ltm.profile.diameters.diameter.create,
            "read": self._api.tm.ltm.profile.diameters.diameter.load,
            "update": self._api.tm.ltm.profile.diameters.diameter.update,
            "delete": self._api.tm.ltm.profile.diameters.diameter.delete,
            "exists": self._api.tm.ltm.profile.diameters.diameter.exists,
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpLtmProfileDiameter(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
