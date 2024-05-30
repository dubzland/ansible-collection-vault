# -*- coding: utf-8 -*-

# Copyright: Josh Williams <jdubz@dubzland.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest

from .compat import mock


@pytest.fixture
def mock_module():
    module = mock.Mock()
    module.get_bin_path.return_value = "/mock/bin/testing"
    return module


@pytest.fixture
def hvac_client():
    return mock.MagicMock()


@pytest.fixture
def patch_hvac_client(hvac_client):
    with mock.patch(
        "ansible_collections.dubzland.vault.plugins.module_utils.vault_module.VaultModule.hvac_client",
        return_value=hvac_client,
    ):
        yield
