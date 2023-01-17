# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4 -*-
#
# Copyright 2023 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""JujuSpell juju add user command."""
import argparse
import os
import textwrap
from getpass import getpass
from typing import Any

import craft_cli
import yaml
from craft_cli import emit
from craft_cli.dispatcher import _CustomArgumentParser

from juju_spell.cli.base import BaseJujuCMD
from juju_spell.commands.add_user import AddUserCommand
from juju_spell.settings import PERSONAL_CONFIG_PATH


class AddUserCMD(BaseJujuCMD):
    """JujuSpell add user command."""

    name = "add-user"
    help_msg = "add juju user to remote controller"
    overview = textwrap.dedent(
        """
        The command will create user on controller with random_password or gived
        password and print the yaml config to stdout.

        Example:
        $ juju_spell add-user --username newuser

        controllers:
            - uuid: 74ef132a-6c96-48db-808c-76e8396f4feb
              username: newuser
              password: "{random_password}"
        """
    )

    command = AddUserCommand

    def fill_parser(self, parser: _CustomArgumentParser) -> None:
        super().fill_parser(parser=parser)
        parser.add_argument(
            "--username",
            type=str,
            help="username to create",
            required=True,
        )
        parser.add_argument(
            "--display_name",
            type=str,
            help=(
                "display_name to create. If display_name is None then it will be set as"
                " username"
            ),
            required=False,
        )
        parser.add_argument(
            "-p",
            dest="passowrd",
            nargs="?",
            required=False,
            help=craft_cli.HIDDEN,
        )

    def before(self, parsed_args: argparse.Namespace) -> None:
        """Run before execution."""
        super().before(parsed_args=parsed_args)
        parsed_args.password = getpass("Password(If empty will use random password): ")
        if not parsed_args.display_name:
            parsed_args.display_name = parsed_args.username

    @staticmethod
    def format_output(retval: Any) -> str:
        """Pretty formatter for output.

        Notes:
            - The first element of retval, which is a list, is a list of controllers'
            output. The example:

            retval = [
                [
                    {
                        "output": output
                        "context": {
                            "name": controller_config.name,
                            "customer": controller_config.customer,
                        },
                    },
                    {
                        "output": output
                        "context": {
                            "name": controller_config.name,
                            "customer": controller_config.customer,
                        },
                    },
                ]
            ]
        """
        emit.debug(f"formatting `{retval}`")

        output = {"controllers": []}
        for controller_output in retval[0]:
            output["controllers"].append(controller_output["output"])

        yaml_str = yaml.dump(
            output, default_flow_style=False, allow_unicode=True, encoding=None
        )
        return (
            f"Please put user information to personal config({PERSONAL_CONFIG_PATH}):"
            f"{os.linesep}{os.linesep}{yaml_str}{os.linesep}"
        )
