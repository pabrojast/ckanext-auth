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
        user_mock.as_dict.return_value = {'name': 'testuser', 'email': 'test@example.com'}
        context['model'].User.get.return_value = user_mock
        
        data_dict = {'id': 'testuser', 'password': 'testpass'}
        
        # Mock authenticator
        with pytest.patch('ckanext.auth.logic.authenticator') as mock_auth:
            auth_instance = Mock()
            auth_instance.authenticate.return_value = 'user123,1'  # user_id,status format
            mock_auth.UsernamePasswordAuthenticator.return_value = auth_instance
            
            result = logic.user_login(context, data_dict)
            
            assert result == {'name': 'testuser', 'email': 'test@example.com'}
            context['model'].User.get.assert_called_once_with('user123')
    
    def test_user_login_with_email(self):
        """Test login with email"""
        # Mock context and model
        context = {'model': Mock()}
        user_mock = Mock()
        user_mock.as_dict.return_value = {'name': 'testuser', 'email': 'test@example.com'}
        context['model'].User.get.return_value = user_mock
        
        data_dict = {'id': 'test@example.com', 'password': 'testpass'}
        
        # Mock authenticator
        with pytest.patch('ckanext.auth.logic.authenticator') as mock_auth:
            auth_instance = Mock()
            auth_instance.authenticate.return_value = 'user123,1'  # user_id,status format
            mock_auth.UsernamePasswordAuthenticator.return_value = auth_instance
            
            result = logic.user_login(context, data_dict)
            
            assert result == {'name': 'testuser', 'email': 'test@example.com'}
            context['model'].User.get.assert_called_once_with('user123')
    
    def test_user_login_authentication_failed(self):
        """Test login with authentication failure"""
        # Mock context and model
        context = {'model': Mock()}
        
        data_dict = {'id': 'testuser', 'password': 'wrongpass'}
        
        # Mock authenticator
        with pytest.patch('ckanext.auth.logic.authenticator') as mock_auth:
            auth_instance = Mock()
            auth_instance.authenticate.return_value = None  # Authentication failed
            mock_auth.UsernamePasswordAuthenticator.return_value = auth_instance
            
            result = logic.user_login(context, data_dict)
            
            assert 'errors' in result
            assert 'auth' in result['errors']
    
    def test_user_login_user_not_found_after_auth(self):
        """Test when authentication succeeds but user not found in database"""
        # Mock context and model
        context = {'model': Mock()}
        context['model'].User.get.return_value = None  # User not found
        
        data_dict = {'id': 'testuser', 'password': 'testpass'}
        
        # Mock authenticator
        with pytest.patch('ckanext.auth.logic.authenticator') as mock_auth:
            auth_instance = Mock()
            auth_instance.authenticate.return_value = 'user123,1'
            mock_auth.UsernamePasswordAuthenticator.return_value = auth_instance
            
            result = logic.user_login(context, data_dict)
            
            assert 'errors' in result
            assert 'auth' in result['errors']

def test_plugin():
    """Original test - keeping for compatibility"""
    import ckanext.auth.plugin as plugin
    # Just ensure the plugin can be imported
    assert plugin.AuthPlugin is not None