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

"""Helper functions for the F5 Ansible Utility Module
"""

import collections
import re

from ansible.module_utils.six import iteritems, iterkeys, string_types


def missing_required_params(rq_set, params):
    key_set = set(list(iterkeys(params)))
    required_minus_received = rq_set - key_set

    if required_minus_received != set():
        return list(required_minus_received)


def camel_to_snake(name):
    camel_pat = re.compile(r"([A-Z])")
    return camel_pat.sub(lambda x: "_" + x.group(1).lower(), name)


def snake_to_camel(name):
    under_pat = re.compile(r"_([a-z])")
    return under_pat.sub(lambda x: x.group(1).upper(), name)


def change_dict_naming_convention(d, convert_fn):
    new = {}

    for k, v in iteritems(d):
        new_v = v
        new[convert_fn(k)] = new_v

    return new


def convert(data):
    if isinstance(data, string_types):
        return str(data.strip())
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, iteritems(data)))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data


def to_lines(stdout):
    for item in stdout:
        if isinstance(item, string_types):
            item = str(item).split("\n")
        yield item
