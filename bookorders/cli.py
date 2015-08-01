from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

import click

from bookorders.app import BookOrders


@BookOrders.command()
def hello():
    click.echo('Hello World')


def cli_entry():
    BookOrders.cli_run()

if __name__ == '__main__':
    cli_entry()
