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
    
    if data_dict[u'password']:
        identity = {
            u'login': data_dict['id'],  # Pass the original id (username or email)
            u'password': data_dict[u'password']
        }

        auth = authenticator.UsernamePasswordAuthenticator()
        authResult = auth.authenticate(context, identity)

        if authResult is None:
            return generic_error_message
        else:
            # Extract user ID from auth result (format: "user_id,1")
            user_id = authResult.split(',')[0]
            model = context['model']
            user = model.User.get(user_id)
            if user:
                return user.as_dict()
            else:
                return generic_error_message
