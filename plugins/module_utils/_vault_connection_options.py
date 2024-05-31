# -*- coding: utf-8 -*-

# Copyright: Josh Williams <jdubz@dubzland.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class VaultConnectionOptions(object):
    ARGUMENT_SPEC = dict(url=dict(type="str", required=True))

    def __init__(self, params):
        self.url = params.get("url")

    def get_hvac_connection_params(self):
        return dict(url=self.url)
