"""Tests for plugin.py."""
import pytest
import ckan.tests.factories as factories
import ckan.model as model
from ckan.tests import helpers

import ckanext.auth.plugin as plugin
from ckanext.auth.logic import user_login


class TestAuthPlugin:
    """Test class for AuthPlugin functionality."""

    def test_plugin(self):
        """Basic plugin test."""
        pass

    @pytest.mark.usefixtures("clean_db", "with_plugins")
    def test_user_login_with_username(self):
        """Test login with username."""
        # Create a test user
        user = factories.User(
            name='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        context = {'model': model}
        data_dict = {
            'id': 'testuser',
            'password': 'testpass123'
        }
        
        result = user_login(context, data_dict)
        
        # Should return user dict on successful login
        assert isinstance(result, dict)
        assert result['name'] == 'testuser'
        assert result['email'] == 'test@example.com'

    @pytest.mark.usefixtures("clean_db", "with_plugins")
    def test_user_login_with_email(self):
        """Test login with email address."""
        # Create a test user
        user = factories.User(
            name='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
        
        context = {'model': model}
        data_dict = {
            'id': 'test2@example.com',  # Using email instead of username
            'password': 'testpass123'
        }
        
        result = user_login(context, data_dict)
        
        # Should return user dict on successful login
        assert isinstance(result, dict)
        assert result['name'] == 'testuser2'
        assert result['email'] == 'test2@example.com'

    @pytest.mark.usefixtures("clean_db", "with_plugins")
    def test_user_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        # Create a test user
        user = factories.User(
            name='testuser3',
            email='test3@example.com',
            password='testpass123'
        )
        
        context = {'model': model}
        data_dict = {
            'id': 'testuser3',
            'password': 'wrongpassword'
        }
        
        result = user_login(context, data_dict)
        
        # Should return error message on failed login
        assert 'errors' in result
        assert 'auth' in result['errors']

    @pytest.mark.usefixtures("clean_db", "with_plugins")
    def test_user_login_nonexistent_user(self):
        """Test login with non-existent user."""
        context = {'model': model}
        data_dict = {
            'id': 'nonexistent@example.com',
            'password': 'somepassword'
        }
        
        result = user_login(context, data_dict)
        
        # Should return error message for non-existent user
        assert 'errors' in result
        assert 'auth' in result['errors']