# -*- coding: utf-8 -*-
"""Print system information useful for bug reports or other inspections."""

import platform
from os import environ

import click

from pype.pype_constants import ENV_CONFIG_FILE

from tabulate import tabulate


@click.command(help=__doc__)
def main():
    """Script's main entry point."""
    UNSET = 'Not set'
    print('PYPE SYSTEM ENVIRONMENT')
    infos = []
    infos.append(['MACHINE', platform.machine()])
    infos.append(['PROCESSOR', platform.processor()])
    infos.append(['PLATFORM', platform.platform()])
    infos.append(['VERSION', platform.version()])
    infos.append(['RELEASE', platform.release()])
    infos.append(['SYSTEM', platform.system()])
    infos.append(['SHELL', environ.get('SHELL', UNSET)])
    infos.append(['CONFIG FILE', environ.get(
        ENV_CONFIG_FILE, UNSET)])
    print(tabulate(infos))


if __name__ == '__main__':
    main()
