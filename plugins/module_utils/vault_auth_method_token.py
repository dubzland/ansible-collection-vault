# -*- coding: utf-8 -*-

# Copyright: Josh Williams <jdubz@dubzland.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os

from ._vault_common import VaultAuthMethod, VaultAuthenticationError


class VaultAuthMethodToken(VaultAuthMethod):
    NAME = "token"
    AUTH_FIELDS = ["token", "token_path", "token_filename", "token_validate"]

    def validate(self):
        if (
            self._options.get("token") is None
            and self._options.get("token_path") is not None
        ):
            token_filename = os.path.join(
                self._options.get("token_path"),
                self._options.get("token_filename"),
            )
            if os.path.exists(token_filename):
                if not os.path.isfile(token_filename):
                    raise VaultAuthenticationError(
                        "The Vault token file '%s' was found but is not a file."
                        % token_filename
                    )
                with open(token_filename) as token_file:
                    self._options["token"] = token_file.read().strip()

        if self._options.get("token") is None:
            raise VaultAuthenticationError("No Vault Token specified or discovered.")

    def authenticate(self, client, use_token=True):
        token = self._options.get("token")
        validate = self._options.get("token_validate")
        if use_token:
            client.token = token

            if validate:
                client.auth.token.lookup_self()
