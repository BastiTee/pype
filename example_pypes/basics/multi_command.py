# -*- coding: utf-8 -*-
"""A dynamic multi-command creator."""

import json
from os import path
from typing import Any, List

# Import the "Command Line Interface Creation Kit"
# <https://click.palletsprojects.com>
import click

import pype

# Store your dynamic commands along other pype configuration files
commands_registry = path.join(
    pype.Config().get_dir_path(), 'example-multicommands')


def _load_command_registry() -> List:
    """Load the available commands from a json file."""
    try:
        commands = json.load(open(commands_registry, 'r'))
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        commands = []  # Fallback on first initialization
    return commands


def _generate_multi_command() -> List[Any]:
    """Create the subcommand registry."""
    commands = _load_command_registry()
    return [{
        'name': command,
        'help': 'Execute ' + command
    } for command in commands]


def _command_callback(command: str, context: click.Context) -> None:
    """Process the passed subcommand."""
    print('Executing ' + command)
    print('Command context: ' + str(context))


# Create a new click command with dynamic sub commands
@click.group(
    name=pype.fname_to_name(__file__), help=__doc__,
    # Initialize dynamic subcommands using the convenience function
    cls=pype.generate_dynamic_multicommand(
        # Add a function to create multi commands, in this case
        # based on the existing command registry.
        _generate_multi_command(),
        # Provide a callback to receive the command and the
        # click context object.
        _command_callback
    ),
    # This will allow to call the pype without a sub command
    invoke_without_command=True
)
# Add an option to extend the command registry
@click.option('--add', '-a', metavar='COMMAND_NAME',
              help='Add a new subcommand')
# Pass the context to be able to print the help text
@click.pass_context
def main(ctx: click.Context, add: str) -> None:
    """Script's main entry point."""
    # Load the current registry from a local json-file
    command_registry = _load_command_registry()
    # If add option was selected...
    if add:
        if add in command_registry:
            print(add + ' already registered.')
            exit(0)
        click.confirm(
            'Add ' + add + ' to commands?', default=False, abort=True)
        # Register and save the new command
        command_registry.append(add)
        json.dump(command_registry, open(commands_registry, 'w+'))
    # ... else just print the help text.
    elif ctx.invoked_subcommand is None:
        print(ctx.get_help())
