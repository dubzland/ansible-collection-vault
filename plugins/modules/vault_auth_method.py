#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Josh Williams <jdubz@dubzland.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: vault_auth_method
short_description: Manages HashiCorp Vault authentication methods
description:
  - When the auth method does not exist, it will be created.
  - When the auth method does exist and O(state=absent), the auth method will be deleted.
  - When changes are made to the auth method, the auth method will be updated.
author:
  - Josh Williams (@t3hpr1m3)
requirements:
  - python >= 3.8
  - hvac >= 7.1.4
attributes:
  check_mode:
    support: full
    description: Can run in check_mode and return changed status prediction without modifying target.
  diff_mode:
    support: none
    description: Will return details on what has changed (or possibly needs changing in check_mode), when in diff mode.
options:
  method_type:
    type: str
    required: True
    description: Type of authentication method to be created
    choices:
      - token
      - userpass
      - approle
  path:
    type: str
    description: Path to the authentication method to be enabled.
  description:
    type: str
    description: Human readable description for the authentication method.
  config:
    type: dict
    suboptions:
      default_lease_ttl:
        type: str
        description: The default lease duration, specified as a string duration like "5s" or "30m".
      max_lease_ttl:
        type: str
        description: The maximum lease duration, specified as a string duration like "5s" or "30m".
      audit_non_hmac_request_keys:
        type: list
        elements: str
        description: List of keys that will not be HMAC'd by audit devices in the request data object.
      audit_non_hmac_response_keys:
        type: list
        elements: str
        description: List of keys that will not be HMAC'd by audit devices in the response data object.
      listing_visibility:
        type: list
        elements: str
        description: |
          Specifies whether to show this mount in the UI-specific listing endpoint. Valid values are
          "unauth" or "hidden", with the default "" being equivalent to "hidden".
      passthrough_request_headers:
        type: list
        elements: str
        description: List of headers to allow and pass from the request to the plugin.
      allowed_response_headers:
        type: list
        elements: str
        description: List of headers to allow, allowing a plugin to include them in the response.
      plugin_version:
        type: str
        description:
          - Specifies the semantic version of the plugin to use, e.g. "v1.0.0".
          - |
            If unspecified, the server will select any matching unversioned plugin that may have been
            registered, the latest versioned plugin registered, or a built-in plugin in that order of precedence.
      identity_token_key:
        type: str
        description: The key to use for signing plugin workload identity tokens. If not provided, this will default to Vault's OIDC default key.
    description: Configuration provided to the authentication method.
  state:
    description:
      - Indicates the desired authentication method state.
      - V(present) ensures the authentication method is present.
      - V(absent) ensures the authentication method is absent.
    default: present
    choices: [ "present", "absent" ]
    type: str
extends_documentation_fragment: dubzland.vault.hvac_auth
"""

EXAMPLES = """
- name: Enable AppRole authentication
  dubzland.vault.vault_auth_method:
    method_type: approle
    description: AppRole authentication
    state: present
    url: http://localhost:8200
    token: "{{ _root_token }}"
"""

RETURN = r"""
auth_method:
    description: Details about the authentication method
    type: dict
    returned: success
"""


from ansible_collections.dubzland.vault.plugins.module_utils.hashicorp_vault import (
    vault_client,
    vault_argument_spec,
    is_state_changed,
)

from ansible.module_utils.basic import AnsibleModule


class VaultAuthMethod(object):
    def __init__(self, module, vault_instance):
        self._module = module
        self._vault = vault_instance
        self.auth_method = None

    def exists_auth_method(self, path):
        response = self._vault.sys.list_auth_methods()
        auth_methods = response.get("data")
        return (path + "/") in auth_methods

    def create_auth_method(self, method_type, description=None, path=None, config=None):
        if path is None:
            path = method_type + "/"

        self._vault.sys.enable_auth_method(
            method_type, description=description, path=path, config=config
        )
        response = self._vault.sys.list_auth_methods()
        auth_method = response.get("data").get(path)
        return auth_method

    def update_auth_method(self, path, description=None, config=None):
        self._vault.sys.tune_auth_method(path, description=description, **config)
        response = self._vault.sys.list_auth_methods()
        auth_method = response.get("data").get(path)
        return auth_method

    def delete_auth_method(self, path):
        self._vault.sys.disable_auth_method(path)
        return None

    def create_or_update_auth_method(self, path, description, method_type, config):
        changed = False
        response = self._vault.sys.list_auth_methods()
        auth_methods = response.get("data")
        if (path + "/") in auth_methods:
            self.auth_method = auth_methods.get(path + "/")
            if description != self.auth_method["description"] or is_state_changed(
                config, self.auth_method["config"]
            ):
                if not self._module.check_mode:
                    self.auth_method = self.update_auth_method(
                        path, description=description, **config
                    )
                changed = True
        else:
            if not self._module.check_mode:
                self.auth_method = self.create_auth_method(
                    method_type, description=description, path=path, config=config
                )
            changed = True

        return changed


def main():
    argument_spec = vault_argument_spec(
        method_type=dict(
            type="str", choices=["token", "userpass", "approle"], required=True
        ),
        path=dict(type="str"),
        description=dict(type="str"),
        config=dict(
            type="dict",
            options=dict(
                default_lease_ttl=dict(type="str"),
                max_lease_ttl=dict(type="str"),
                audit_non_hmac_request_keys=dict(
                    type="list", elements="str", no_log=True
                ),
                audit_non_hmac_response_keys=dict(
                    type="list", elements="str", no_log=True
                ),
                listing_visibility=dict(type="list", elements="str"),
                passthrough_request_headers=dict(
                    type="list", elements="str", no_log=True
                ),
                allowed_response_headers=dict(type="list", elements="str"),
                plugin_version=dict(type="str"),
                identity_token_key=dict(type="str", no_log=True),
            ),
        ),
        state=dict(default="present", choices=["present", "absent"]),
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    path = module.params["path"]
    description = module.params["description"]
    method_type = module.params["method_type"]
    config = {}
    state = module.params["state"]

    if path is None:
        path = method_type

    client = vault_client(module)

    vault_auth_method = VaultAuthMethod(module, client)

    if state == "present":
        if vault_auth_method.create_or_update_auth_method(
            path, description, method_type, config
        ):
            module.exit_json(
                changed=True,
                msg="Successfully created or updated the authentication method %s"
                % path,
                auth_method=vault_auth_method.auth_method,
            )
        module.exit_json(
            changed=False,
            msg="No changes to authentication method %s" % path,
            auth_method=vault_auth_method.auth_method,
        )
    elif state == "absent":
        auth_method_exists = vault_auth_method.exists_auth_method(path)
        if auth_method_exists:
            vault_auth_method.delete_auth_method(path)
            module.exit_json(
                changed=True,
                msg="Successfuly deleted authentication method %s" % path,
                auth_method=vault_auth_method.auth_method,
            )
        else:
            module.exit_json(
                changed=False, msg="Authentication method %s does not exist" % path
            )


if __name__ == "__main__":
    main()
