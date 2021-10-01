from . import base
from . import login
from . import metrics
from . import pages
from . import userapi
from .base import *
from .login import *

default_handlers = []
for mod in (base, pages, login, metrics, userapi):
    default_handlers.extend(mod.default_handlers)
