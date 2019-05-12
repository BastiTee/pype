#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Pype

:copyright: (c) 2019 by Basti Tee.
:license: Apache 2.0, see LICENSE for more details.
"""

import logging
import os
from re import sub
from argparse import ArgumentParser
from json import load
from pype.util.misc import get_or_default
import importlib
import inspect
from pype.util.iotools import get_immediate_subfiles


class PypeException(Exception):
    pass


class PypeConfigurationException(PypeException):
    pass


class Pype():

    DEFAULT_LOG_LEVEL = 'INFO'
    DEFAULT_LOG_FORMAT = (
        '%(asctime)-15s %(levelname)s %(message)s [%(name)s.%(funcName)s]'
    )
    DEFAULT_CONFIG_FILE = 'config.json'

    def __init__(self, args):
        cfg = self.load_configuration(args.c)
        default_loglevel = (
            'DEBUG' if args.v
            else get_or_default(cfg, 'core.loglevel', self.DEFAULT_LOG_LEVEL))
        logging.basicConfig(
            level=default_loglevel,
            format=get_or_default(cfg,
                                  'core.logformat', self.DEFAULT_LOG_FORMAT)
        )
        self.log = logging.getLogger(__name__)
        self.log.debug('Initializing pype...')
        self.plugin_registry = {}
        for plugin in get_or_default(cfg, 'pypes', []):
            self.init_plugin(plugin)
        self.log.debug('Loaded plugins:\n{}'.format(
            self.prettify_plugin_registry()))
        self.invoke_matching_pype(self.plugin_registry, args.pype_command)

    def init_plugin(self, plugin):
        # Load remote module via importlib
        try:
            plugin_mod = importlib.import_module(plugin)
        except ModuleNotFoundError as e:
            raise PypeConfigurationException(e)
        # Setup plugin registry
        reg = {'name': plugin, 'module': plugin_mod}
        reg['abspath'] = os.path.dirname(inspect.getabsfile(plugin_mod))
        reg['cmds'] = self.resolve_pypes(reg['abspath'])
        # Register
        self.plugin_registry[plugin] = reg

    def resolve_pypes(self, abspath):
        cmds = get_immediate_subfiles(abspath, r'^(?!__).*(?!__)\.py$')
        return [sub(r'\.py$', '', cmd) for cmd in cmds]

    def invoke_matching_pype(self, reg, pype):
        if not pype:
            print('No pype selected.')
            exit(0)
        root_cmd = pype[0]
        for key in reg.keys():
            mod = reg[key]
            for cmd in mod['cmds']:
                if not cmd == root_cmd:
                    continue
                importlib.import_module(mod['name'] + '.' + cmd)

    def load_configuration(self, cfg_path):
        cfg_path = cfg_path if cfg_path else self.DEFAULT_CONFIG_FILE
        return load(open(cfg_path, 'r'))

    def prettify_plugin_registry(self):
        plugin_docu = []
        for plugin in self.plugin_registry:
            pg = self.plugin_registry.get(plugin)
            plugin_docu.append(plugin.upper())
            for key in pg.keys():
                plugin_docu.append(' - {} = {}'.format(key, pg[key]))
        return '\n'.join(plugin_docu)


if __name__ == "__main__":
    parser = ArgumentParser(description="pype")
    parser.add_argument(
        '-c',
        metavar="CONFIG_JSON",
        type=str,
        help='Pype configuration file (defaults to config.json)')
    parser.add_argument(
        '-v',
        action='store_true',
        help='Set logging to DEBUG')
    parser.add_argument('pype_command', nargs='*')
    pype = Pype(parser.parse_args())