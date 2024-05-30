# -*- coding: utf-8 -*-

# Copyright: Josh Williams <jdubz@dubzland.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ._vault_common import VaultAuthMethod, VaultAuthenticationError


class VaultAuthMethodAwsIam(VaultAuthMethod):
    NAME = "aws_iam"
    AUTH_FIELDS = [
        "aws_profile",
        "aws_access_key",
        "aws_secret_key",
        "aws_security_token",
        "region",
        "aws_iam_server_id",
        "role_id",
    ]

    def validate(self):
        params = {
            "access_key": self._options.get("aws_access_key"),
            "secret_key": self._options.get("aws_secret_key"),
        }

        session_token = self._options.get("aws_security_token")
        if session_token:
            params["session_token"] = session_token

        mount_point = self._options.get("mount_point")
        if mount_point:
            params["mount_point"] = mount_point

        role = self._options.get("role_id")
        if role:
            params["role"] = role

        region = self._options.get("region")
        if region:
            params["region"] = region

        header_value = self._options.get("aws_iam_server_id")
        if header_value:
            params["header_value"] = header_value

        if not (params["access_key"] and params["secret_key"]):
            try:
                import boto3
                import botocore
            except ImportError:
                raise VaultAuthenticationError(
                    "boto3 is required for loading a profile or IAM role credentials."
                )

            profile = self._options.get("aws_profile")
            try:
                session_credentials = boto3.session.Session(
                    profile_name=profile
                ).get_credentials()
            except botocore.exceptions.ProfileNotFound:
                raise VaultAuthenticationError(
                    "The AWS profile '%s' was not found." % profile
                )

            if not session_credentials:
                raise VaultAuthenticationError(
                    "No AWS credentials supplied or available."
                )

            params["access_key"] = session_credentials.access_key
            params["secret_key"] = session_credentials.secret_key
            if session_credentials.token:
                params["session_token"] = session_credentials.token

        self._auth_aws_iam_login_params = params

    def authenticate(self, client, use_token=True):
        params = self._auth_aws_iam_login_params
        client.auth.aws.iam_login(use_token=use_token, **params)
