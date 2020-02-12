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
module: f5bigip_ltm_persistence_hash
short_description: BIG-IP ltm persistence hash module
description:
    - You can use the hash component to configure a hash persistence profile for the BIG-IP system.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Gabriel Fortin (@GabrielFortin)"
options:
    defaults_from:
        description:
            - Specifies the existing profile from which the system imports settings for the new profile.
        default: hash
    hash_algorithm:
        description:
            - Specifies the system uses hash persistence load balancing.
        default: default
        choices: ['carp', 'default']
    hash_buffer_limit:
        description:
            - Specifies the maximum buffer length the system collects to locate the hashing pattern for hash persistence
              load balancing.
        default: 0
    hash_end_pattern:
        description:
            - Specifies the string that describes the ending location of the hash pattern that the system uses to
              perform hash persistence load balancing.
    hash_length:
        description:
            - Specifies the length of data within the packet in bytes that the system uses to calculate the hash value
              when performing hash persistence load balancing.
        default: 0
    hash_offset:
        description:
            - Specifies the start offset within the packet from which the system begins the hash when performing hash
              persistence load balancing.
        default: 0
    hash_start_pattern:
        description:
            - Specifies the string that describes the start location of the hash pattern that the system uses to perform
              hash persistence load balancing.
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
    rule:
        description:
            - Specifies a rule name, if you are using a rule for universal persistence.
    timeout:
        description:
            - Specifies the duration of the persistence entries.
        default: 180
extends_documentation_fragment:
    - f5_common
    - f5_app_service
    - f5_description
    - f5_name
    - f5_partition
    - f5_state
"""

EXAMPLES = """
- name: Create LTM Hash Persistence profile
  f5bigip_ltm_persistence_hash:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: my_hash_persistence
    partition: Common
    description: My hash persistence profile
    defaults_from: hash
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
            hash_algorithm=dict(type="str", choices=["carp", "default"]),
            hash_buffer_limit=dict(type="int"),
            hash_end_pattern=dict(type="str"),
            hash_length=dict(type="int"),
            hash_offset=dict(type="int"),
            hash_start_pattern=dict(type="str"),
            match_across_pools=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            match_across_services=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            match_across_virtuals=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            mirror=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            override_connection_limit=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            rule=dict(type="str"),
            timeout=dict(type="int"),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpLtmPersistenceHash(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "create": self._api.tm.ltm.persistence.hashs.hash.create,
            "read": self._api.tm.ltm.persistence.hashs.hash.load,
            "update": self._api.tm.ltm.persistence.hashs.hash.update,
            "delete": self._api.tm.ltm.persistence.hashs.hash.delete,
            "exists": self._api.tm.ltm.persistence.hashs.hash.exists,
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpLtmPersistenceHash(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
