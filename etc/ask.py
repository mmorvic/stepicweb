import multiprocessing


def number_of_workers():
  return (multiprocessing.cpu_count() * 2) + 1

mode = 'wsgi'
bind = '%s:%s' % ('0.0.0.0', '8000')
working_dir = '~/box/web/ask'
workers = number_of_workers()
loglevel = "debug"
application = 'ask.wsgi:application'

# CONFIG = {
#   'mode': 'wsgi',
#   'python': '/usr/bin/python3',
#   'working_dir': '/home/box/web/ask',
#   'args': (
#     '--bind=0.0.0.0:8000',
#     '--workers=2',
#     '--timeout=15',
#     '--log-level=debug',
#     'ask.wsgi:application',
#   ),
# }