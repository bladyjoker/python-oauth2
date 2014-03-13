class HTTPRequest(object):
	def __init__(self, method: str, uri: str, entity: bytes, headers: dict = {}):
		self.method = method
		self.uri = uri
		self.headers = headers
		self.entity = entity

class HTTPResponse(object):
	def __init__(self, status: str, reason: str, headers: dict, entity: bytes, protocol: str = 'HTTP/1.1'):
		self.status = status
		self.reason = reason
		self.entity = entity
		self.protocol = protocol

class HTTPRequestProcessor(object):
	def __init__(self, process_impl):
		self.process_impl = process_impl
	def process(self, req: HTTPRequest) -> HTTPRequest: # mutates and returns the same HTTPRequest object
		return self.process_impl(req)

class HTTPChannel(object):
	def __init__(self, send_impl):
		self.send_impl = send_impl
	def send(self, http_request: HTTPRequest):
		return self.send_impl(http_request)

def http_req_proc(req_processors: list):
	def process(req: HTTPRequest):
		for proc in req_processors:
			proc.process(req)
		return req
	return HTTPRequestProcessor(process)

def http_basic_authenticator(client_identifier: str, client_password: str):
	import base64
	import urllib.parse
	def process(req: HTTPRequest) -> HTTPRequest:
		authorization_string = str(base64.b64encode(bytes('{id}:{pwd}'.format(id=client_identifier, pwd=client_password), 'UTF-8')), 'UTF-8')
		req.headers['Authorization'] = 'Basic {auth}'.format(auth=authorization_string)
		return req
	return HTTPRequestProcessor(process)

def pyhttpcli_channel(host: str, port:int):
	import http.client
	def send(http_request: HTTPRequest):
		http_conn = http.client.HTTPConnection(host, port)
		http_conn.request(
			http_request.method, 
			http_request.uri,
			body=http_request.entity, 
			headers=http_request.headers
		)
		resp=http_conn.getresponse()
		return HTTPResponse(str(resp.status), resp.reason, dict(resp.getheaders()), resp.read())
	return HTTPChannel(send)
