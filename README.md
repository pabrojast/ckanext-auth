Use CKAN as an auth service in your application.

It adds a new `user_login` action to the CKAN API so that you can call it for authentication of a user from a third party application:

* Method: POST
* Endpoint: `http://ckan:5000/api/3/action/user_login`
* Body: `{"id": <username_or_email>, "password": <password>}`

The `id` field accepts either the username or email address of the user. This leverages CKAN's built-in authentication system that supports both login methods.

## Usage Examples

**Login with username:**
```bash
curl -X POST http://ckan:5000/api/3/action/user_login \
  -H "Content-Type: application/json" \
  -d '{"id": "johndoe", "password": "mypassword"}'
```

**Login with email:**
```bash
curl -X POST http://ckan:5000/api/3/action/user_login \
  -H "Content-Type: application/json" \
  -d '{"id": "john@example.com", "password": "mypassword"}'
```

Example of using it in the NodeJS app:

```javascript
const loginViaCKAN = async function(body) {
   // Call `user_login` action here
   // body can contain either username or email in the 'id' field
   // Example: {"id": "username", "password": "password"}
   // or: {"id": "user@example.com", "password": "password"}
}

app.post("/login", async (req, res) => {
   const loggedUser = await loginViaCKAN(req.body)
   if (loggedUser) {
      // Add logged user to session
      req.session.ckan_user = loggedUser
      res.redirect('/dashboard')
   } else {
      req.flash('error_messages', 'Invalid username/email or password.')
      res.redirect('/login')
   }
})
```

## Requirements

This has been tested on CKAN v2.8.2.

## Installation

To install ckanext-auth:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

2. Install the ckanext-auth Python package into your virtual environment::

     pip install --no-cache-dir -e git+https://github.com/datopian/ckanext-auth.git#egg=ckanext-auth

3. Add ``auth`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

     sudo service apache2 reload

## Debugging

If email login is not working, you can:

1. **Check the logs**: The extension now includes debug logging. Enable debug mode in your CKAN config and check the logs for messages starting with `user_login:`.

2. **Use the debug script**: Run the included debug script to test login:
   ```bash
   python debug_login.py https://your-ckan-site.com user@example.com password
   ```

3. **Verify email in database**: Make sure the user's email is correctly stored in the CKAN database.

4. **Test with username**: Try logging in with the username instead of email to isolate the issue.

## Troubleshooting

**Common issues:**

- **Email not found**: The user's email might not be set in their profile
- **Case sensitivity**: Some CKAN versions are case-sensitive for emails
- **Email validation**: Make sure the email format is correct
- **User status**: Ensure the user account is active
