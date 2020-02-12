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


class ModuleDocFragment(object):
    # F5 common documentation fragment
    DOCUMENTATION = """
options:
    provider:
        description:
            - Connection details.
        type: dict
        suboptions:
            server:
                description: The BIG-IP host.
                required: true
            server_port:
                description: The BIG-IP server port.
                default: 443
            user:
                description: The username to connect to the BIG-IP.
                required: true
            password:
                description: The password to connect to the BIG-IP.
                required: true
            validate_certs:
                description: If C(false), SSL certificates are not validated.
                type: bool
                default: false
requirements:
    - Ansible >= 2.8.0 (ansible)
    - F5 Python SDK >= 3.0.21 (f5-sdk)
    - Deep Difference >= 4.2.0 (deepdiff)
    - Requests: HTTP for Humans >= 2.22.0 (requests)
notes:
    - Requires BIG-IP software version >= 12.0.
"""
