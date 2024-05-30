# -*- coding: utf-8 -*-

# Copyright: Josh Williams <jdubz@dubzland.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule, missing_required_lib

from ansible_collections.dubzland.vault.plugins.module_utils._vault_connection_options import (
    VaultConnectionOptions,
)
from .vault_auth import (
    VaultAuth,
)

try:
    import hvac

    python_hvac_installed = True
except ImportError:
    python_hvac_installed = False


def ensure_hvac_package(module):
    if not python_hvac_installed:
        module.fail_json(
            msg=missing_required_lib(
                "hvac",
                url="https://hvac.readthedocs.io/en/stable/overview.html",
            ),
        )


class VaultModule(AnsibleModule):
    def __init__(self, *args, **kwargs):
        super(VaultModule, self).__init__(*args, **kwargs)

        self.connection_options = VaultConnectionOptions(self.params)
        self.authenticator = VaultAuth(self.params)

    @classmethod
    def generate_argument_spec(cls, **kwargs):
        spec = VaultConnectionOptions.ARGUMENT_SPEC.copy()
        spec.update(VaultAuth.ARGUMENT_SPEC.copy())
        spec.update(**kwargs)

        return spec

    def hvac_client(self):
        ensure_hvac_package(self)

        connection_params = self.connection_options.get_hvac_connection_params()
        client = hvac.Client(**connection_params)

        return client
