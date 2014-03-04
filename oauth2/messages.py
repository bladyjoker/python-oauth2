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
class AccessTokenRequestType(object):
	def __init__(self, name: str):
		self.name = name

AUTHCODE_REQTYPE = AccessTokenRequestType('authorization_code')
ROCREDS_REQTYPE = AccessTokenRequestType('password')
CLICREDS_REQTYPE = AccessTokenRequestType('client_credentials')
REFRESH_REQTYPE = AccessTokenRequestType('refresh_token')

class AccessTokenRequestParam(object):
	def __init__(self, key, value):
		self.key = key
		self.value = value

def code_reqparams(code, redirect_uri, client_id):
	return [
		AccessTokenRequestParam('code', code),
		AccessTokenRequestParam('redirect_uri', redirect_uri),
		AccessTokenRequestParam('client_id', client_id)
		]

def resource_owner_pwd_creds_reqparams(username, password, scope):
	return [
		AccessTokenRequestParam('username', username),
		AccessTokenRequestParam('password', password),
		AccessTokenRequestParam('scope', scope)
		]

def client_credentials_reqparams(scope):
	return [AccessTokenRequestParam('scope', scope)]

def refresh_reqparams(refresh_token, scope):
	return [
		AccessTokenRequestParam('refresh_token', refresh_token),
		AccessTokenRequestParam('scope', scope)
		]

class AccessTokenRequest(object):
	def __init__(self, request_type: AccessTokenRequestType, params: [AccessTokenRequestParam]):
		self.request_type = request_type
		self.params = params

class AccessToken(object):
	def __init__(self, access_token: str, token_type: str, expires_in: int):
		self.access_token = access_token
		self.token_type = token_type
		self.expires_in = expires_in
		self.expires_on = 1#time!!!

class AccessTokenParam(object):
	def __init__(self, key, value):
		self.key = key
		self.value = value

def refresh_tokenparams(refresh_token):
	return [AccessTokenParam('refresh_token', refresh_token)]

def state_tokenparams(state, scope):
	return [AccessTokenParam('state', state), AccessTokenParam('scope', scope)]


class AccessTokenError(object):
	def __init__(self, code: str, description: str, uri: str):
		self.code = code
		self.description = description
		self.uri = uri

class AccessTokenErrorParam(object):
	def __init__(self, key, value):
		self.key = key
		self.value = value

def state_errorparams(state):
	return [AccessTokenErrorParam('state', state)]

class AcccessTokenResponse(object):
	def __init__(self, success: bool, error: AccessTokenError, access_token: AccessToken):
		self.success = success
		self.error = error
		self.access_token = access_token

