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

"""Ansible Utility Module for F5 iWorkflow
"""

import time

from ansible.module_utils.erjac77.network.f5.base import (
    AnsibleF5Error,
    F5BaseClient,
    F5NamedBaseObject,
    F5UnnamedBaseObject,
)

# Make sure the f5-sdk is installed on the host
try:
    from f5.bigip import ManagementRoot as iWfMgmtRoot

    HAS_F5SDK = True
except ImportError:
    HAS_F5SDK = False


class F5iWorkflowClient(F5BaseClient):
    """F5 iWorkflow client

    It provides an interface to a single F5 iWorkflow system.
    """

    def __init__(self, **kwargs):
        if not HAS_F5SDK:
            raise AnsibleF5Error(
                "The python f5-sdk module is required. Try 'pip install f5-sdk'."
            )
        self.provider = kwargs.get("provider", None)

    @property
    def mgmt_root(self):
        err = None
        retries = self.provider.get("retries", 3)
        timeout = self.provider.get("timeout", 10)

        for x in range(retries):
            try:
                return BigIpMgmtRoot(
                    self.provider["server"],
                    self.provider["user"],
                    self.provider["password"],
                    port=self.provider["server_port"],
                    verify=self.provider["validate_certs"],
                    token="local",
                )
            except Exception as exc:
                err = exc
                time.sleep(timeout)

        err_msg = "Unable to connect to host {0} on port {1}.".format(
            self.provider["server"], self.provider["server_port"]
        )
        if err is not None:
            err_msg += ' The error message was "{0}".'.format(str(err))
        raise AnsibleF5Error(err_msg)

    @property
    def _system_version(self):
        raise NotImplemented


class F5iWorkflowNamedObject(F5NamedBaseObject):
    """Base class for all F5 iWorkflow named objects"""

    @property
    def _api(self):
        return F5iWorkflowClient(provider=self._provider).mgmt_root


class F5iWorkflowUnnamedObject(F5UnnamedBaseObject):
    """Base class for all F5 iWorkflow unnamed objects"""

    @property
    def _api(self):
        return F5iWorkflowClient(provider=self._provider).mgmt_root
