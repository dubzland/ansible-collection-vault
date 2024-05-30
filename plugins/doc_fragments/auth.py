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
    choices:
      - approle
      - aws_iam
      - azure
      - cert
      - jwt
      - ldap
      - token
      - userpass
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
  token_path:
    description: If no token is specified, will try to read the I(token_filename) from this path.
    type: str
  token_filename:
    description: If no token is specified, will try to read the token from this file in I(token_path).
    default: '.vault-token'
    type: str
  token_validate:
    description:
      - For token auth, will perform a C(lookup-self) operation to determine the token's validity before using it.
      - Disable if your token does not have the C(lookup-self) capability.
    type: bool
    default: false
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
  jwt:
    description: The JSON Web Token (JWT) to use for JWT authentication to Vault.
    type: str
  aws_profile:
    description: The AWS profile
    type: str
    aliases: [ boto_profile ]
  aws_access_key:
    description: The AWS access key to use.
    type: str
    aliases: [ aws_access_key_id ]
  aws_secret_key:
    description: The AWS secret key that corresponds to the access key.
    type: str
    aliases: [ aws_secret_access_key ]
  aws_security_token:
    description: The AWS security token if using temporary access and secret keys.
    type: str
  region:
    description: The AWS region for which to create the connection.
    type: str
  aws_iam_server_id:
    description: If specified, sets the value to use for the C(X-Vault-AWS-IAM-Server-ID) header as part of C(GetCallerIdentity) request.
    required: False
    type: str
  azure_tenant_id:
    description:
      - The Azure Active Directory Tenant ID (also known as the Directory ID) of the service principal. Should be a UUID.
      - >-
        Required when using a service principal to authenticate to Vault,
        e.g. required when both I(azure_client_id) and I(azure_client_secret) are specified.
      - Optional when using managed identity to authenticate to Vault.
    required: False
    type: str
  azure_client_id:
    description:
      - The client ID (also known as application ID) of the Azure AD service principal or managed identity. Should be a UUID.
      - If not specified, will use the system assigned managed identity.
    required: False
    type: str
  azure_client_secret:
    description: The client secret of the Azure AD service principal.
    required: False
    type: str
  azure_resource:
    description: The resource URL for the application registered in Azure Active Directory. Usually should not be changed from the default.
    required: False
    type: str
    default: https://management.azure.com/
  cert_auth_public_key:
    description: For C(cert) auth, path to the certificate file to authenticate with, in PEM format.
    type: path
  cert_auth_private_key:
    description: For C(cert) auth, path to the private key file to authenticate with, in PEM format.
    type: path
"""
