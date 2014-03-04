import oauth2.http as http
import oauth2.messages as messages

import urllib.parse
import json

# Access Token		
class AccessTokenChannel(object):
	def __init__(self, send_impl):
		self.send_impl = send_impl
	def send(self, access_token_request: messages.AccessTokenRequest) -> messages.AccessToken:
		return self.send_impl(access_token_request)

def access_token_channel(token_endpoint: str,
		client_authenticator: http.HTTPRequestProcessor,
		http_channel: http.HTTPChannel):
	def send(access_token_req: messages.AccessTokenRequest):
		grant_entity = {param.key:param.value for param in access_token_req.params}
		grant_entity['grant_type'] = access_token_req.request_type.name
		http_req = http.HTTPRequest(method='POST',
			uri=token_endpoint,
			headers={'Content-Type': 'application/x-www-form-urlencoded'},
			entity=urllib.parse.urlencode(grant_entity)
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
			
			return (True, messages.AccessToken(**dict(token)), [messages.AccessTokenParam(*p) for p in params])
		elif http_resp.status == '400':
			error,params = partition(
					json.loads(str(http_resp.entity, 'UTF-8')).items(), 
					lambda elem: 
						elem[0] in ['error', 'error_description', 'error_uri']
					)
			return (False, messages.AccessTokenError(**dict(error)), [messages.AccessTokenErrorParam(*p) for p in params])
	return AccessTokenChannel(send)
