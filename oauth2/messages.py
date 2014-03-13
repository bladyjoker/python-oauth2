## Authorization

AuthorizationRequestParam = tuple

AuthorizationRequestType = str
AUTHCODE_AUTHREQTYPE = AuthorizationRequestType('code')
IMPLICIT_AUTHREQTYPE = AuthorizationRequestType('token')

class AuthorizationRequest(object):
	def __init__(self, request_type: AuthorizationRequestType, params: [AuthorizationRequestParam]):
		self.request_type = request_type
		self.params = params

def code_auth_request(client_id, redirect_uri, scope, state):
	return AuthorizationRequest(
			AUTHCODE_AUTHREQTYPE, 
			[
				AuthorizationRequestParam(('client_id', client_id)),
				AuthorizationRequestParam(('redirect_uri', redirect_uri)),
				AuthorizationRequestParam(('scope', scope)),
				AuthorizationRequestParam(('state', state))
			]
		)

def implicit_auth_request(client_id, redirect_uri, scope, state):
	return AuthorizationRequest(
		IMPLICIT_AUTHREQTYPE, 
		[
			AuthorizationRequestParam(('client_id', client_id)),
			AuthorizationRequestParam(('redirect_uri', redirect_uri)),
			AuthorizationRequestParam(('scope', scope)),
			AuthorizationRequestParam(('state', state))
		]
	) 

class CodeAuthorization(object):
	def __init__(self, code, state):
		self.code = code
		self.state = state

class AuthorizationError(object):
	def __init__(self, error, error_description, error_uri, state):
		self.error = error
		self.error_description = error_description
		self.error_uri = error_uri
		self.state = state

# Access token
AccessTokenRequestParam = tuple

AccessTokenRequestType = str
AUTHCODE_TKNREQTYPE = AccessTokenRequestType('authorization_code')
ROCREDS_TKNREQTYPE = AccessTokenRequestType('password')
CLICREDS_TKNREQTYPE = AccessTokenRequestType('client_credentials')
REFRESH_TKNREQTYPE = AccessTokenRequestType('refresh_token')

class AccessTokenRequest(object):
	def __init__(self, request_type: AccessTokenRequestType, params: [AccessTokenRequestParam]):
		self.request_type = request_type
		self.params = params

def code_tokenreq(code, redirect_uri, client_id):
	return AccessTokenRequest(
		AUTHCODE_TKNREQTYPE,
		[
			AccessTokenRequestParam(('code', code)),
			AccessTokenRequestParam(('redirect_uri', redirect_uri)),
			AccessTokenRequestParam(('client_id', client_id))
		])

def resource_owner_pwd_creds_tokenreq(username, password, scope):
	return AccessTokenRequest(
		ROCREDS_TKNREQTYPE,
		[
			AccessTokenRequestParam(('username', username)),
			AccessTokenRequestParam(('password', password)),
			AccessTokenRequestParam(('scope', scope))
		])

def client_credentials_tokenreq(scope):
	return AccessTokenRequest(
		CLICREDS_TKNREQTYPE,
		[AccessTokenRequestParam(('scope', scope))])

def refresh_tokenreq(refresh_token, scope):
	return AccessTokenRequest(
		REFRESH_TKNREQTYPE,
		[
			AccessTokenRequestParam(('refresh_token', refresh_token)),
			AccessTokenRequestParam(('scope', scope))
		])

class AccessToken(object):
	def __init__(self, access_token: str, token_type: str, expires_in: int):
		self.access_token = access_token
		self.token_type = token_type
		self.expires_in = expires_in
		self.expires_on = 1#time!!!

AccessTokenParam = tuple

def refresh_tokenparams(refresh_token):
	return [AccessTokenParam(('refresh_token', refresh_token))]

def state_tokenparams(state, scope):
	return [AccessTokenParam(('state', state)), AccessTokenParam(('scope', scope))]


class AccessTokenError(object):
	def __init__(self, error: str, error_description: str, error_uri: str):
		self.error = error
		self.error_description = error_description
		self.error_uri = error_uri

AccessTokenErrorParam = tuple

def state_errorparams(state):
	return [AccessTokenErrorParam(('state', state))]

