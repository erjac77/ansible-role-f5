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

"""Ansible Utility Module for F5 systems

This module provides utility classes to ease the interaction between Ansible and F5 systems.
"""

from abc import ABCMeta, abstractmethod

import requests
from ansible.module_utils.six import iteritems, with_metaclass
from deepdiff import DeepDiff
from requests.exceptions import HTTPError
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from ansible.module_utils.erjac77.network.f5.utils import (
    camel_to_snake,
    change_dict_naming_convention,
    convert,
    missing_required_params,
    snake_to_camel,
)

# Disable Insecure Request Warning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class AnsibleF5Error(Exception):
    pass


class F5BaseClient(with_metaclass(ABCMeta)):
    """Base class for all F5 clients

    It provides an interface to a single F5 system.
    """

    @property
    @abstractmethod
    def mgmt_root(self):
        """Get the Management Root.

        Any class inheriting from F5BaseClient should implement and override this method.
        """
        pass

    @property
    @abstractmethod
    def _system_version(self):
        """Get the version of the F5 system.

        Any class inheriting from F5BaseClient should implement and override this method.
        """
        pass


class F5BaseObject(with_metaclass(ABCMeta)):
    """Base abstract class for all F5 objects

    It represents an F5 resource configurable by Ansible.
    """

    def __init__(self, **kwargs):
        """Prepare the parameters needed by this module."""
        super(F5BaseObject, self).__init__()

        # Required params
        self._required_create_params = set()
        self._required_load_params = set()
        self._required_update_params = set()

        # Store and remove BIG-IP and Ansible params
        self._provider = kwargs.pop("provider", None)
        self._state = kwargs.pop("state", None)
        self._check_mode = kwargs.pop("check_mode", None)
        self._tr = kwargs.pop("tr", None)

        # Change Snake to Camel naming convention of the params that are sent to the module
        self._params = change_dict_naming_convention(kwargs, snake_to_camel)

        # Set CRUD methods
        self._methods = {}
        self._set_crud_methods()

        # Set exclude paths
        self._exclude_paths = {}

        # Translate conflictual params (eg 'state')
        if self._tr is not None:
            for k, v in iteritems(self._tr):
                kc = snake_to_camel(k)
                if kc in self._params:
                    self._params[snake_to_camel(v)] = self._params[kc]
                    del self._params[kc]

        # Call property objects
        for k in self._params:
            try:
                ks = camel_to_snake(k)
                if getattr(self, ks) is not None:
                    self._params[k] = getattr(self, ks)
            except AttributeError:
                pass

        # The object
        self._obj = None

    @abstractmethod
    def _set_crud_methods(self):
        """Set the CRUD methods for this object.

        Any class inheriting from F5BaseObject should implement and override this method.
        """
        pass

    def _check_create_params(self):
        """Params given to create should satisfy required params."""
        check = missing_required_params(self._required_create_params, self._params)
        if check:
            raise AnsibleF5Error("Missing required create params: %s" % check)

    def _check_load_params(self):
        """Params given to load should satisfy required params."""
        check = missing_required_params(self._required_load_params, self._params)
        if check:
            raise AnsibleF5Error("Missing required load params: %s" % check)

    def _check_update_params(self):
        """Params given to update should satisfy required params."""
        check = missing_required_params(self._required_update_params, self._params)
        if check:
            raise AnsibleF5Error("Missing required update params: %s" % check)

    @abstractmethod
    def _read(self):
        """Load an already configured object from the F5 system.

        Any class inheriting from F5BaseObject should implement and override this method.
        """
        pass

    def _update(self):
        """Update an object on the F5 system."""
        # Load the object
        self._obj = self._read()

        # Check params
        self._check_update_params()

        changed = False
        cparams = {}  # The params that have changed

        # Merge exclude paths
        exclude_paths = {
            r"root['nameReference']",
        }
        if self._exclude_paths:
            exclude_paths.update(self._exclude_paths)

        # Determine if some params have changed
        for key, new_val in iteritems(self._params):
            if new_val is not None:
                if hasattr(self._obj, key):
                    cur_val = convert(getattr(self._obj, key))
                    ddiff = DeepDiff(
                        cur_val,
                        new_val,
                        ignore_order=True,
                        exclude_regex_paths=exclude_paths,
                    )
                    if ddiff:
                        cparams[key] = new_val
                else:
                    if new_val:
                        cparams[key] = new_val

        # If changed params, update the object
        if cparams:
            changed = True

            if self._check_mode:
                return changed

            if "modify" in self._methods:
                self._obj.modify(**cparams)
            else:
                self._obj.update(**cparams)
            self._obj.refresh()

        return changed

    @abstractmethod
    def flush(self):
        """Send the buffered object to the F5 system.

        Any class inheriting from F5BaseObject should implement and override this method."""
        pass


