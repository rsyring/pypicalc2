from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

import click

from pypicalc.app import PyPICalc


@PyPICalc.command()
def hello():
    click.echo('Hello World')


def cli_entry():
    PyPICalc.cli_run()

if __name__ == '__main__':
    cli_entry()
