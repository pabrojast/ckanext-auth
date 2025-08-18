import ckan.logic as logic
import ckan.lib.authenticator as authenticator
from ckan.plugins import toolkit as tk
from ckan.common import _

_check_access = logic.check_access

def user_login(context, data_dict):
    # Adapted from  https://github.com/ckan/ckan/blob/master/ckan/views/user.py#L203-L211
    generic_error_message = {
        u'errors': {
            u'auth': [_(u'Username or password entered was incorrect')]
        },
        u'error_summary': {_(u'auth'): _(u'Incorrect username or password')}
    }

    # Accept either username or email in the incoming identifier
    login_value = data_dict.get('id') or data_dict.get('login')
    password_value = data_dict.get('password')

    if not login_value or not password_value:
        return generic_error_message

    identity = {
        u'login': login_value,
        u'password': password_value
    }

    auth = authenticator.UsernamePasswordAuthenticator()
    auth_user_name = auth.authenticate(context, identity)

    if not auth_user_name:
        return generic_error_message

    model = context['model']
    user_obj = model.User.get(auth_user_name)
    if not user_obj:
        return generic_error_message

    return user_obj.as_dict()
