# -*- coding: utf-8 -*-

# Copyright: Josh Williams <jdubz@dubzland.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class VaultAuthenticationError(ValueError):
    """Use in authentication code to raise an Exception that can be turned into AnsibleError or used to fail_json()"""


class VaultAuthMethod:
    NAME = None

    def __init__(self, options):
        self._options = options

    def validate_required_fields(self, *field_names):
        # raise Exception("options: %s" % self._options)
        missing = [field for field in field_names if self._options.get(field) is None]

        if missing:
            raise VaultAuthenticationError(
                "Authentication method %s requires options %r to be set, but these are missing: %r"
                % (self.NAME, field_names, missing)
            )

    def login_params(self, *field_names):
        params = {}
        for field in field_names:
            params = self._options[field]
        return params
