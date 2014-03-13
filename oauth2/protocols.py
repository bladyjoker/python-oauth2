import oauth2.messages as messages
import oauth2.actors as actors
from urllib.parse import urlencode, parse_qs
import logging

def code_grant(client: actors.Client, 
		scope: list,
		state: str,
		authorization_endpoint,
		user_authorization_callback,
		access_token_channel):
	
	redirect_uri = user_authorization_callback('{auth_endpoint}?{params}'.format(
			auth_endpoint=authorization_endpoint,
			params=urlencode(
			{
				'client_id': client.identifier,
				'redirect_uri': client.redirect_uris[0],
				'state': state,
				'response_type': str(messages.AUTHCODE_AUTHREQTYPE),
				'scope': ' '.join(scope)
			}))
			)
	auth_params = parse_qs(redirect_uri.split('?')[1])
	if 'error' in auth_params:
		return messages.AuthorizationError(
				auth_params['error'],
				auth_params['error_description'],
				auth_params.get('error_uri', None),
				auth_params['state']	
			)

	token_req = messages.code_tokenreq(auth_params.code, client.redirect_uris[0], client.identifier)
	access_token_response, access_token_response_params = access_token_channel.send(token_req)
	if type(access_token_response) is messages.AccessTokenError:
		logging.getLogger(__name__).warn('Access token failed with {0}'.format(access_token_response.error))
		return access_token_response
	return access_token_response

def resource_owner_grant(access_token_channel, username, password, scope: [str]):
	access_token_response, access_token_response_params = access_token_channel.send(messages.resource_owner_pwd_creds_tokenreq(username, password, scope))
	if type(access_token_response) is messages.AccessTokenError:
		logging.getLogger(__name__).warn('Access token failed with {0}'.format(access_token_response.error))
		return access_token_response
	return access_token_response

def client_creds_grant(access_token_channel, scope: [str]):
	access_token_response, access_token_response_params = access_token_channel.send(messages.client_credentials_tokenreq(scope))
	if type(access_token_response) is messages.AccessTokenError:
		logging.getLogger(__name__).warn('Access token failed with {0}'.format(access_token_response.error))
		return access_token_response
	return access_token_response
