from __future__ import absolute_import
from __future__ import unicode_literals

# important to import from .cli so that the commands get attached
from pypicalc.cli import BookOrders


def pytest_configure(config):
    BookOrders.testing_prep()
