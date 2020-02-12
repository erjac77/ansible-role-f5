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
module: f5bigip_ltm_profile_dns
short_description: BIG-IP ltm profile dns module
description:
    - Configures a Domain Name System (DNS) profile.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Gabriel Fortin (@GabrielFortin)"
options:
    avr_dnsstat_sample_rate:
        description:
            - Sets AVR DNS statistics rate.
        default: 0
    defaults_from:
        description:
            - Specifies the profile that you want to use as the parent profile.
        default: dns
    dns64:
        description:
            - Specifies DNS64 mapping IPv6 prefix.
        default: disabled
        choices: ['disabled', 'secondary', 'immediate', 'v4-only']
    dns64_additional_section_rewrite:
        description:
            - Sets DNS64 additional section rewriting.
        default: disabled
        choices: ['disabled', 'v6-only', 'v4-only', 'any']
    dns64_prefix:
        description:
            - Specifies DNS64 mapping IPv6 prefix.
    enable_dns_express:
        description:
            - Indicates whether the dns-express service is enabled.
        choices: ['no', 'yes']
    enable_dnssec:
        description:
            - Indicates whether to perform DNS Security Extension (DNSSEC) operations on the DNS packet, for example,
              respond to DNSKEY queries; add RRSIGs to response.
        choices: ['no', 'yes']
    enable_gtm:
        description:
            - Indicates whether the Global Traffic Manager handles DNS resolution for DNS queries and responses that
              contain Wide IP names.
        default: yes
        choices: ['no', 'yes']
    enable_logging:
        description:
            - Indicates whether to enable high speed logging for DNS queries and responses or not.
        default: no
        choices: ['no', 'yes']
    enable_rapid_response:
        description:
            - Indicates whether to allow queries to be answered by Rapid Response.
        default: no
        choices: ['no', 'yes']
    log_profile:
        description:
            - Specifies the DNS logging profile used to configure what events get logged and their message format.
    process_rd:
        description:
            - Indicates whether to process clientside DNS packets with Recursion Desired set in the header.
        choices: ['no', 'yes']
    rapid_response_last_action:
        description:
            - Specifies what action to take when Rapid Response is enabled and the incoming query has not matched a
              DNS-Express Zone.
        choices: ['allow', 'drop', 'noerror', 'nxdomain', 'refuse', 'truncate']
    unhandled_query_action:
        description:
            - Specifies the action to take when a query does not match a Wide IP or a DNS Express Zone.
        choices: ['allow', 'drop', 'hint', 'noerror', 'reject']
    use_local_bind:
        description:
            - Indicates whether non-GTM and non-dns-express requests should be forwarded to the local BIND.
        choices: ['no', 'yes']
extends_documentation_fragment:
    - f5_common
    - f5_app_service
    - f5_description
    - f5_name
    - f5_partition
    - f5_state
"""

EXAMPLES = """
- name: Create LTM Profile DNS
  f5bigip_ltm_profile_dns:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: my_dns_profile
    partition: Common
    description: My dns profile
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
            app_service=dict(type="str"),
            avr_dnsstat_sample_rate=dict(type="int"),
            defaults_from=dict(type="str"),
            description=dict(type="str"),
            dns64=dict(
                type="str", choices=["disabled", "secondary", "immediate", "v4-only"]
            ),
            dns64_additional_section_rewrite=dict(
                type="str", choices=["disabled", "v6-only", "v4-only", "any"]
            ),
            dns64_prefix=dict(type="str"),
            enable_dns_express=dict(type="str", choices=F5_POLAR_CHOICES),
            enable_dnssec=dict(type="str", choices=F5_POLAR_CHOICES),
            enable_gtm=dict(type="str", choices=F5_POLAR_CHOICES),
            enable_logging=dict(type="str", choices=F5_POLAR_CHOICES),
            enable_rapid_response=dict(type="str", choices=F5_POLAR_CHOICES),
            log_profile=dict(type="str"),
            process_rd=dict(type="str", choices=F5_POLAR_CHOICES),
            rapid_response_last_action=dict(
                type="str",
                choices=["allow", "drop", "noerror", "nxdomain", "refuse", "truncate"],
            ),
            unhandled_query_action=dict(
                type="str", choices=["allow", "drop", "hint", "noerror", "reject"]
            ),
            use_local_bind=dict(type="str", choices=F5_POLAR_CHOICES),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpLtmProfileDns(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "create": self._api.tm.ltm.profile.dns_s.dns.create,
            "read": self._api.tm.ltm.profile.dns_s.dns.load,
            "update": self._api.tm.ltm.profile.dns_s.dns.update,
            "delete": self._api.tm.ltm.profile.dns_s.dns.delete,
            "exists": self._api.tm.ltm.profile.dns_s.dns.exists,
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpLtmProfileDns(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
