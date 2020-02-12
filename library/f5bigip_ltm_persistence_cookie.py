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
module: f5bigip_ltm_persistence_cookie
short_description: BIG-IP ltm persistence cookie module
description:
    - Configures a cookie persistence profile.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Eric Jacob (@erjac77)"
options:
    always_send:
        description:
            - Send the cookie persistence entry on every reply, even if the entry has previously been supplied to the
              client.
        default: disabled
        choices: ['enabled', 'disabled']
    cookie_name:
        description:
            - Specifies a unique name for the cookie.
    cookie_encryption:
        description:
            - Specifies the way in which cookie format will be used.
        default: required
        choices: ['required', 'preferred', 'disabled']
    cookie_encryption_passphrase:
        description:
            - Specifies a passphrase to be used for cookie encryption.
    defaults_from:
        description:
            - Specifies the existing profile from which the system imports settings for the new profile.
        default: cookie
    expiration:
        description:
            - Specifies the cookie expiration date in the format d:h:m:s, h:m:s, m:s or seconds.
        default: session cookie
    hash_length:
        description:
            - Specifies the cookie hash length.
        default: 0
    hash_offset:
        description:
            - Specifies the cookie hash offset.
        default: 0
    match_across_pools:
        description:
            - Specifies, when enabled, that the system can use any pool that contains this persistence record.
        default: disabled
        choices: ['enabled', 'disabled']
    match_across_services:
        description:
            - Specifies, when enabled, that all persistent connections from a client IP address, which go to the same
              virtual IP address, also go to the same node.
        default: disabled
        choices: ['enabled', 'disabled']
    match_across_virtuals:
        description:
            - Specifies, when enabled, that all persistent connections from the same client IP address go to the same
              node.
        default: disabled
        choices: ['enabled', 'disabled']
    method:
        description:
            - Specifies the type of cookie processing that the system uses.
        default: insert
        choices: ['hash', 'insert', 'passive', 'rewrite']
    mirror:
        description:
            - Specifies whether the system mirrors persistence records to the high-availability peer.
        default: disabled
        choices: ['enabled', 'disabled']
    override_connection_limit:
        description:
            - Specifies, when enabled, that the pool member connection limits are not enforced for persisted clients.
        default: disabled
        choices: ['enabled', 'disabled']
    timeout:
        description:
            - Specifies the duration of the persistence entries.
        default: 0
extends_documentation_fragment:
    - f5_common
    - f5_app_service
    - f5_description
    - f5_name
    - f5_partition
    - f5_state
"""

EXAMPLES = """
- name: Create LTM Cookie Persistence profile
  f5bigip_ltm_persistence_cookie:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: my_cookie_persistence
    partition: Common
    description: My cookie persistence profile
    defaults_from: /Common/cookie
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
            always_send=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            app_service=dict(type="str"),
            cookie_name=dict(type="str"),
            cookie_encryption=dict(
                type="str", choices=["required", "preferred", "disabled"]
            ),
            cookie_encryption_passphrase=dict(type="str", no_log=True),
            defaults_from=dict(type="str"),
            description=dict(type="str"),
            expiration=dict(type="str"),
            hash_length=dict(type="int"),
            hash_offset=dict(type="int"),
            match_across_pools=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            match_across_services=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            match_across_virtuals=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            method=dict(type="str", choices=["hash", "insert", "passive", "rewrite"]),
            mirror=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            override_connection_limit=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            timeout=dict(type="int"),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpLtmPersistenceCookie(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "create": self._api.tm.ltm.persistence.cookies.cookie.create,
            "read": self._api.tm.ltm.persistence.cookies.cookie.load,
            "update": self._api.tm.ltm.persistence.cookies.cookie.update,
            "delete": self._api.tm.ltm.persistence.cookies.cookie.delete,
            "exists": self._api.tm.ltm.persistence.cookies.cookie.exists,
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpLtmPersistenceCookie(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
