# -*- coding: utf-8 -*-
"""Not documented yet."""

# Import the "Command Line Interface Creation Kit"
# <https://click.palletsprojects.com>
import click
# For colored output pype includes the colorama library
from colorama import Fore, Style

import pype


# Create a click command https://click.palletsprojects.com/en/7.x/commands/
@click.command(name=pype.fname_to_name(__file__), help=__doc__)
# Add options https://click.palletsprojects.com/en/7.x/options/
@click.option('--option', '-o', default='default', help='An option')
@click.option('--verbose', '-v', is_flag=True, help='A toggle')
def main(option, verbose):
    """Script's main entry point."""
    # Print out something in shiny colors
    pype.print_success('Yay!')
    pype.print_warning('Meh.')
    pype.print_error('Oh no!')

    # Use colorama directly
    print(Fore.RED + '- option:  ' + Style.DIM + Fore.GREEN + option)
    print(Fore.RED + '- verbose: ' + Style.DIM + Fore.GREEN + str(verbose))

    # Use a pype utility
    pype.run_interactive('ls')

    # Your code goes here ...
