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

# Common choices
F5_ACTIVATION_CHOICES = ["enabled", "disabled"]
F5_POLAR_CHOICES = ["yes", "no"]
F5_SEVERITY_CHOICES = [
    "alert",
    "crit",
    "debug",
    "emerg",
    "err",
    "info",
    "notice",
    "warning",
]
F5_STATE_CHOICES = ["present", "absent"]
F5_SWITCH_CHOICES = ["on", "off"]

# Common arguments
F5_PROVIDER_ARGS = dict(
    provider=dict(type="dict", required=True),
    # server=dict(type="str", required=True),
    # server_port=dict(type="int", default=443),
    # user=dict(type="str", required=True),
    # password=dict(type="str", required=True, no_log=True),
    # validate_certs=dict(type="bool", default=False),
)
F5_NAMED_OBJ_ARGS = dict(
    name=dict(type="str", required=True),
    partition=dict(type="str", default="Common"),
    state=dict(type="str", choices=F5_STATE_CHOICES, default="present"),
    sub_path=dict(type="str"),
)
