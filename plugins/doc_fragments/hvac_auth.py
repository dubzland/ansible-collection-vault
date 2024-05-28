# -*- coding: utf-8 -*-

# Copyright: Josh Williams <jdubz@dubzland.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = """
options:
  auth_method:
    type: str
    description:
      - Authentication method to be used.
      - C(none) auth method was added in collection version C(1.2.0).
      - C(cert) auth method was added in collection version C(1.4.0).
      - C(aws_iam_login) was renamed C(aws_iam) in collection version C(2.1.0) and was removed in C(3.0.0).
      - C(azure) auth method was added in collection version C(3.2.0).
    choices:
      - token
      - userpass
      - ldap
      - approle
      - aws_iam
      - azure
      - jwt
      - cert
      - none
    default: token
  mount_point:
    type: str
    description:
      - Vault mount point.
      - If not specified, the default mount point for a given auth method is used.
      - Does not apply to token authentication.
  token:
    type: str
    description:
      - Vault token. Token may be specified explicitly, through the listed [env] vars, and also through the C(VAULT_TOKEN) env var.
      - If no token is supplied, explicitly or through env, then the plugin will check for a token file, as determined by I(token_path) and I(token_file).
      - The order of token loading (first found wins) is C(token param -> ansible var -> ANSIBLE_HASHI_VAULT_TOKEN -> VAULT_TOKEN -> token file).
  username:
    type: str
    description: Authentication user name.
  password:
    type: str
    description: Authentication password.
  role_id:
    type: str
    description:
      - Vault Role ID or name. Used in C(approle), C(aws_iam), C(azure) and C(cert) auth methods.
      - For C(cert) auth, if no I(role_id) is supplied, the default behavior is to try all certificate roles and return any one that matches.
      - For C(azure) auth, I(role_id) is required.
  secret_id:
    type: str
    description: Secret ID to be used for Vault AppRole authentication.
  url:
    type: str
    required: true
    description: The resolvable endpoint for the Vault API.
"""
