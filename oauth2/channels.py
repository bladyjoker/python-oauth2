# HTTP
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
		return HTTPResponse(resp.status, resp.reason, dict(resp.getheaders()), resp.read())
	return HTTPChannel(send)

# Access Token		
import oauth2.messages as messages

class AccessTokenChannel(object):
	def __init__(self, send_impl):
		self.send_impl = send_impl
	def send(self, access_token_grant: messages.AccessTokenGrant) -> messages.AccessToken:
		return self.send_impl(access_token_grant)

def access_token_channel(token_endpoint: str,
		authenticator: HTTPRequestProcessor,
		http_channel: HTTPChannel):
	import urllib.parse
	def send(access_token_grant: messages.AccessTokenGrant):
		grant_entity = 'grant_type={name}&{params}'.format(
					name=access_token_grant.grant_type.name, 
					params=urllib.parse.urlencode(access_token_grant.params.__dict__)
				)
		http_req = HTTPRequest(method='POST',
			uri=token_endpoint,
			headers={'Content-Type': 'application/x-www-form-urlencoded'},
			entity=grant_entity
		)
		authenticated_http_req = authenticator.process(http_req)
		http_resp = http_channel.send(authenticated_http_req)
		if http_resp.status == '200':
			return None
		elif http_resp.status == '400':
			error = urllib.parse.parse_qs(http_resp.read())
			error_fields = ['error', 'error_description', 'error_uri']
			return (
				False, 
				messages.AccessTokenGrantError(**{k:v for k,v in error if k in error_fields}),
				{k:v for k,v in error if k not in error_fields}
				)
	return AccessTokenChannel(send)
