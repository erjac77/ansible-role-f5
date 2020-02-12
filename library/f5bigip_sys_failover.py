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
module: f5bigip_sys_failover
short_description: BIG-IP sys failover module
description:
    - Configures failover for a BIG-IP unit in a redundant system configuration..
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Gabriel Fortin (@GabrielFortin)"
options:
    offline:
        description:
            - Changes the status of a unit or cluster to Forced Offline.
        choices: ['false', 'true']
    online:
        description:
            - Changes the status of a unit or cluster from Forced Offline to either Active or Standby, depending upon
              the status of the other unit or cluster in a redundant system configuration.
        choices: ['false', 'true']
    standby:
        description:
            - Specifies that the active unit or cluster fails over to a Standby state, causing the standby unit or
              cluster to become Active.
        choices: ['false', 'true']
    traffic_group:
        description:
            - Specifies the traffic-group that should fail over to the Standby state, the traffic-group will become
              Active on another device.
extends_documentation_fragment:
    - f5_common
"""

EXAMPLES = """
- name: Run SYS Failover
  f5bigip_sys_failover:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    online: True
  delegate_to: localhost
"""

RETURN = """ # """

import re
import time

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six import iteritems
from ansible.module_utils.erjac77.network.f5.common import F5_PROVIDER_ARGS
from ansible.module_utils.erjac77.network.f5.bigip import F5BigIpUnnamedObject


class ModuleParams(object):
    @property
    def argument_spec(self):
        argument_spec = dict(
            online=dict(type="bool"),
            offline=dict(type="bool"),
            standby=dict(type="bool"),
            traffic_group=dict(type="str"),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpSysFailover(F5BigIpUnnamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "read": self._api.tm.sys.failover.load,
            "update": self._api.tm.sys.failover.update,
            "run": self._api.tm.sys.failover.exec_cmd,
        }

    def get_failover_state(self):
        return re.findall(
            "[A-z]+", self._methods["read"]().attrs["apiRawValues"]["apiAnonymous"]
        )[1]

    def flush(self):
        # Remove empty params
        params = dict((k, v) for k, v in iteritems(self._params) if v is not None)

        before = self.get_failover_state()

        self._methods["run"]("run", **params)
        time.sleep(0.3)

        if self.get_failover_state() != before:
            has_changed = True
        else:
            has_changed = False

        return {"Failover state": self.get_failover_state(), "changed": has_changed}


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        obj = F5BigIpSysFailover(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
