import ckan.logic as logic
import ckan.lib.authenticator as authenticator
from ckan.plugins import toolkit as tk
from ckan.common import _
import logging

log = logging.getLogger(__name__)
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
    
    login_id = data_dict.get('id', '').strip()
    password = data_dict.get('password', '')
    
    log.info("Login attempt with id: %s", login_id)
    
    # Input validation
    if not login_id or not password:
        log.info("Missing login_id or password")
        return generic_error_message
    
    # Try to find user by username first, then by email
    user = model.User.get(login_id)
    log.info("User found by username: %s", user is not None)
    
    # If not found by username, try to find by email
    if not user:
        log.info("Searching for user by email: %s", login_id)
        try:
            users = model.Session.query(model.User).filter(
                model.User.email == login_id
            ).all()
            
            log.info("Users found by email: %s", len(users) if users else 0)
            
            if users:
                # If multiple users have the same email, take the first active one
                for u in users:
                    if u.is_active():
                        user = u
                        log.info("Selected active user: %s", u.name)
                        break
                # If no active user found, take the first one
                if not user:
                    user = users[0]
                    log.info("Selected first user: %s", user.name)
        except Exception as e:
            log.error("Error searching user by email: %s", str(e))
    
    if not user:
        log.info("No user found")
        return generic_error_message

    # Check if user is active
    if not user.is_active():
        log.info("User %s is not active", user.name)
        return generic_error_message

    log.info("Attempting authentication for user: %s", user.name)
    
    user_dict = user.as_dict()

    if password:
        identity = {
            'login': user_dict['name'],  # Always use username for authentication
            'password': password
        }

        auth = authenticator.UsernamePasswordAuthenticator()
        authUser = auth.authenticate(context, identity)
        
        log.info("Authentication result: %s, expected: %s", authUser, user_dict['name'])

        if authUser != user_dict['name']:
            log.info("Authentication failed - password mismatch")
            return generic_error_message
        else:
            log.info("Login successful for user: %s", user_dict['name'])
            return user_dict
    
    return generic_error_message