class F5NamedBaseObject(F5BaseObject):
    """Base abstract class for all F5 named objects"""

    def _set_crud_methods(self):
        raise NotImplemented

    def _exists(self):
        """Check for the existence of the named object on the F5 system."""
        try:
            return self._methods["exists"](**self._get_resource_id_from_params())
        except HTTPError:
            return False

    def _read(self):
        """Load an already configured object from the F5 system."""
        self._check_load_params()
        obj = self._methods["read"](**self._get_resource_id_from_params())

        for attr, value in vars(obj).items():
            if isinstance(value, list):
                if all(isinstance(val, dict) for val in value):
                    for key in value:
                        if "nameReference" in key:
                            del key["nameReference"]

        return obj

    def _create(self):
        """Create an object on the F5 system."""
        # Remove empty params
        params = dict((k, v) for k, v in iteritems(self._params) if v is not None)

        # Check params
        self._check_create_params()

        if self._check_mode:
            return True

        # Create the object
        self._methods["create"](**params)

        # Make sure it is created
        if self._exists():
            return True
        else:
            raise AnsibleF5Error("Failed to create the object.")

    def _delete(self):
        """Delete an object on the F5 system."""
        # Load the object
        self._obj = self._read()

        if self._check_mode:
            return True

        # Delete the object
        self._obj.delete()

        # Make sure it is gone
        if self._exists():
            raise AnsibleF5Error("Failed to delete the object.")

        return True

    def _present(self):
        if self._exists():
            has_changed = self._update()
        else:
            has_changed = self._create()

        return has_changed

    def _absent(self):
        has_changed = False

        if self._exists():
            has_changed = self._delete()

        return has_changed

    def flush(self):
        """Send the buffered object to the F5 system, depending upon the state of the object."""
        result = dict(changed=False)

        if self._state == "present":
            result["changed"] = self._present()
        elif self._state == "absent":
            result["changed"] = self._absent()

        return result

    def _strip_partition(self, name):
        partition_prefix = "/{0}/".format(self._params["partition"])
        return str(name.replace(partition_prefix, ""))

    def _get_resource_id_from_params(self):
        res_id_args = {"name": self._params["name"]}

        if "partition" in self._params and self._params["partition"] is not None:
            res_id_args.update({"partition": self._params["partition"]})
        if "subPath" in self._params and self._params["subPath"] is not None:
            res_id_args.update({"subPath": self._params["subPath"]})

        return res_id_args

    def _get_resource_id_from_path(self, path):
        res_id_args = {}
        path_segments = path.strip("/").split("/")

        if len(path_segments) == 1:
            res_id_args.update({"name": path_segments[0]})
            if "partition" in self._params and self._params["partition"] is not None:
                res_id_args.update({"partition": self._params["partition"]})
        elif len(path_segments) == 2:
            res_id_args.update({"partition": path_segments[0]})
            res_id_args.update({"name": path_segments[1]})
        elif len(path_segments) == 3:
            res_id_args.update({"partition": path_segments[0]})
            res_id_args.update({"subPath": path_segments[1]})
            res_id_args.update({"name": path_segments[2]})
        else:
            raise AnsibleF5Error("Invalid resource id.")

        return res_id_args


class F5UnnamedBaseObject(F5BaseObject):
    """Base abstract class for all F5 unnamed objects

    These objects do not support create or delete.
    """

    def _set_crud_methods(self):
        raise NotImplemented

    def _read(self):
        """Load an already configured object from the F5 system."""
        self._check_load_params()
        return self._methods["read"]()

    def flush(self):
        """Send the buffered object to the F5 system."""
        result = dict(changed=False)
        result["changed"] = self._update()
        return result
