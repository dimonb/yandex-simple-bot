
import logging
root = logging.getLogger()
root.setLevel(logging.DEBUG)

import gettext
el = gettext.translation('base', localedir='locales', languages=['ru'])
el.install()
