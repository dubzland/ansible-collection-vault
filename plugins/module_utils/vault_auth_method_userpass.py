# -*- coding: utf-8 -*-

# Copyright: Josh Williams <jdubz@dubzland.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ._vault_common import VaultAuthMethod


class VaultAuthMethodUserpass(VaultAuthMethod):
    NAME = "userpass"
    AUTH_FIELDS = ["username", "password", "mount_point"]

    def validate(self):
        self.validate_required_fields(["username", "password"])

    def authenticate(self, client):
        params = self.login_params(*self.AUTH_FIELDS)
        client.auth.userpass.login(**params)
