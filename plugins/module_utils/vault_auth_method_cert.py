# -*- coding: utf-8 -*-

# Copyright: Josh Williams <jdubz@dubzland.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ._vault_common import VaultAuthMethod


class VaultAuthMethodCert(VaultAuthMethod):
    NAME = "cert"
    AUTH_FIELDS = [
        "cert_auth_public_key",
        "cert_auth_private_key",
        "mount_point",
        "role_id",
    ]

    def validate(self):
        self.validate_required_fields(["cert_auth_public_key", "cert_auth_private_key"])

    def authenticate(self, client):
        opts = self.login_params(*self.AUTH_FIELDS)

        params = {
            "cert_pem": opts["cert_auth_public_key"],
            "key_pem": opts["cert_auth_private_key"],
        }

        if "mount_point" in opts:
            params["mount_point"] = opts["mount_point"]
        if "role_id" in opts:
            params["name"] = opts["role_id"]

        client.auth.cert.login(**params)
