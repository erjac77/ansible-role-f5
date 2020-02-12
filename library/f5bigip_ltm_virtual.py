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
module: f5bigip_ltm_virtual
short_description: BIG-IP ltm virtual server module
description:
    - Configures a virtual server.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Eric Jacob (@erjac77)"
options:
    address_status:
        description:
            - Specifies whether the virtual will contribute to the operational status of the associated virtual-address.
        default: yes
        choices: ['yes', 'no']
    all:
        description:
            - Specifies that you want to modify all of the existing components of the specified type.
        type: bool
    auth:
        description:
            - Specifies a list of authentication profile names, separated by spaces, that the virtual server uses to
              manage authentication.
    auto_lasthop:
        description:
            - Allows the BIG-IP system to track the source MAC address of incoming connections and return traffic from
              pools to the source MAC address, regardless of the routing table.
        default: default
        choices: ['default', 'enabled', 'disabled']
    cmp_enabled:
        description:
            - Enables or disables clustered multi-processor (CMP) acceleration.
        default: yes
        choices: ['yes', 'no']
    connection_limit:
        description:
            - Specifies the maximum number of concurrent connections you want to allow for the virtual server.
    destination:
        description:
            - Specifies the name of the virtual address and service on which the virtual server listens for connections.
        default: any:any
    dhcp_relay:
        description:
            - Specifies a virtual server that relays all received dhcp requests to all pool members.
    disabled:
        description:
            - Specifies the state of the virtual server.
        default: false
        type: bool
    enabled:
        description:
            - Specifies the state of the virtual server.
        default: true
        type: bool
    fallback_persistence:
        description:
            - Specifies a fallback persistence profile for the virtual server to use when the default persistence
              profile is not available.
    flow_eviction_policy:
        description:
            - Specifies a flow eviction policy for the virtual server to use, to select which flows to terminate when
              the number of connections approaches the connection limit on the virtual server.
    fw_enforced_policy:
        description:
            - Specifies an enforced firewall policy.
    fw_staged_policy:
        description:
            - Specifies a staged firewall policy.
    gtm_score:
        description:
            - Specifies a score that is associated with the virtual server.
    http_class:
        description:
            - Specifies a list of HTTP class profiles, separated by spaces, with which the virtual server works to
              increase the speed at which the virtual server processes HTTP requests.
    ip_forward:
        description:
            - Specifies a virtual server that has no pool members to load balance, but instead, forwards the packet
              directly to the destination IP address specified in the client request.
    ip_protocol:
        description:
            - Specifies the IP protocol for which you want the virtual server to direct traffic.
        default: any
    internal:
        description:
            - Specifies an internal virtual server that handles requests for a parent virtual server, such as content
              adaptation.
    l2_forward:
        description:
            - Specifies a virtual server that shares the same IP address as a node in an associated VLAN.
    last_hop_pool:
        description:
            - Specifies the name of the last hop pool that you want the virtual server to use to direct reply traffic to
              the last hop router.
    mask:
        description:
            - Specifies the netmask for a network virtual server only.
        default: 255.255.255.255 for IPv4 or ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff for IPv6
    mirror:
        description:
            - Enables or disables mirroring.
        choices: ['disabled', 'enabled', 'none']
    nat64:
        description:
            - Enable or disable NAT64.
        default: disabled
        choices: ['disabled', 'enabled']
    pool:
        description:
            - Specifies a default pool to which you want the virtual server to automatically direct traffic.
    rate_class:
        description:
            - Specifies the name of an existing rate class that you want the virtual server to use to enforce a
              throughput policy for incoming network traffic.
    rate_limit:
        description:
            - Specifies the maximum number of connections per second allowed for a virtual server.
    rate_limit_mode:
        description:
            - Indicates whether the rate limit is applied per virtual object, per source address, per destination
              address, or some combination thereof.
        default: object
        choices: [
            'destination', 'object', 'object-destination', 'object-source', 'object-source-destination', 'source',
            'source-destination'
        ]
    rate_limit_dst_mask:
        description:
            - Specifies a mask, in bits, to be applied to the destination address as part of the rate limiting.
        default: 0
    rate_limit_src_mask:
        description:
            - Specifies a mask, in bits, to be applied to the source address as part of the rate limiting.
        default: 0
    related_rules:
        description:
            - Specifies a list of iRules, that customize the behavior of secondary channels (for instance the data
              channel on FTP) opened on behalf of the virtual server.
    reject:
        description:
            - Specifies that the BIG-IP system rejects any traffic destined for the virtual server IP address.
        type: bool
    rules:
        description:
            - Specifies a list of iRules, that customize the virtual server to direct and manage traffic.
    source:
        description:
            - Specifies an IP address or network from which the virtual server will accept traffic.
    source_address_translation:
        description:
            - Specifies the type of source address translation enabled for the listener as well as the pool that the
              source address translation will use.
        suboptions:
            pool:
                description:
                    - Specifies the name of a SNAT pool used by the specified listener.
            type:
                description:
                    - Specifies the type of source address translation associated with the specified listener.
                choices: ['automap', 'lsn', 'none', 'snat']
    source_port:
        description:
            - Specifies whether the system preserves the source port of the connection.
        default: preserve
        choices: ['change', 'preserve', 'preserve-strict']
    traffic_classes:
        description:
            - Specifies a list of traffic classes that are associated with the virtual server.
    translate_address:
        description:
            - Enables or disables address translation for the virtual server.
        default: disabled.
        choices: ['enabled', 'disabled']
    translate_port:
        description:
            - Enables or disables port translation.
        default: disabled
        choices: ['enabled', 'disabled']
    vlans:
        description:
            - Specifies a list of VLANs on which the virtual server is either enabled or disabled.
    vlans_disabled:
        description:
            - Disables the virtual server on the VLANs specified in the vlans option.
        default: true
        type: bool
    vlans_enabled:
        description:
            - Enables the virtual server on the VLANs specified in the vlans option.
        default: false
        type: bool
