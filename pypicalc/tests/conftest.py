from __future__ import absolute_import
from __future__ import unicode_literals

# important to import from .cli so that the commands get attached
from pypicalc.cli import PyPICalc


def pytest_configure(config):
    PyPICalc.testing_prep()
