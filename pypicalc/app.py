from __future__ import absolute_import
from __future__ import unicode_literals

from keg import Keg
from flask_mail import Mail

from pypicalc.views import public


class PyPICalc(Keg):
    import_name = 'pypicalc'
    use_blueprints = [public]
    db_enabled = True
    visit_modules = ['.events']
    mail = Mail()
