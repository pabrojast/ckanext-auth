import ckan.logic as logic
import ckan.lib.authenticator as authenticator
from ckan.plugins import toolkit as tk
from ckan.common import _

_check_access = logic.check_access

log = tk.get_logger(__name__)


def user_login(context, data_dict):
    # Adapted from  https://github.com/ckan/ckan/blob/master/ckan/views/user.py#L203-L211
    generic_error_message = {
        u'errors': {
            u'auth': [_(u'Username or password entered was incorrect')]
        },
        u'error_summary': {_(u'auth'): _(u'Incorrect username or password')}
    }

    # Accept either username or email in the incoming identifier
    login_value = (data_dict.get('id') or data_dict.get('login') or u'').strip()
    password_value = data_dict.get('password')

    if not login_value or not password_value:
        return generic_error_message

    # Resolve to username if an email was provided
    model = context['model']
    resolved_username = None
    try:
        if '@' in login_value:
            log.debug('user_login: identifier looks like an email, resolving to username')
            user_from_email = (
                model.Session.query(model.User)
                .filter(model.User.email.ilike(login_value))
                .first()
            )
            if user_from_email:
                resolved_username = user_from_email.name
                log.debug('user_login: resolved email to username=%s', resolved_username)
        else:
            # Might already be a username
            resolved_username = login_value
    except Exception as exc:
        # Do not leak sensitive details; just log for admins
        log.warning('user_login: exception while resolving identifier to username: %r', exc)
        resolved_username = login_value

    identity = {u'login': resolved_username or login_value, u'password': password_value}

    auth = authenticator.UsernamePasswordAuthenticator()
    auth_user_name = auth.authenticate(context, identity)

    if not auth_user_name:
        log.info('user_login: authentication failed for identifier="%s" (resolved_username="%s")', login_value, resolved_username)
        return generic_error_message

    user_obj = model.User.get(auth_user_name)
    if not user_obj:
        return generic_error_message

    return user_obj.as_dict()
