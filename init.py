this_file = 'req/bin/activate_this.py'
exec(open(this_file).read(), {'__file__': this_file})

import logging
root = logging.getLogger()
root.setLevel(logging.DEBUG)

import gettext
el = gettext.translation('base', localedir='locales', languages=['ru'])
el.install()
