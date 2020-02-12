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
module: f5bigip_ltm_profile_radius
short_description: BIG-IP ltm profile radius module
description:
    - Configures a RADIUS profile for network traffic load balancing.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Gabriel Fortin (@GabrielFortin)"
options:
    clients:
        description:
            - Specifies host and network addresses from which clients can connect.
    defaults_from:
        description:
            - Specifies the profile that you want to use as the parent profile.
        default: radiusLB
    persist_avp:
        description:
            - Specifies the name of the RADIUS attribute on which traffic persists.
    subscriber_aware:
        description:
            - Specifies whether to extract subscriber information from RADIUS packets.
        default: disabled
        choices: ['disabled', 'enabled']
    subscriber_id_type:
        description:
            - Specifies the RADIUS attribute to be used as the subscriber Id when extracting subscriber information from
              the RADIUS message.
        default: 3gpp-imsi
        choices: ['3gpp-imsi', 'calling-station-id', 'user-name']
extends_documentation_fragment:
    - f5_common
    - f5_app_service
    - f5_description
    - f5_name
    - f5_partition
    - f5_state
"""

EXAMPLES = """
- name: Create LTM Profile RADIUS
  f5bigip_ltm_profile_radius:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: my_radius_profile
    partition: Common
    description: My radius profile
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
            app_service=dict(type="str"),
            clients=dict(type="str"),
            defaults_from=dict(type="str"),
            description=dict(type="str"),
            persist_avp=dict(type="str"),
            subscriber_aware=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            subscriber_id_type=dict(
                type="str", choices=["3gpp-imsi", "calling-station-id", "user-name"]
            ),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpLtmProfileRadius(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "create": self._api.tm.ltm.profile.radius_s.radius.create,
            "read": self._api.tm.ltm.profile.radius_s.radius.load,
            "update": self._api.tm.ltm.profile.radius_s.radius.update,
            "delete": self._api.tm.ltm.profile.radius_s.radius.delete,
            "exists": self._api.tm.ltm.profile.radius_s.radius.exists,
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpLtmProfileRadius(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
