# -*- coding: utf-8 -*-
"""Register a new plugin."""

import getpass
from os import mkdir
from os.path import dirname, isdir, join
from re import IGNORECASE, sub

import click

from pype.config_handler import PypeConfigHandler
from pype.constants import NOT_DOCUMENTED_YET
from pype.core import load_module
from pype.exceptions import PypeException
from pype.util.cli import fname_to_name, print_error, print_success
from pype.util.iotools import resolve_path


@click.command(name=fname_to_name(__file__), help=__doc__)
@click.option('--name', '-n', help='Plugin name.',
              metavar='NAME', required=True)
@click.option('--path', '-p', help='Host directory.',
              metavar='PATH', required=True)
@click.option('--create', '-c', help='Create on the fly.', is_flag=True)
@click.option('--user-only', '-u', help='Just for current user.', is_flag=True)
def main(name, path, create, user_only):
    """Script's main entry point."""
    if create:
        _create_on_the_fly(name, path)
    # Try to load the module to verify the configuration
    module = None
    try:
        module = load_module(name, path)
    except PypeException:
        print_error(f'Could not find a python module "{name}" at {path}')
        exit(1)
    # Append plugin to global configuration
    config_handler = PypeConfigHandler()
    config_json = config_handler.get_json()
    if any([plugin for plugin in config_json['plugins']
            if plugin['name'] == name]):
        print_error(f'There is already a plugin named "{name}".')
        exit(1)
    path = _replace_parentfolder_if_relative_to_config(
        path, config_handler.get_file_path())
    path = _replace_homefolder_with_tilde(path)
    users = [getpass.getuser()] if user_only else []
    config_json['plugins'].append({
        'name': module.__name__,
        'path': path,
        'users': users
    })
    config_handler.set_json(config_json)

    print_success(f'Plugin "{name}" successfully registered.')


def _replace_homefolder_with_tilde(plugin_path):
    home_folder = resolve_path('~')
    return sub(home_folder, '~', plugin_path, flags=IGNORECASE)


def _replace_parentfolder_if_relative_to_config(plugin_path, config_path):
    plugin_path_abs = resolve_path(plugin_path)
    config_dir_abs = resolve_path(dirname(config_path))
    return sub(sub(r'[/]+$', '', config_dir_abs, flags=IGNORECASE),
               '.', plugin_path_abs, flags=IGNORECASE)


def _create_on_the_fly(name, path):
    abspath = resolve_path(path)
    if not isdir(abspath):
        print_error(f'Path {abspath} does not point to a directoy.')
        exit(1)
    plugin_dir = join(abspath, name)
    if isdir(plugin_dir):
        print_error(f'Path {abspath} already exists.')
        exit(1)
    plugin_init_file = join(plugin_dir, '__init__.py')
    mkdir(plugin_dir)
    with open(plugin_init_file, 'w+') as init:
        init.write('"""' + NOT_DOCUMENTED_YET + '"""\n')
    print_success(f'Plugin "{name}" successfully created at {abspath}')
