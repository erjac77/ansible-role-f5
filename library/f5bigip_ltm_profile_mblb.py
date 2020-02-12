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
module: f5bigip_ltm_profile_mblb
short_description: BIG-IP ltm profile mblb module
description:
    - Configures an MBLB profile (experimental).
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Gabriel Fortin (@GabrielFortin)"
options:
    defaults_from:
        description:
            - Specifies the profile that you want to use as the parent profile.
        default: mblb
    egress_high:
        description:
            - Specify the high water mark for egress message queue.
        default: 50
    egress_low:
        description:
            - Specify the low water mark for egress message queue.
        default: 5
    ingress_high:
        description:
            - Specify the high water mark for ingress message queue.
        default: 50
    ingress_low:
        description:
            - Specify the low water mark for ingress message queue.
        default: 5
    isolate_abort:
        description:
            - Specify whether to isolate abort event propagation.
        choices: ['disabled', 'enabled']
    isolate_client:
        description:
            - Specify whether to isolate clientside shutdown event propagation.
        choices: ['disabled', 'enabled']
    isolate_expire:
        description:
            - Specify whether to isolate expiration event propagation.
        choices: ['disabled', 'enabled']
    isolate_server:
        description:
            - Specify whether to isolate serverside shutdown event propagation.
        choices: ['disabled', 'enabled']
    min_conn:
        description:
            - Specify the minimum number of serverside connections.
        default: 0
    shutdown_timeout:
        description:
            - Delays sending FIN when BIGIP receives the first FIN packet from either the client or the server.
        default: 5
    tag_ttl:
        description:
            - Specify the TTL (time to live) for message TAG.
        default: 60
extends_documentation_fragment:
    - f5_common
    - f5_app_service
    - f5_description
    - f5_name
    - f5_partition
    - f5_state
"""

EXAMPLES = """
- name: Create LTM Profile MBLB
  f5bigip_ltm_profile_mblb:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: my_mblb_profile
    partition: Common
    description: My mblb profile
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
            defaults_from=dict(type="str"),
            description=dict(type="str"),
            egress_high=dict(type="int"),
            egress_low=dict(type="int"),
            ingress_high=dict(type="int"),
            ingress_low=dict(type="int"),
            isolate_abort=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            isolate_client=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            isolate_expire=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            isolate_server=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            min_conn=dict(type="int"),
            shutdown_timeout=dict(type="int"),
            tag_ttl=dict(type="int"),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpLtmProfileMblb(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "create": self._api.tm.ltm.profile.mblbs.mblb.create,
            "read": self._api.tm.ltm.profile.mblbs.mblb.load,
            "update": self._api.tm.ltm.profile.mblbs.mblb.update,
            "delete": self._api.tm.ltm.profile.mblbs.mblb.delete,
            "exists": self._api.tm.ltm.profile.mblbs.mblb.exists,
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpLtmProfileMblb(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
