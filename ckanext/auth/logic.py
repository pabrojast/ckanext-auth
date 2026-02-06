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
    if not login_id or not password:
        return generic_error_message

    model = context['model']

    log.debug('user_login: Attempting login with id: %s', login_id)

    # First, try to find the user by username
    user = model.User.by_name(login_id)
    if not user:
        log.debug('user_login: User not found by name, trying by email')
        # Try to find by email
        try:
            user = model.User.by_email2(login_id)
        except AttributeError:
            user = model.User.by_email(login_id)
            # CKAN <= 2.8 may return a list
            if isinstance(user, list):
                user = user[0] if user else None

    if not user:
        log.debug('user_login: User not found by any method')
        return generic_error_message

    # Use the username for authentication (email not accepted in older CKAN)
    identity = {
        u'login': user.name,
        u'password': password
    }

    log.debug('user_login: Authenticating user: %s', user.name)
    auth_result = _authenticate(context, identity)

    if auth_result is None:
        log.debug('user_login: Authentication failed for user: %s', user.name)
        return generic_error_message

    log.debug('user_login: Authentication successful for user: %s', user.name)
    if hasattr(auth_result, 'as_dict'):
        return auth_result.as_dict()
    return user.as_dict()
