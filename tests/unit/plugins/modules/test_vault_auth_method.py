# -*- coding: utf-8 -*-

# Copyright: Josh Williams <jdubz@dubzland.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
import requests_mock

from ansible_collections.dubzland.vault.plugins.modules.vault_auth_method import (
    VaultAuthMethod,
)


from ansible_collections.dubzland.vault.tests.unit.plugins.modules.utils import (
    ModuleTestCase,
    mock_list_auth_methods,
    mock_enable_auth_method,
    mock_tune_auth_method,
    mock_disable_auth_method,
)


class TestVaultAuthMethod(ModuleTestCase):
    def setUp(self):
        super(TestVaultAuthMethod, self).setUp()

        self.vault_instance.token = "test-auth-token"

        self.moduleUtil = VaultAuthMethod(
            module=self.mock_module, vault_instance=self.vault_instance
        )

    @pytest.fixture(autouse=True)
    def _mocker(self, mocker):
        self.mocker = mocker

    @requests_mock.Mocker()
    def test_auth_method_exists(self, m):
        mock_list_auth_methods(
            m,
            resp={"valid-method/": {"description": "Valid auth method", "config": {}}},
        )
        result = self.moduleUtil.exists_auth_method("valid-method")

        self.assertEqual(result, True)

        result = self.moduleUtil.exists_auth_method("invalid-method")

        self.assertEqual(result, False)

    @requests_mock.Mocker()
    def test_auth_method_create(self, m):
        auth_method = "new-method"
        description = "New auth method"

        mock_enable_auth_method(m, auth_method)
        mock_list_auth_methods(
            m, resp={auth_method + "/": {"description": description, "config": {}}}
        )

        result = self.moduleUtil.create_auth_method(
            auth_method, description=description
        )

        self.assertEqual(result.get("description"), description)

    @requests_mock.Mocker()
    def test_auth_method_update(self, m):
        auth_method = "auth-method"
        description = "Updated auth method"

        mock_tune_auth_method(m, auth_method)
        mock_list_auth_methods(
            m, resp={auth_method + "/": {"description": description, "config": {}}}
        )

        result = self.moduleUtil.update_auth_method(
            auth_method + "/", description=description
        )

        self.assertEqual(result.get("description"), description)

    @requests_mock.Mocker()
    def test_auth_method_delete(self, m):
        auth_method = "auth-method"

        mock_disable_auth_method(m, auth_method)

        result = self.moduleUtil.delete_auth_method(auth_method + "/")

        self.assertEqual(result, None)
