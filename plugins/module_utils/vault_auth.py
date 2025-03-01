# -*- coding: utf-8 -*-

# Copyright: Josh Williams <jdubz@dubzland.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type


from .vault_auth_method_approle import VaultAuthMethodApprole
from .vault_auth_method_aws_iam import VaultAuthMethodAwsIam
from .vault_auth_method_azure import VaultAuthMethodAzure
from .vault_auth_method_cert import VaultAuthMethodCert
from .vault_auth_method_jwt import VaultAuthMethodJwt
from .vault_auth_method_ldap import VaultAuthMethodLdap
from .vault_auth_method_none import VaultAuthMethodNone
from .vault_auth_method_token import VaultAuthMethodToken
from .vault_auth_method_userpass import VaultAuthMethodUserpass


class VaultAuth(object):
    ARGUMENT_SPEC = dict(
        auth_method=dict(
            type="str",
            default="token",
            choices=[
                "approle",
                "aws_iam",
                "azure",
                "cert",
                "jwt",
                "ldap",
                "token",
                "userpass",
                "none",
            ],
        ),
        mount_point=dict(type="str"),
        token=dict(type="str", no_log=True),
        token_path=dict(type="str", default=None, no_log=False),
        token_filename=dict(type="str", default=".vault-token"),
        token_validate=dict(type="bool", default=False),
        username=dict(type="str", no_log=True),
        password=dict(type="str", no_log=True),
        role_id=dict(type="str", no_log=True),
        secret_id=dict(type="str", no_log=True),
        jwt=dict(type="str", no_log=True),
        aws_profile=dict(type="str", aliases=["boto_profile"]),
        aws_access_key=dict(type="str", aliases=["aws_access_key_id"], no_log=False),
        aws_secret_key=dict(type="str", aliases=["aws_secret_access_key"], no_log=True),
        aws_security_token=dict(type="str", no_log=False),
        region=dict(type="str"),
        aws_iam_server_id=dict(type="str"),
        azure_tenant_id=dict(type="str"),
        azure_client_id=dict(type="str"),
        azure_client_secret=dict(type="str", no_log=True),
        azure_resource=dict(type="str", default="https://management.azure.com/"),
        cert_auth_private_key=dict(type="path", no_log=False),
        cert_auth_public_key=dict(type="path"),
    )

    def __init__(self, params):
        self._authenticators = {
            "approle": VaultAuthMethodApprole,
            "aws_iam": VaultAuthMethodAwsIam,
            "azure": VaultAuthMethodAzure,
            "cert": VaultAuthMethodCert,
            "jwt": VaultAuthMethodJwt,
            "ldap": VaultAuthMethodLdap,
            "none": VaultAuthMethodNone,
            "token": VaultAuthMethodToken,
            "userpass": VaultAuthMethodUserpass,
        }
        self._params = params
        self._authenticator = None

    def get_authenticator(self):
        if self._authenticator is None:
            auth_method = self._params.get("auth_method")
            self._authenticator = self._authenticators[auth_method](self._params)

        return self._authenticator

    def validate(self):
        self.get_authenticator().validate()

    def authenticate(self, client):
        self.get_authenticator().authenticate(client)
