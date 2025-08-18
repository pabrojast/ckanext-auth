import ckan.logic as logic
import ckan.lib.authenticator as authenticator
from ckan.plugins import toolkit as tk
from ckan.common import _

_check_access = logic.check_access

def user_login(context, data_dict):
    # Adapted from  https://github.com/ckan/ckan/blob/master/ckan/views/user.py#L203-L211
    # Enhanced to support login with both username and email
    generic_error_message = {
        'errors': {
            'auth': [_('Username/Email or password entered was incorrect')]
        },
        'error_summary': {_('auth'): _('Incorrect username/email or password')}
    }
    model = context['model']
    
    # Try to find user by username first, then by email
    user = model.User.get(data_dict['id'])
    
    # If not found by username, try to find by email
    if not user:
        # Search for user by email
        users = model.Session.query(model.User).filter(
            model.User.email == data_dict['id']
        ).all()
        
        if users:
            # If multiple users have the same email, take the first active one
            for u in users:
                if u.is_active():
                    user = u
                    break
            # If no active user found, take the first one
            if not user:
                user = users[0]
    
    if not user:
        return generic_error_message

    user_dict = user.as_dict()

    if data_dict['password']:
        identity = {
            'login': user_dict['name'],  # Always use username for authentication
            'password': data_dict['password']
        }

        auth = authenticator.UsernamePasswordAuthenticator()
        authUser = auth.authenticate(context, identity)

        if authUser != user_dict['name']:
            return generic_error_message
        else:
            return user_dict
