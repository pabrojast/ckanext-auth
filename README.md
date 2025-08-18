Use CKAN as an auth service in your application.

It adds a new `user_login` action to the CKAN API so that you can call it for authentication of a user from a third party application:

* Method: POST
* Endpoint: `http://ckan:5000/api/3/action/user_login`
* Body: `{"id": <username_or_email>, "password": <password>}`

## Features

- ✅ **Login with Username**: Traditional authentication using CKAN username
- ✅ **Login with Email**: New functionality to authenticate using email address
- ✅ **Flexible Authentication**: Automatically detects whether the provided `id` is a username or email
- ✅ **Active User Priority**: When multiple users share the same email, prioritizes active users
- ✅ **Error Handling**: Clear error messages for invalid credentials or non-existent users

## Authentication Flow

1. The system first attempts to find a user by the provided `id` as a username
2. If no user is found by username, it searches for users by email address
3. If multiple users have the same email, it prioritizes active users
4. Authentication is performed using the found user's username
5. Returns user data on success or error message on failure

Example of using it in the NodeJS app:

```javascript
const loginViaCKAN = async function(body) {
   // Call `user_login` action here
   // body.id can now be either username or email
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

## API Examples

### Login with Username
```json
{
  "id": "my_username",
  "password": "my_password"
}
```

### Login with Email
```json
{
  "id": "user@example.com", 
  "password": "my_password"
}
```

### Success Response
```json
{
  "success": true,
  "result": {
    "id": "user-uuid",
    "name": "my_username",
    "email": "user@example.com",
    "fullname": "User Full Name",
    "created": "2023-01-01T00:00:00.000000",
    "is_active": true,
    // ... other user fields
  }
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "errors": {
      "auth": ["Username/Email or password entered was incorrect"]
    },
    "error_summary": {
      "auth": "Incorrect username/email or password"
    }
  }
}
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
