from __future__ import absolute_import
from __future__ import unicode_literals

from keg import Keg

from pypicalc.views import public


class BookOrders(Keg):
    import_name = 'pypicalc'
    use_blueprints = [public]
    db_enabled = True
