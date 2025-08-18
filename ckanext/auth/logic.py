import ckan.logic as logic
import ckan.lib.authenticator as authenticator
from ckan.plugins import toolkit as tk
from ckan.common import _
import logging

log = logging.getLogger(__name__)
_check_access = logic.check_access

def user_login(context, data_dict):
    # Adapted from  https://github.com/ckan/ckan/blob/master/ckan/views/user.py#L203-L211
    generic_error_message = {
        u'errors': {
            u'auth': [_(u'Username or password entered was incorrect')]
        },
        u'error_summary': {_(u'auth'): _(u'Incorrect username or password')}
    }
    
    if data_dict[u'password']:
        model = context['model']
        login_id = data_dict['id']
        
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
        
        # Use the username for authentication
        identity = {
            u'login': user.name,  # Always use the username for authentication
            u'password': data_dict[u'password']
        }

        log.debug('user_login: Authenticating user: %s', user.name)
        auth = authenticator.UsernamePasswordAuthenticator()
        authResult = auth.authenticate(context, identity)

        if authResult is None:
            log.debug('user_login: Authentication failed for user: %s', user.name)
            return generic_error_message
        else:
            log.debug('user_login: Authentication successful for user: %s', user.name)
            # Return the user data
            return user.as_dict()
