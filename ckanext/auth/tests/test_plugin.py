"""Tests for plugin.py."""
import pytest
from unittest.mock import Mock
import ckanext.auth.logic as logic

class TestUserLogin:
    
    def test_user_login_with_username(self):
        """Test login with username"""
        # Mock context and model
        context = {'model': Mock()}
        user_mock = Mock()
        user_mock.name = 'testuser'
        user_mock.as_dict.return_value = {'name': 'testuser', 'email': 'test@example.com'}
        context['model'].User.by_name.return_value = user_mock
        
        data_dict = {'id': 'testuser', 'password': 'testpass'}
        
        # Mock authenticator
        with pytest.patch('ckanext.auth.logic.authenticator') as mock_auth:
            mock_auth.ckan_authenticator.return_value = user_mock
            
            result = logic.user_login(context, data_dict)
            
            assert result == {'name': 'testuser', 'email': 'test@example.com'}
            context['model'].User.by_name.assert_called_once_with('testuser')
    
    def test_user_login_with_email(self):
        """Test login with email"""
        # Mock context and model
        context = {'model': Mock()}
        user_mock = Mock()
        user_mock.name = 'testuser'
        user_mock.as_dict.return_value = {'name': 'testuser', 'email': 'test@example.com'}
        context['model'].User.by_name.return_value = None
        context['model'].User.by_email2.return_value = user_mock
        
        data_dict = {'id': 'test@example.com', 'password': 'testpass'}
        
        # Mock authenticator
        with pytest.patch('ckanext.auth.logic.authenticator') as mock_auth:
            mock_auth.ckan_authenticator.return_value = user_mock
            
            result = logic.user_login(context, data_dict)
            
            assert result == {'name': 'testuser', 'email': 'test@example.com'}
            context['model'].User.by_email2.assert_called_once_with('test@example.com')
    
    def test_user_login_authentication_failed(self):
        """Test login with authentication failure"""
        # Mock context and model
        context = {'model': Mock()}
        user_mock = Mock()
        user_mock.name = 'testuser'
        context['model'].User.by_name.return_value = user_mock
        
        data_dict = {'id': 'testuser', 'password': 'wrongpass'}
        
        # Mock authenticator
        with pytest.patch('ckanext.auth.logic.authenticator') as mock_auth:
            mock_auth.ckan_authenticator.return_value = None  # Authentication failed
            
            result = logic.user_login(context, data_dict)
            
            assert 'errors' in result
            assert 'auth' in result['errors']
    
    def test_user_login_user_not_found_after_auth(self):
        """Test when authentication succeeds but user not found in database"""
        # Mock context and model
        context = {'model': Mock()}
        context['model'].User.by_name.return_value = None  # User not found
        context['model'].User.by_email2.return_value = None
        
        data_dict = {'id': 'testuser', 'password': 'testpass'}
        
        # Mock authenticator
        with pytest.patch('ckanext.auth.logic.authenticator') as mock_auth:
            mock_auth.ckan_authenticator.return_value = Mock()
            
            result = logic.user_login(context, data_dict)
            
            assert 'errors' in result
            assert 'auth' in result['errors']

def test_plugin():
    """Original test - keeping for compatibility"""
    import ckanext.auth.plugin as plugin
    # Just ensure the plugin can be imported
    assert plugin.AuthPlugin is not None
