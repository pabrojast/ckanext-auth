import ckan.logic as logic
import ckan.lib.authenticator as authenticator
from ckan.plugins import toolkit as tk
from ckan.common import _
import logging

log = logging.getLogger(__name__)
_check_access = logic.check_access

def _authenticate(context, identity):
    # CKAN >= 2.10 exposes ckan_authenticator/default_authenticate
    if hasattr(authenticator, 'ckan_authenticator'):
        return authenticator.ckan_authenticator(identity)
    if hasattr(authenticator, 'default_authenticate'):
        return authenticator.default_authenticate(identity)
    # CKAN <= 2.9
    if hasattr(authenticator, 'UsernamePasswordAuthenticator'):
        auth = authenticator.UsernamePasswordAuthenticator()
        return auth.authenticate(context, identity)
    log.error('user_login: No compatible authenticator found')
    return None


def user_login(context, data_dict):
    # Adapted from  https://github.com/ckan/ckan/blob/master/ckan/views/user.py#L203-L211
    generic_error_message = {
        u'errors': {
            u'auth': [_(u'Username or password entered was incorrect')]
        },
        u'error_summary': {_(u'auth'): _(u'Incorrect username or password')}
    }
    
    login_id = data_dict.get('id')
    password = data_dict.get('password')
    if login_id and password:
        model = context['model']
        
        log.debug('user_login: Attempting login with id: %s', login_id)
        
        # First, try to find the user by username or email
        user = model.User.by_name(login_id)
        if not user:
            log.debug('user_login: User not found by name, trying by email')
            # Try to find by email
            try:
                user = model.User.by_email2(login_id)
                if user:
                    log.debug('user_login: User found by email2: %s', user.name)
            except AttributeError:
                log.debug('user_login: by_email2 not available, trying by_email')
                # Fallback if by_email2 doesn't exist
                user = model.User.by_email(login_id)
                if user:
                    log.debug('user_login: User found by email: %s', user.name)
        else:
            log.debug('user_login: User found by name: %s', user.name)
        
        if not user:
            log.debug('user_login: User not found by any method')
            return generic_error_message
        
        # Use the username for authentication (email not accepted in older CKAN)
        identity = {
            u'login': user.name,  # Always use the username for authentication
            u'password': password
        }

        log.debug('user_login: Authenticating user: %s', user.name)
        authResult = _authenticate(context, identity)

        if authResult is None:
            log.debug('user_login: Authentication failed for user: %s', user.name)
            return generic_error_message
        else:
            log.debug('user_login: Authentication successful for user: %s', user.name)
            # Return the authenticated user data if available
            if hasattr(authResult, 'as_dict'):
                return authResult.as_dict()
            return user.as_dict()
    return generic_error_message
