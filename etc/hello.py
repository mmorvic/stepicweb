import multiprocessing


# mode = 'wsgi'
# working_dir = '/home/victor/box/web/hello.py'
# bind = '0.0.0.0:8080'
# workers = multiprocessing.cpu_count() * 2 + 1
# application = 'hello:app'
# loglevel = 'error'
def number_of_workers():
	# print 'is working'
	return (multiprocessing.cpu_count() * 2) + 1

# options = {
#     'bind': '%s:%s' % ('0.0.0.0', '8080'),
#     'workers': number_of_workers(),
# }
bind = '%s:%s' % ('0.0.0.0', '8080')
workers = number_of_workers()
# print bind
loglevel = "debug"