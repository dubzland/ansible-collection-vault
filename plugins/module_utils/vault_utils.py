# -*- coding: utf-8 -*-

# Copyright: Josh Williams <jdubz@dubzland.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

# import sys
#
# from urllib.parse import urlparse

from ansible.module_utils.basic import missing_required_lib


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


def vault_client(module):
    ensure_hvac_package(module)

    params = module.params

    url = params.get("url")
    client = hvac.Client(url=url)

    auth_method = params.get("auth_method")
    login_mount_point = params.get("login_mount_point", auth_method)
    if not login_mount_point:
        login_mount_point = auth_method

    if auth_method == "token":
        token = params.get("token")
        client.token = token
    elif auth_method == "userpass":
        username = params.get("username")
        password = params.get("password")
        client.auth.userpass.login(username, password, mount_point=login_mount_point)
    elif auth_method == "approle":
        role_id = params.get("role_id")
        secret_id = params.get("secret_id")
        client = AppRoleClient(
            client, role_id, secret_id, mount_point=login_mount_point
        )

    return client


class AppRoleClient(object):
    """
    hvac.Client decorator which generates and sets a new approle token on every
    function call. This allows multiple calls to Vault without having to manually
    generate and set a token on every Vault call.
    """

    def __init__(self, client, role_id, secret_id, mount_point):
        object.__setattr__(self, "client", client)
        object.__setattr__(self, "role_id", role_id)
        object.__setattr__(self, "secret_id", secret_id)
        object.__setattr__(self, "login_mount_point", mount_point)

    def __setattr__(self, name, val):
        """
        sets attribute in decorated class (Client)
        """
        client = object.__getattribute__(self, "client")
        client.__setattr__(name, val)

    def __getattribute__(self, name):
        """
        generates and sets new approle token in decorated class (Client)
        returns decorated class (Client) attribute
        """
        client = object.__getattribute__(self, "client")
        attr = client.__getattribute__(name)

        role_id = object.__getattribute__(self, "role_id")
        secret_id = object.__getattribute__(self, "secret_id")
        login_mount_point = object.__getattribute__(self, "login_mount_point")
        resp = client.auth.approle.login(
            role_id, secret_id=secret_id, mount_point=login_mount_point
        )
        client.token = str(resp["auth"]["client_token"])
        return attr


def _compare_state(desired_state, current_state, ignore=None):
    """Compares desired state to current state. Returns true if objects are equal

    Recursively walks dict object to compare all keys

    :param desired_state: The state user desires.
    :param current_state: The state that currently exists.
    :param ignore: Ignore these keys.
    :type ignore: list

    :return: True if the states are the same.
    :rtype: bool
    """

    if ignore is None:
        ignore = []
    if isinstance(desired_state, list):
        if (not isinstance(current_state, list)) or (
            len(desired_state) != len(current_state)
        ):
            return False
        for i in range(len(desired_state)):
            if not _compare_state(desired_state[i], current_state[i]):
                return False
        return True

    if isinstance(desired_state, dict):
        if not isinstance(current_state, dict):
            return False

        # iterate over dictionary keys
        for key in desired_state.keys():
            if key in ignore:
                continue
            v = desired_state[key]
            if (key not in current_state) or (
                not _compare_state(v, current_state.get(key))
            ):
                return False
        return True

    # lots of things get handled as strings in ansible that aren't necessarily strings, can extend this list later.
    if isinstance(desired_state, str) and isinstance(current_state, int):
        current_state = str(current_state)

    return desired_state == current_state


def _convert_to_seconds(original_value):
    try:
        value = str(original_value)
        seconds = 0
        if "h" in value:
            ray = value.split("h")
            seconds = int(ray.pop(0)) * 3600
            value = "".join(ray)
        if "m" in value:
            ray = value.split("m")
            seconds += int(ray.pop(0)) * 60
            value = "".join(ray)
        if value:
            ray = value.split("s")
            seconds += int(ray.pop(0))
        return seconds
    except Exception:
        pass
    return original_value


def get_keys_updated(desired_state, current_state, ignore=None):
    """Return list of keys that have different values

    Recursively walks dict object to compare all keys

    :param desired_state: The state user desires.
    :type desired_state: dict
    :param current_state: The state that currently exists.
    :type current_state: dict
    :param ignore: Ignore these keys.
    :type ignore: list

    :return: Different items
    :rtype: list
    """

    if ignore is None:
        ignore = []

    differences = []
    for key in desired_state.keys():
        if key in ignore:
            continue
        if key not in current_state:
            differences.append(key)
            continue
        new_value = desired_state[key]
        old_value = current_state[key]
        if "ttl" in key:
            if _convert_to_seconds(old_value) != _convert_to_seconds(new_value):
                differences.append(key)
        elif not _compare_state(new_value, old_value):
            differences.append(key)
    return differences


def is_state_changed(desired_state, current_state):
    """Return list of keys that have different values

    Recursively walks dict object to compare all keys

    :param desired_state: The state user desires.
    :type desired_state: dict
    :param current_state: The state that currently exists.
    :type current_state: dict
    :param ignore: Ignore these keys.
    :type ignore: list

    :return: Different
    :rtype: bool
    """
    return len(get_keys_updated(desired_state, current_state)) > 0
