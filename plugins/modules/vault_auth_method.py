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
extends_documentation_fragment:
  - dubzland.vault.auth
  - dubzland.vault.connection
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


from ansible_collections.dubzland.vault.plugins.module_utils.vault_utils import (
    is_state_changed,
)
from ansible_collections.dubzland.vault.plugins.module_utils.vault_module import (
    VaultModule,
)


def main():
    argument_spec = VaultModule.generate_argument_spec(
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
    module = VaultModule(argument_spec=argument_spec, supports_check_mode=True)

    path = module.params["path"]
    description = module.params["description"]
    method_type = module.params["method_type"]
    config = module.params["config"]
    state = module.params["state"]
    changed = False
    exists = False

    if path is None:
        path = method_type + "/"
    if config is None:
        config = {}

    client = module.hvac_client()
    module.authenticator.validate()
    module.authenticator.authenticate(client)

    response = client.sys.list_auth_methods()
    auth_methods = response.get("data")
    if (path) in auth_methods:
        auth_method = auth_methods.get(path)
        exists = True

    if state == "present":
        if exists:
            if description != auth_method["description"] or is_state_changed(
                config, auth_method["config"]
            ):
                if not module.check_mode:
                    client.sys.tune_auth_method(path, description=description, **config)
                changed = True
        else:
            if not module.check_mode:
                client.sys.enable_auth_method(
                    method_type, description=description, path=path, config=config
                )
            changed = True

        if changed:
            response = client.sys.list_auth_methods()
            auth_method = response.get("data").get(path)
            module.exit_json(
                changed=True,
                msg="Successfully created or updated the authentication method %s"
                % path,
                auth_method=auth_method,
            )

        module.exit_json(
            changed=False,
            msg="No changes to authentication method %s" % path,
            auth_method=auth_method,
        )
    elif state == "absent":
        if exists:
            if not module.check_mode:
                client.sys.disable_auth_method(path)

            module.exit_json(
                changed=True,
                msg="Successfully deleted authentication method %s" % path,
                auth_method=auth_method,
            )

        module.exit_json(
            changed=False,
            msg="Authentication method %s deleted or does not exist" % path,
        )


if __name__ == "__main__":
    main()
