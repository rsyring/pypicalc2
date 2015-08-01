from __future__ import absolute_import
from __future__ import unicode_literals

import warnings

warnings.filterwarnings('ignore', r".*unclosed file", module='click', category=ResourceWarning)
warnings.filterwarnings('ignore', r".*unclosed file", module='sys', category=ResourceWarning)
