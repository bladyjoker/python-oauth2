## Authorization
class AuthorizationRequest(object):
	def __init__(self, response_type, client_id, redirect_uri, scope, state):
		self.response_type = response_type
		self.client_id = client_id
		self.redirect_uri = redirect_uri
		self.scope = scope
		self.state = state

### Code Grant
class CodeAuthorizationRequest(AuthorizationRequest):
	def __init__(self, client_id, redirect_uri, scope, state):
		AuthorizationRequest.__init__(self, 'code', client_id, redirect_uri, scope, state)

class CodeAuthorizationSuccessResponse(object):
	def __init__(self, code, state):
		self.code = code
		self.state = state
### Implicit grant
class ImplicitAuthorizationRequest(AuthorizationRequest):
	def __init__(self, client_id, redirect_uri, scope, state):
		AuthorizationRequest.__init__(self, 'token', client_id, redirect_uri, scope, state)

### Erroneous
class AuthorizationErrorResponse(object):
	def __init__(self, error, error_description, error_uri, state):
		self.error = error
		self.error_description = error_description
		self.error_uri = error_uri
		self.state = state

# Access token model
class AccessTokenGrantType(object):
	def __init__(self, name: str):
		self.name = name

AUTHCODE_GRANT = AccessTokenGrantType('authorization_code')
ROCREDS_GRANT = AccessTokenGrantType('password')
CLICREDS_GRANT = AccessTokenGrantType('client_credentials')
REFRESH_GRANT = AccessTokenGrantType('refresh_token')

class AccessTokenGrantParams(object):
	pass

class Code(AccessTokenGrantParams):
	def __init__(self, code, redirect_uri, client_id):
		self.code = code
		self.redirect_uri = redirect_uri
		self.client_id = client_id

class ResourceOwnerPasswordCredential(AccessTokenGrantParams):
	def __init__(self, username, password, scope):
		self.username = username
		self.password = password
		self.scope = scope

class ClientCredentials(AccessTokenGrantParams):
	def __init__(self, scope):
		self.scope = scope

class Refresh(AccessTokenGrantParams):
	def __init__(self, refresh_token, scope):
		self.refresh_token = refresh_token
		self.scope = scope

class AccessTokenGrant(object):
	def __init__(self, grant_type: AccessTokenGrantType, params: AccessTokenGrantParams):
		self.grant_type = grant_type
		self.params = params

class AccessToken(object):
	def __init__(self, access_token: str, token_type: str, expires_in: int):
		self.access_token = access_token
		self.token_type = token_type
		self.expires_in = expires_in
		self.expires_on = 1#time!!!

class AccessTokenRefresh(object):
	def __init__(refresh_token: str, access_token: AccessToken):
		self.refresh_token = refresh_token
		self.access_token = access_token

class AccessTokenState(object):
	def __init__(state: str, scope: list, access_token: AccessToken):
		self.state = state
		self.scope = scope
		self.access_token = access_token

class AccessTokenGrantError(object):
	def __init__(self, code: str, description: str, uri: str):
		self.code = code
		self.description = description
		self.uri = uri

class AccessTokenGrantErrorState(object):
	def __init__(self, state, error: AccessTokenGrantError):
		self.state = state
		self.error = error

