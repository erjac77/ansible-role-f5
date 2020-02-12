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
module: f5bigip_facts
short_description: Gather facts from BIG-IP system
description:
    - Collect facts from BIG-IP system.
version_added: "1.0.0" # of erjac77.f5 role
author:
    - "Eric Jacob (@erjac77)"
options:
    component:
        description:
            - Specifies the component to collect.
        required: true
    expand_subcollections:
        description:
            - Specifies that iControl REST expand any references to sub collections when set to true/yes.
    filter:
        description:
            - Specifies an administrative partition to query for a result set.
    module:
        description:
            - Specifies the module.
        required: true
    namespaces:
        description:
            - Specifies the namespace of the request.
            - The default value is 'tm' (for traffic management).
        default: tm
    select:
        description:
            - Specifies a subset of the properties that will appear in the result set.
    sub_module:
        description:
            - Specifies the sub-module.
    skip:
        description:
            - Specifies the number of rows to skip in the result set.
    top:
        description:
            - Specifies the first N rows of the result set.
extends_documentation_fragment:
    - f5_common
"""

EXAMPLES = """
- name: Collect BIG-IP facts
  f5bigip_facts:
    provider:
      server: "{{ ansible_host }}"
      server_port: "{{ http_port | default(443) }}"
      user: "{{ http_user }}"
      password: "{{ http_pass }}"
      validate_certs: false
    module: ltm
    component: pool
    filter: partition eq Common
    select: name,partition
    expand_subcollections: yes
  delegate_to: localhost

- debug:
    msg: "{{ tm_ltm_pool['items']|map(attribute='name')|list }}"
"""

RETURN = """
ansible_facts.({namespace})_({module})(_{sub_module})?_({component}):
    description: Facts about BIG-IP components
    returned: On success
    type: complex
"""

from ansible.module_utils.basic import AnsibleModule, json
from ansible.module_utils.erjac77.network.f5.common import F5_PROVIDER_ARGS
from ansible.module_utils.six import iteritems, iterkeys
from ansible.module_utils.urls import open_url


def get_facts(uri, **params):
    rparams = dict()
    rq_subcol = params["expand_subcollections"]
    rq_filter = params["filter"]
    rq_select = params["select"]
    rq_skip = params["skip"]
    rq_top = params["top"]
    if rq_filter:
        rparams["filter"] = rq_filter.replace(" ", "+")
    if rq_select:
        if "name" not in rq_select:
            rq_select.append("name")
        rparams["select"] = rq_select
    if rq_skip:
        rparams["skip"] = rq_skip
    if rq_top:
        rparams["top"] = rq_top

    req_params = ""
    if rq_subcol:
        req_params += "?expandSubcollections=true"
    if rparams:
        if not req_params:
            req_params = "?"
        for k, v in iteritems(rparams):
            if len(req_params) > 1:
                req_params += "&"
            req_params += "$" + k + "=" + str(v)

    resp = open_url(
        "https://"
        + params["f5_hostname"]
        + ":"
        + str(params["f5_port"])
        + uri
        + req_params,
        method="GET",
        url_username=params["f5_username"],
        url_password=params["f5_password"],
        validate_certs=params["f5_verify"],
    )

    return json.loads(resp.read())


def convert_keys(data):
    for key in iterkeys(data):
        new_key = key.replace("-", "")
        if new_key != key:
            data[new_key] = data[key]
            del data[key]
    return data


class ModuleParams(object):
    @property
    def argument_spec(self):
        argument_spec = dict(
            component=dict(type="str", required=True),
            expand_subcollections=dict(type="bool"),
            filter=dict(type="str"),
            module=dict(type="str", required=True),
            namespace=dict(type="str", default="tm"),
            select=dict(type="str"),
            skip=dict(type="int"),
            sub_module=dict(type="str"),
            top=dict(type="int"),
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


def main():
    params = ModuleParams()
    module = AnsibleModule(
        argument_spec=params.argument_spec,
        supports_check_mode=params.supports_check_mode,
    )

    try:
        facts = {}

        resource = module.params["namespace"] + "/" + module.params["module"]
        if module.params["sub_module"] is not None:
            resource += "/" + module.params["sub_module"]
        resource += "/" + module.params["component"]

        facts[resource.replace("/", "_")] = get_facts(
            uri="/mgmt/" + resource + "/", **module.params
        )
        result = {"ansible_facts": convert_keys(facts)}
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
