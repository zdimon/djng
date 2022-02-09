TRANS_MAP = {}

# /dashboard/index PAGE
from .parts.admin import MAP
TRANS_MAP.update(MAP)

# Main login-form
from .parts.loginform import MAP
TRANS_MAP.update(MAP)

# Registration-form
from .parts.regform import MAP
TRANS_MAP.update(MAP)

# Chat room
from .parts.chat import MAP
TRANS_MAP.update(MAP)

from .parts.photo import MAP
TRANS_MAP.update(MAP)

from .parts.nav import MAP
TRANS_MAP.update(MAP)

from .parts.autotrans import MAP
TRANS_MAP.update(MAP)