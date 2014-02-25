class Client(object):
	def __init__(self, identifier, client_type, redirect_uris):
		self.identifier = identifier
		self.client_type = client_type
		self.redirect_uris = redirect_uris

class ResourceOwner(object):
	def __init__(self):
		pass
class AuthorizationEndpoint(object):
	def __init__(self, uri):
		self.uri = uri

class TokenEndpoint(object):
	def __init__(self, uri):
		self.uri = uri
