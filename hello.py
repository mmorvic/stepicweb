import urlparse


def app(environ, start_response):
    status = '200 OK'
    response_headers = [
        ('Content-type','text/plain')
    ]
    start_response(status, response_headers)
    data = []
    qs = urlparse.parse_qs(environ['QUERY_STRING'])
    for k in qs:
	    for i in qs[k]:
	        data.append("%s=%s\n" % (k, i))

    return iter(data)