# -*- coding: utf-8 -*-

# Copyright: Josh Williams <jdubz@dubzland.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
import pytest

from ansible_collections.dubzland.vault.plugins.modules import vault_auth_method

pytestmark = pytest.mark.usefixtures(
    "patch_hvac_client",
)

from ansible_collections.dubzland.vault.tests.unit.plugins.modules.utils import (
    set_module_args,
)


@pytest.fixture
def module_args():
    return {
        "url": "http://localhost:8200",
        "token": "example-token",
        "method_type": "approle",
        "description": "Test AppRole authentication",
    }


@pytest.fixture
def create_args(module_args):
    args = module_args.copy()
    args.update({"state": "present"})
    return args


@pytest.fixture
def update_args(create_args):
    args = create_args.copy()
    args.update({"description": "Updated Description"})
    return args


@pytest.fixture
def delete_args(create_args):
    args = create_args.copy()
    args.update({"state": "absent"})
    return args


@pytest.fixture
def missing_json_response():
    return {"data": {}}


@pytest.fixture
def create_json_response(create_args):
    return {
        "data": {"approle/": {"description": create_args["description"], "config": {}}}
    }


@pytest.fixture
def update_json_response(update_args):
    return {"data": {"approle/": {"description": update_args["description"]}}}


class TestVaultAuthMethod:
    def test_vault_auth_method_create(
        self,
        create_args,
        missing_json_response,
        create_json_response,
        hvac_client,
        capfd,
    ):
        hvac_client.sys.list_auth_methods.side_effect = [
            missing_json_response,
            create_json_response,
        ]
        hvac_client.sys.enable_auth_method.return_value = {}

        set_module_args(create_args)
        with pytest.raises(SystemExit) as e:
            vault_auth_method.main()

        out, *rest = capfd.readouterr()
        result = json.loads(out)

        hvac_client.sys.enable_auth_method.assert_called_once_with(
            create_args["method_type"],
            description=create_args["description"],
            path="%s/" % create_args["method_type"],
            config={},
        )

        assert e.value.code == 0
        assert result["changed"] is True
        assert (
            result["msg"]
            == "Successfully created or updated the authentication method %s/"
            % create_args["method_type"]
        )
        auth_method = result["auth_method"]
        assert auth_method["description"] == create_args["description"]

    def test_vault_auth_method_update(
        self,
        update_args,
        create_json_response,
        update_json_response,
        hvac_client,
        capfd,
    ):
        hvac_client.sys.list_auth_methods.side_effect = [
            create_json_response,
            update_json_response,
        ]
        hvac_client.sys.tune_auth_method.return_value = {}

        set_module_args(update_args)
        with pytest.raises(SystemExit) as e:
            vault_auth_method.main()

        out, *rest = capfd.readouterr()
        result = json.loads(out)

        hvac_client.sys.tune_auth_method.assert_called_once_with(
            update_args["method_type"] + "/",
            description=update_args["description"],
        )

        assert e.value.code == 0
        assert result["changed"] is True
        assert (
            result["msg"]
            == "Successfully created or updated the authentication method %s/"
            % update_args["method_type"]
        )
        auth_method = result["auth_method"]
        assert auth_method["description"] == update_args["description"]

    def test_vault_auth_method_update_no_change(
        self,
        create_args,
        create_json_response,
        hvac_client,
        capfd,
    ):
        hvac_client.sys.list_auth_methods.side_effect = [
            create_json_response,
            create_json_response,
        ]
        hvac_client.sys.tune_auth_method.return_value = {}

        set_module_args(create_args)
        with pytest.raises(SystemExit) as e:
            vault_auth_method.main()

        out, *rest = capfd.readouterr()
        result = json.loads(out)

        hvac_client.sys.tune_auth_method.assert_not_called()

        assert e.value.code == 0
        assert result["changed"] is False
        assert (
            result["msg"]
            == "No changes to authentication method %s/" % create_args["method_type"]
        )
        auth_method = result["auth_method"]
        assert auth_method["description"] == create_args["description"]

    def test_vault_auth_method_delete(
        self,
        delete_args,
        create_json_response,
        hvac_client,
        capfd,
    ):
        hvac_client.sys.list_auth_methods.side_effect = [
            create_json_response,
        ]
        hvac_client.sys.disable_auth_method.return_value = {}

        set_module_args(delete_args)
        with pytest.raises(SystemExit) as e:
            vault_auth_method.main()

        out, *rest = capfd.readouterr()
        result = json.loads(out)

        hvac_client.sys.disable_auth_method.assert_called_once_with(
            delete_args["method_type"] + "/"
        )

        assert e.value.code == 0
        assert result["changed"] is True
        assert (
            result["msg"]
            == "Successfully deleted authentication method %s"
            % delete_args["method_type"]
            + "/"
        )

    def test_vault_auth_method_delete_nochange(
        self,
        delete_args,
        missing_json_response,
        hvac_client,
        capfd,
    ):
        hvac_client.sys.list_auth_methods.side_effect = [
            missing_json_response,
        ]
        hvac_client.sys.disable_auth_method.return_value = {}

        set_module_args(delete_args)
        with pytest.raises(SystemExit) as e:
            vault_auth_method.main()

        out, *rest = capfd.readouterr()
        result = json.loads(out)

        hvac_client.sys.disable_auth_method.assert_not_called()

        assert e.value.code == 0
        assert result["changed"] is False
        assert result["msg"] == "Authentication method %s deleted or does not exist" % (
            delete_args["method_type"] + "/"
        )
