# -*- coding: utf-8 -*-

# Copyright: Josh Williams <jdubz@dubzland.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ._vault_common import VaultAuthMethod, VaultAuthenticationError


class VaultAuthMethodAzure(VaultAuthMethod):
    NAME = "azure"
    AUTH_FIELDS = [
        "role_id",
        "jwt",
        "mount_point",
        "azure_tenant_id",
        "azure_client_id",
        "azure_client_secret",
        "azure_resource",
    ]

    def validate(self):
        params = {
            "role": self._options.get("role_id"),
            "jwt": self._options.get("jwt"),
        }
        if not params["role"]:
            raise VaultAuthenticationError(
                "role_id is required for azure authentication."
            )

        mount_point = self._options.get("mount_point")
        if mount_point:
            params["mount_point"] = mount_point

        if not params["jwt"]:
            azure_tenant_id = self._options.get("azure_tenant_id")
            azure_client_id = self._options.get("azure_client_id")
            azure_client_secret = self._options.get("azure_client_secret")

            azure_resource = self._options.get("azure_resource")
            azure_scope = azure_resource + "/.default"

            try:
                import azure.identity
            except ImportError:
                raise VaultAuthenticationError(
                    "azure-identity is required for getting access token from azure service principal or managed identity."
                )

            if azure_client_id and azure_client_secret:
                if not azure_tenant_id:
                    raise VaultAuthenticationError(
                        "azure_tenant_id is required when using azure service principal."
                    )
                azure_credentials = azure.identity.ClientSecretCredential(
                    azure_tenant_id, azure_client_id, azure_client_secret
                )
            elif azure_client_id:
                azure_credentials = azure.identity.ManagedIdentityCredential(
                    client_id=azure_client_id
                )
            else:
                azure_credentials = azure.identity.ManagedIdentityCredential()

            params["jwt"] = azure_credentials.get_token(azure_scope).token

        self._auth_azure_login_params = params

    def authenticate(self, client, use_token=True):
        params = self._auth_azure_login_params
        client.auth.azure.login(use_token=use_token, **params)
