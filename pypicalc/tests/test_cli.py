from __future__ import absolute_import
from __future__ import unicode_literals

from keg.testing import CLIBase

from pypicalc.app import PyPICalc


class TestCLI(CLIBase):
    app_cls = PyPICalc

    def test_hello(self):
        result = self.invoke(cmd_name='hello')
        assert 'Hello World\n' == result.output
