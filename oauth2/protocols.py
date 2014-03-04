import oauth2.messages as messages
import oauth2.actors as actors
import logging

	
def code_grant(client: actors.Client, 
		scope: list,
		state: str,
		user_authorization_callback,
		access_token_channel):
	
	car = messages.CodeAuthorizationRequest(client.identifier, client.redirect_uris[0], scope, state)
	logging.getLogger(__name__).info('Requesting authorization for client with id {0} and scope {1} with redirection uri {2}'.format(client.identifier, ' '.join(scope), client.redirect_uris[0]))
	is_success, auth_response = user_authorization_callback(car)
	if is_success == False:
		logging.getLogger(__name__).warn('Authorization request failed with {0}'.format(auth_response.error))
		return auth_response
	if car.state != auth_response.state:
		logging.getLogger(__name__).warn('Invalid authorization response state')
		return auth_response
	code_params = messages.code_reqparams(auth_response.code, client.redirect_uris[0], client.identifier)
	grant = messages.AccessTokenRequest(messages.AUTHCODE_REQTYPE, code_params)
	is_success, access_token, access_token_params = access_token_channel.send(grant)
	if is_success == False:
		logging.getLogger(__name__).warn('Access token failed with {0}'.format(access_token_response.error))
		return access_token_response
	return access_token