extends_documentation_fragment:
    - f5_common
    - f5_app_service
    - f5_description
    - f5_name
    - f5_partition
    - f5_state
"""

EXAMPLES = """
- name: Create LTM Virtual Server
  f5bigip_ltm_virtual:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: my_http_vs
    description: my http vs
    partition: Common
    destination: 10.10.20.201:80
    state: present
  delegate_to: localhost
"""

RETURN = """ # """

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.erjac77.network.f5.common import F5_ACTIVATION_CHOICES
from ansible.module_utils.erjac77.network.f5.common import F5_NAMED_OBJ_ARGS
from ansible.module_utils.erjac77.network.f5.common import F5_POLAR_CHOICES
from ansible.module_utils.erjac77.network.f5.common import F5_PROVIDER_ARGS
from ansible.module_utils.erjac77.network.f5.bigip import F5BigIpNamedObject


class ModuleParams(object):
    @property
    def argument_spec(self):
        argument_spec = dict(
            all=dict(type="bool"),
            address_status=dict(type="str", choices=F5_POLAR_CHOICES),
            app_service=dict(type="str"),
            auth=dict(type="list"),
            auto_lasthop=dict(type="str", choices=["default", "enabled", "disabled"]),
            # clone_pools=dict(type='list'),
            cmp_enabled=dict(type="str", choices=F5_POLAR_CHOICES),
            connection_limit=dict(type="int"),
            description=dict(type="str"),
            destination=dict(type="str"),
            dhcp_relay=dict(type="bool"),
            disabled=dict(type="bool"),
            enabled=dict(type="bool"),
            fallback_persistence=dict(type="str"),
            flow_eviction_policy=dict(type="str"),
            fw_enforced_policy=dict(type="str"),
            # fw_rules=dict(type='list'),
            fw_staged_policy=dict(type="list"),
            gtm_score=dict(type="int"),
            http_class=dict(type="str"),
            ip_forward=dict(type="bool"),
            ip_protocol=dict(type="str"),
            internal=dict(type="bool"),
            l2_forward=dict(type="bool"),
            last_hop_pool=dict(type="str"),
            # metadata=dict(type='list'),
            mask=dict(type="str"),
            mirror=dict(type="str", choices=["disabled", "enabled", "none"]),
            nat64=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            persist=dict(type="list"),
            pool=dict(type="str"),
            rate_class=dict(type="str"),
            rate_limit=dict(type="int"),
            rate_limit_mode=dict(
                type="str",
                choices=[
                    "destination",
                    "object",
                    "object-destination",
                    "object-source",
                    "object-source-destination",
                    "source",
                    "source-destination",
                ],
            ),
            rate_limit_dst_mask=dict(type="int"),
            rate_limit_src_mask=dict(type="int"),
            related_rules=dict(type="str"),
            reject=dict(type="bool"),
            rules=dict(type="list"),
            source=dict(type="str"),
            source_address_translation=dict(type="dict"),
            source_port=dict(
                type="str", choices=["change", "preserve", "preserve-strict"]
            ),
            traffic_classes=dict(type="list"),
            translate_address=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            translate_port=dict(type="str", choices=F5_ACTIVATION_CHOICES),
            vlans=dict(type="list"),
            vlans_disabled=dict(type="bool"),
            vlans_enabled=dict(type="bool"),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True

    @property
    def mutually_exclusive(self):
        return [
            ["dhcp_relay", "ip_forward", "l2_forward", "reject"],
            ["enabled", "disabled"],
            ["vlans_enabled", "vlans_disabled"],
        ]


class F5BigIpLtmVirtual(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "create": self._api.tm.ltm.virtuals.virtual.create,
            "read": self._api.tm.ltm.virtuals.virtual.load,
            "update": self._api.tm.ltm.virtuals.virtual.update,
            "delete": self._api.tm.ltm.virtuals.virtual.delete,
            "exists": self._api.tm.ltm.virtuals.virtual.exists,
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
        mutually_exclusive=params.mutually_exclusive,
    )

    try:
        obj = F5BigIpLtmVirtual(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
