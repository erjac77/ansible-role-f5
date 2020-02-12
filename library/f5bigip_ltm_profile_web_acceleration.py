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
module: f5bigip_ltm_profile_web_acceleration
short_description: BIG-IP ltm profile web acceleration module
description:
    - Configures a Web Acceleration profile.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Gabriel Fortin (@GabrielFortin)"
options:
    applications:
        description:
            - Configures a list of applications assigned to this profile.
    cache_aging_rate:
        description:
            - Specifies how quickly the system ages a cache entry.
        default: 9
        choices: range(0,10)
    cache_client_cache_control_mode:
        description:
            - Specifies which cache disabling headers sent by clients the system ignores.
        default: all
        choices: ['all', 'max-age', 'none']
    cache_insert_age_header:
        description:
            - When enabled, inserts Age and Date headers in the response.
        default: enabled
        choices: ['disabled', 'enabled']
    cache_max_age:
        description:
            - Specifies how long the system considers the cached content to be valid.
        default: 3600
    cache_max_entries:
        description:
            - Specifies the maximum number of entries that can be in the WA cache.
        default: 10000
    cache_object_max_size:
        description:
            - Specifies the largest object that the system considers eligible for caching.
        default: 50000
    cache_object_min_size:
        description:
            - Specifies the smallest object that the system considers eligible for caching.
        default: 500
    cache_size:
        description:
            - Specifies the maximum size, in megabytes, for the WA cache.
        default: 100
    cache_uri_exclude:
        description:
            - Configures a list of Uniform Resource Identifiers (URIs) to exclude from the WA Cache.
    cache_uri_include:
        description:
            - Configures a list of URIs that are cacheable.
    cache_uri_include_override:
        description:
            - Configures a list of URIs that should be cached in the WA cache even though they would normally not be
              cached due to constraints defined by web-acceleration I(cache_object_max_size) or others.
    cache_uri_pinned:
        description:
            - Configures a list of URIs that are kept in the WA cache regardless the I(cache_max_age) or expiry
              settings.
    defaults_from:
        description:
            - Configures the profile that you want to use as the parent profile.
        default: webacceleration
    metadata_cache_max_size:
        description:
            - Specifies the maximum size of the metadata cache.
extends_documentation_fragment:
    - f5_common
    - f5_app_service
    - f5_name
    - f5_partition
    - f5_state
"""

EXAMPLES = """
- name: Create LTM Monitor Web Acceleration
  f5bigip_ltm_profile_web_acceleration:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    partition: Common
    name: my_web_acceleration_profile
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
            applications=dict(type="list"),
            cache_aging_rate=dict(type="int", choices=range(0, 10)),
            cache_client_cache_control_mode=dict(
                type="str", choices=["all", "max-age", "none"]
            ),
            cache_insert_age_header=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            cache_max_age=dict(type="int"),
            cache_max_entries=dict(type="int"),
            cache_object_max_size=dict(type="int"),
            cache_object_min_size=dict(type="int"),
            cache_size=dict(type="int"),
            cache_uri_exclude=dict(type="list"),
            cache_uri_include=dict(type="list"),
            cache_uri_include_override=dict(type="list"),
            cache_uri_pinned=dict(type="list"),
            defaults_from=dict(type="str"),
            metadata_cache_max_size=dict(type="int"),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpLtmProfileWebAcceleration(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "create": self._api.tm.ltm.profile.web_accelerations.web_acceleration.create,
            "read": self._api.tm.ltm.profile.web_accelerations.web_acceleration.load,
            "update": self._api.tm.ltm.profile.web_accelerations.web_acceleration.update,
            "delete": self._api.tm.ltm.profile.web_accelerations.web_acceleration.delete,
            "exists": self._api.tm.ltm.profile.web_accelerations.web_acceleration.exists,
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpLtmProfileWebAcceleration(
            check_mode=module.check_mode, **module.params
        )
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
