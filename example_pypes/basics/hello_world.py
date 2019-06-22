# -*- coding: utf-8 -*-
"""A classic hello world console feedback."""

import click


@click.command('hello_world', help=__doc__)
def main():
    """Script's main entry point."""
    print('Hello World!')
