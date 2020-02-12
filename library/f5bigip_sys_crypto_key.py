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
module: f5bigip_sys_crypto_key
short_description: BIG-IP sys crypto key module
description:
    - Manage cryptographic keys and related objects on the BIG-IP system.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Eric Jacob (@erjac77)"
options:
    challenge_password:
        description:
            - Specifies the challenge password to create the certificate request key.
    command:
        description:
            - Specifies the command to execute.
        choices: ['install']
    consumer:
        description:
            - Specifies the system component by which a key and/or associated cryptographic file will be consumed.
        default: ltm
        choices: ['enterprise-manager', 'iquery', 'iquery-big3d', 'ltm', 'webserver']
    curve_name:
        description:
            - Specifies the curve name to be used in creation of elliptc curve (EC) key.
        default: prime256v1
        choices: ['prime256v1', 'secp384r1']
    from_editor:
        description:
            - Specifies that the key should be obtained from a text editor session.
    from_local_file:
        description:
            - Specifies a local file path from which a key is to be copied.
    from_url:
        description:
            - Specifies a URI which is to be used to obtain a key for import into the configuration of the system.
    key_size:
        description:
            - Specifies the size, in bits, of the key to be generated.
        choices: ['512', '1024', '2048', '4096']
    key_type:
        description:
            - Specifies the size, in bits, of the key to be generated.
        choices: ['dsa-private', 'ec-private', 'rsa-private']
    lifetime:
        description:
            - Specifies the certificate life time to be used in creation of the certificate associated with the given
              key.
        default: 365
    no_overwrite:
        description:
            - Specifies option of not overwriting a key if it is in the scope.
        default: true
        type: bool
    passphrase:
        description:
            - Specifies an optional passphrase with which the key has been protected.
    security_type:
        description:
            - Specifies the level of security used in storing the key in question.
extends_documentation_fragment:
    - f5_common
    - f5_name
    - f5_partition
    - f5_state
"""

EXAMPLES = """
- name: Install SYS Crypto Key from local file
  f5bigip_sys_crypto_key:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: example.localhost.key
    partition: Common
    from_local_file: /tmp/example.localhost.key
    state: present
  delegate_to: localhost

- name: Create SYS Crypto Key
  f5bigip_sys_crypto_key:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    name: example.localhost.key
    state: present
  delegate_to: localhost
"""

RETURN = """ # """

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.erjac77.network.f5.base import AnsibleF5Error
from ansible.module_utils.erjac77.network.f5.common import F5_NAMED_OBJ_ARGS
from ansible.module_utils.erjac77.network.f5.common import F5_PROVIDER_ARGS
from ansible.module_utils.erjac77.network.f5.bigip import F5BigIpNamedObject


class ModuleParams(object):
    @property
    def argument_spec(self):
        argument_spec = dict(
            consumer=dict(
                type="str",
                choices=[
                    "enterprise-manager",
                    "iquery",
                    "iquery-big3d",
                    "ltm",
                    "webserver",
                ],
            ),
            # create
            challenge_password=dict(type="str", no_log=True),
            curve_name=dict(type="str", choices=["prime256v1", "secp384r1"]),
            key_size=dict(type="str", choices=["512", "1024", "2048", "4096"]),
            key_type=dict(
                type="str", choices=["dsa-private", "ec-private", "rsa-private"]
            ),
            lifetime=dict(type="int"),
            passphrase=dict(type="str", no_log=True),
            security_type=dict(
                type="str", choices=["fips", "normal", "password", "nethsm"]
            ),
            # install
            command=dict(type="str", choices=["install"]),
            from_editor=dict(type="str"),
            from_local_file=dict(type="str"),
            from_url=dict(type="str"),
            no_overwrite=dict(type="bool"),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True

    @property
    def mutually_exclusive(self):
        return [["from_editor", "from_local_file", "from_url"]]


class F5BigIpSysCryptoKey(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            "create": self._api.tm.sys.crypto.keys.key.create,
            "read": self._api.tm.sys.crypto.keys.key.load,
            "update": self._api.tm.sys.crypto.keys.key.update,
            "delete": self._api.tm.sys.crypto.keys.key.delete,
            "exists": self._api.tm.sys.crypto.keys.key.exists,
            "exec_cmd": self._api.tm.sys.crypto.keys.exec_cmd,
        }

    def _install(self):
        """Upload the key on the BIG-IP system."""
        name = self._params["name"]
        param_set = {}

        if self._params["fromEditor"]:
            param_set = {"from-editor": self._params["fromEditor"]}
        if self._params["fromLocalFile"]:
            param_set = {"from-local-file": self._params["fromLocalFile"]}
        if self._params["fromUrl"]:
            param_set = {"from-url": self._params["fromUrl"]}

        if param_set:
            param_set.update({"name": name})
            if self._params["consumer"]:
                param_set.update({"consumer": self._params["consumer"]})
            if self._params["noOverwrite"]:
                param_set.update({"no-overwrite": self._params["noOverwrite"]})

            # Install the key
            self._methods["exec_cmd"]("install", **param_set)
        else:
            raise AnsibleF5Error(
                "Missing required parameter 'from-*' to install the key."
            )

        # Make sure it is installed
        if not self._exists():
            raise AnsibleF5Error("Failed to create the object.")

        return True

    def _present(self):
        has_changed = False

        if self._params["command"] == "install":
            if not self._exists() or (
                self._params["noOverwrite"] is not None
                and self._params["noOverwrite"] is False
            ):
                has_changed = self._install()
        else:
            if not self._exists():
                has_changed = self._create()

        return has_changed


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
        mutually_exclusive=params.mutually_exclusive,
    )

    try:
        obj = F5BigIpSysCryptoKey(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
