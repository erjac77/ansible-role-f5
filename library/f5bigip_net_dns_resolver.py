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
module: f5bigip_net_dns_resolver
short_description: BIG-IP net dns_resolver module
description:
    - Configures a DNS resolver on the BIG-IP system.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Gabriel Fortin (@GabrielFortin)"
options:
    answer_default_zones:
        description:
            - "Specifies whether the resolver answers queries for default zones: localhost, reverse 127.0.0.1 and ::1,
              and AS112 zones."
        default: no
        choices: ['yes', 'no']
    cache_size:
        description:
            - Specifies the maximum cache size in bytes of the DNS Resolver object.
        default: 5767168
    forward_zones:
        description:
            - Adds, deletes, modifies, or replaces a set of forward zones on a DNS Resolver, by specifying zone name(s).
    randomize_query_name_case:
        description:
            - Specifies whether the resolver randomizes the case of query names.
        default: yes
        choices: ['yes', 'no']
    route_domain:
        description:
            - Specifies the route domain the resolver uses for outbound traffic.
    use_ipv4:
        description:
            - Specifies whether the resolver sends DNS queries to IPv4 addresses.
        default: yes
        choices: ['yes', 'no']
    use_ipv6:
        description:
            - Specifies whether the resolver sends DNS queries to IPv6 addresses.
        default: yes
        choices: ['yes', 'no']
    use_tcp:
        description:
            - Specifies whether the resolver can send queries over the TCP protocol.
        default: yes
        choices: ['yes', 'no']
    use_udp:
        description:
            - Specifies whether the resolver can send queries over the UDP protocol.
        default: yes
        choices: ['yes', 'no']
extends_documentation_fragment:
    - f5_common
    - f5_name
    - f5_partition
    - f5_state
"""

EXAMPLES = """
- name: Create NET DNS Resolver
  f5bigip_net_dns_resolver:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: my_dns_resolver
    partition: Common
    use_ipv6: no
    state: present
  delegate_to: localhost
"""

RETURN = """ # """

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.erjac77.network.f5.common import F5_NAMED_OBJ_ARGS
from ansible.module_utils.erjac77.network.f5.common import F5_POLAR_CHOICES
from ansible.module_utils.erjac77.network.f5.common import F5_PROVIDER_ARGS
from ansible.module_utils.erjac77.network.f5.bigip import F5BigIpNamedObject


class ModuleParams(object):
    @property
    def argument_spec(self):
        argument_spec = dict(
            answer_default_zones=dict(type="str", choices=F5_POLAR_CHOICES),
            cache_size=dict(type="int"),
            # forward_zones=dict(type='list'),
            randomize_query_name_case=dict(type="str", choices=F5_POLAR_CHOICES),
            route_domain=dict(type="str"),
            use_ipv4=dict(type="str", choices=F5_POLAR_CHOICES),
            use_ipv6=dict(type="str", choices=F5_POLAR_CHOICES),
            use_tcp=dict(type="str", choices=F5_POLAR_CHOICES),
            use_udp=dict(type="str", choices=F5_POLAR_CHOICES),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpNetDnsResolver(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "create": self._api.tm.net.dns_resolvers.dns_resolver.create,
            "read": self._api.tm.net.dns_resolvers.dns_resolver.load,
            "update": self._api.tm.net.dns_resolvers.dns_resolver.update,
            "delete": self._api.tm.net.dns_resolvers.dns_resolver.delete,
            "exists": self._api.tm.net.dns_resolvers.dns_resolver.exists,
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpNetDnsResolver(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
