#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Josh Williams <jdubz@dubzland.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: vault_approle
short_description: Manages HashiCorp Vault approles
description:
  - When the AppRole does not exist, it will be created.
  - When the AppRole does exist and O(state=absent), it will be deleted.
  - When changes are made to the AppRole, the AppRole will be updated in-place.
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
  name:
    type: str
    required: true
    description: Name associated with this AppRole.
  bind_secret_id:
    type: bool
    description: Require V(secret_id) to be presented when logging in using this approle.
  secret_id_bound_cidrs:
    type: list
    elements: str
    description: Blocks of IP addresses which can perform login operations.
  secret_id_num_uses:
    type: int
    descripiton: Number of times any secret_id can be used to fetch a token. A value of zero allows unlimited uses.
  secret_id_ttl:
    type: str
    description: Duration after which a secret_id expires. This can be specified as an integer number of seconds or as a duration value like “5m”.
  enable_local_secret_ids:
    type: bool
    description: Secret IDs generated using role will be cluster local.
  token_ttl:
    type: str
    description: Incremental lifetime for generated tokens. This can be specified as an integer number of seconds or as a duration value like “5m”.
  token_max_ttl:
    type: str
    description: Maximum lifetime for generated tokens: This can be specified as an integer number of seconds or as a duration value like “5m”.
  token_policies:
    type: list
    elements: str
    description: List of policies to encode onto generated tokens.
  token_bound_cidrs:
    type: list
    elements: str
    description: Blocks of IP addresses which can authenticate successfully.
  token_explicit_max_ttl:
    type: str
    description: If set, will encode an explicit max TTL onto the token. This can be specified as an integer number of seconds or as a duration value like “5m”.
  token_no_default_policy:
    type: bool
    description: Do not add the default policy to generated tokens, use only tokens specified in token_policies.
  token_num_uses:
    type: int
    description: Maximum number of times a generated token may be used. A value of zero allows unlimited uses.
  token_period:
    type: str
    description: The period, if any, to set on the token. This can be specified as an integer number of seconds or as a duration value like “5m”.
  token_type:
    type: str
    description: The type of token that should be generated.
    choices:
      - default
      - batch
      - service
  mount_point:
    type: str
    description: The “path” the method/backend was mounted on.
  state:
    description:
      - Indicates the desired approle state.
      - V(present) ensures the approle is present.
      - V(absent) ensures the approle is absent.
    default: present
    choices: [ "present", "absent" ]
    type: str
extends_documentation_fragment:
  - dubzland.vault.auth
  - dubzland.vault.connection
"""

EXAMPLES = """
- name: Add AppRole login
  dubzland.vault.vault_approle:
    method_type: approle
    description: AppRole authentication
    state: present
    url: http://localhost:8200
    token: "{{ _root_token }}"
"""

from ansible_collections.dubzland.vault.plugins.module_utils.vault_utils import (
    get_keys_updated,
    is_state_changed,
)
from ansible_collections.dubzland.vault.plugins.module_utils.vault_module import (
    VaultModule,
)
from hvac import exceptions


APPROLE_ATTRS = [
    "bind_secret_id",
    "secret_id_bound_cidrs",
    "secret_id_num_uses",
    "secret_id_ttl",
    "enable_local_secret_ids",
    "token_ttl",
    "token_max_ttl",
    "token_policies",
    "token_bound_cidrs",
    "token_explicit_max_ttl",
    "token_no_default_policy",
    "token_num_uses",
    "token_period",
    "token_type",
]


def main():
    argument_spec = VaultModule.generate_argument_spec(
        name=dict(type="str", required=True),
        bind_secret_id=dict(type="bool", default=True),
        secret_id_bound_cidrs=dict(type="list", elements="str"),
        secret_id_num_uses=dict(type="int", default=0),
        secret_id_ttl=dict(type="str", default="0"),
        enable_local_secret_ids=dict(type="bool", default=False),
        token_ttl=dict(type="str", default="0"),
        token_max_ttl=dict(type="str", default="0"),
        token_policies=dict(type="list", elements="str", default=[]),
        token_bound_cidrs=dict(type="list", elements="str", default=[]),
        token_explicit_max_ttl=dict(type="str", default="0"),
        token_no_default_policy=dict(type="bool", default=False),
        token_num_uses=dict(type="int", default=0),
        token_period=dict(type="str", default="0"),
        token_type=dict(
            type="str", choices=["default", "batch", "service"], default="default"
        ),
        mount_point=dict(type="str", default="approle"),
        state=dict(default="present", choices=["present", "absent"]),
    )
    module = VaultModule(argument_spec=argument_spec, supports_check_mode=True)

    name = module.params["name"]
    mount_point = module.params["mount_point"]
    state = module.params["state"]
    changed = False
    changes = {}
    exists = False

    client = module.hvac_client()
    module.authenticator.validate()
    module.authenticator.authenticate(client)

    try:
        response = client.auth.approle.read_role(name, mount_point=mount_point)
        approle = response.get("data")
        exists = True
    except exceptions.InvalidPath:
        exists = False

    if state == "present":
        attrs = {}
        for field in APPROLE_ATTRS:
            attrs[field] = module.params[field]

        current_state = attrs.copy()
        current_state["local_secret_ids"] = current_state.pop("enable_local_secret_ids")

        if exists:
            if is_state_changed(current_state, approle):
                changes = get_keys_updated(current_state, approle)
                if not module.check_mode:
                    client.auth.approle.create_or_update_approle(
                        name, mount_point=mount_point, **attrs
                    )
                changed = True
        else:
            if not module.check_mode:
                client.auth.approle.create_or_update_approle(
                    name, mount_point=mount_point, **attrs
                )
            changed = True

        if changed:
            response = client.auth.approle.read_role(name, mount_point=mount_point)
            approle = response.get("data")
            module.exit_json(
                changed=True,
                msg="Successfully created or updated the approle %s" % name,
                approle=approle,
                changes=changes,
            )

        module.exit_json(
            changed=False,
            msg="No changes to approle %s" % name,
            approle=approle,
        )
    elif state == "absent":
        if exists:
            if not module.check_mode:
                client.auth.approle.delete_role(name, mount_point=mount_point)

            module.exit_json(
                changed=True,
                msg="Successfully deleted approle %s" % name,
                approle=approle,
            )

        module.exit_json(
            changed=False,
            msg="AppRole %s deleted or does not exist" % name,
        )


if __name__ == "__main__":
    main()
