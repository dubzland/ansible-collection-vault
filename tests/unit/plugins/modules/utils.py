# -*- coding: utf-8 -*-

# Copyright: Josh Williams <jdubz@dubzland.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json

from ansible_collections.dubzland.vault.tests.unit.compat import unittest
from ansible_collections.dubzland.vault.tests.unit.compat.mock import patch, MagicMock
from ansible.module_utils import basic
from ansible.module_utils.common.text.converters import to_bytes
from functools import wraps
import hvac


class AnsibleExitJson(Exception):
    """Exception class to be raised by module.exit_json and caught by the test case"""

    pass


class AnsibleFailJson(Exception):
    """Exception class to be raised by module.fail_json and caught by the test case"""

    pass


def set_module_args(args):
    """prepare arguments so that they will be picked up during module creation"""
    args = json.dumps({"ANSIBLE_MODULE_ARGS": args})
    basic._ANSIBLE_ARGS = to_bytes(args)


def exit_json(*args, **kwargs):
    """function to patch over exit_json; package return data into an exception"""
    if "changed" not in kwargs:
        kwargs["changed"] = False
    raise AnsibleExitJson(kwargs)


def fail_json(*args, **kwargs):
    """function to patch over fail_json; package return data into an exception"""
    kwargs["failed"] = True
    raise AnsibleFailJson(kwargs)


def get_bin_path(self, arg, required=False):
    """Mock AnsibleModule.get_bin_path"""
    if arg.endswith("mc"):
        return "/usr/local/bin/mc"
    else:
        if required:
            fail_json(msg="%r not found !" % arg)


def mock_list_auth_methods(mocker, resp=None):
    mocker.get("http://localhost:8200/v1/sys/auth", json={"data": resp})


def mock_enable_auth_method(mocker, method, resp=None):
    mocker.post("http://localhost:8200/v1/sys/auth/%s" % method, json=resp)


def mock_tune_auth_method(mocker, method, resp=None):
    mocker.post("http://localhost:8200/v1/sys/auth/%s/tune" % method, json=resp)


def mock_disable_auth_method(mocker, method, resp=None):
    mocker.delete("http://localhost:8200/v1/sys/auth/%s" % method, json=resp)


def with_mock_client(module_name):
    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            with patch(
                "ansible_collections.dubzland.vault.plugins.modules.%s.vault_client"
                % module_name
            ) as mock_client:
                mock_sys = MagicMock()
                client = MagicMock()
                client.sys = mock_sys
                mock_client.return_value = client
                newargs = args + (client,)
                return func(*newargs, **kwargs)

        return inner

    return decorator


class ModuleTestCase(unittest.TestCase):
    def setUp(self):
        self.mock_module = patch.multiple(
            basic.AnsibleModule,
            exit_json=exit_json,
            fail_json=fail_json,
        )
        self.mock_module.start()
        self.addCleanup(self.mock_module.stop)
        self.vault_instance = hvac.Client(url="http://localhost:8200")
