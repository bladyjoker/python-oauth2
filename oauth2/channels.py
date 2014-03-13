import oauth2.http as http
import oauth2.messages as messages

import urllib.parse
from urllib.parse import quote
import json

# Access Token		
class AccessTokenChannel(object):
	def __init__(self, send_impl):
		self.send_impl = send_impl
	def send(self, access_token_request: messages.AccessTokenRequest) -> messages.AccessToken:
		return self.send_impl(access_token_request)

def http_entity_from_tokreq(req: messages.AccessTokenRequest) -> bytes:
	entity = list()
	for key,value in req.params:
		if type(value) is list:
			entity.append('{0}={1}'.format(
					quote(key), 
					quote(' '.join(value))
					)
				)
		else:
			entity.append('{0}={1}'.format(
					quote(key), 
					quote(value)
					)
				)				

	entity.append('grant_type={0}'.format(quote(str(req.request_type))))
	return bytes('&'.join(entity), 'UTF-8')

def access_token_channel(token_endpoint: str,
		client_authenticator: http.HTTPRequestProcessor,
		http_channel: http.HTTPChannel):
	def error_from_dict(error: dict):
		return messages.AccessTokenError(
				error['error'],
				error['error_description'],
				error.get('error_uri', None)
			)

	
	def send(access_token_req: messages.AccessTokenRequest):
		http_req = http.HTTPRequest(method='POST',
			uri=token_endpoint,
			headers={'Content-Type': 'application/x-www-form-urlencoded'},
			entity=http_entity_from_tokreq(access_token_req)
		)

		http_resp = http_channel.send(client_authenticator.process(http_req))
		def partition(iterable, predicate):
			part_yes = list()
			part_no = list()
			for elem in iterable:
				if predicate(elem):
					part_yes.append(elem)
				else:
					part_no.append(elem)
			return (part_yes, part_no)

		if http_resp.status == '200':
			token,params = partition(
					json.loads(str(http_resp.entity, 'UTF-8')).items(), 
					lambda elem: 
						elem[0] in ['access_token','token_type','expires_in']
					)
			
			return (messages.AccessToken(**dict(token)), [messages.AccessTokenParam(*p) for p in params])
		elif http_resp.status == '400':
			error,params = partition(
					json.loads(str(http_resp.entity, 'UTF-8')).items(), 
					lambda elem: 
						elem[0] in ['error', 'error_description', 'error_uri']
					)
			return (error_from_dict(dict(error)), [messages.AccessTokenErrorParam(*p) for p in params])
	return AccessTokenChannel(send)
