"""Tests for plugin.py."""
import pytest
from unittest.mock import Mock, MagicMock
import ckanext.auth.logic as logic

class TestUserLogin:
    
    def test_user_login_with_username(self):
        """Test login with username"""
        # Mock context and model
        context = {'model': Mock()}
        user_mock = Mock()
        user_mock.as_dict.return_value = {'name': 'testuser', 'email': 'test@example.com'}
        context['model'].User.get.return_value = user_mock
        context['model'].User.by_email.return_value = None
        
        data_dict = {'id': 'testuser', 'password': 'testpass'}
        
        # Mock authenticator
        with pytest.patch('ckanext.auth.logic.authenticator') as mock_auth:
            auth_instance = Mock()
            auth_instance.authenticate.return_value = 'testuser'
            mock_auth.UsernamePasswordAuthenticator.return_value = auth_instance
            
            result = logic.user_login(context, data_dict)
            
            assert result == {'name': 'testuser', 'email': 'test@example.com'}
            context['model'].User.get.assert_called_once_with('testuser')
    
    def test_user_login_with_email(self):
        """Test login with email when username not found"""
        # Mock context and model
        context = {'model': Mock()}
        user_mock = Mock()
        user_mock.as_dict.return_value = {'name': 'testuser', 'email': 'test@example.com'}
        context['model'].User.get.return_value = None  # Username not found
        context['model'].User.by_email.return_value = user_mock  # Email found
        
        data_dict = {'id': 'test@example.com', 'password': 'testpass'}
        
        # Mock authenticator
        with pytest.patch('ckanext.auth.logic.authenticator') as mock_auth:
            auth_instance = Mock()
            auth_instance.authenticate.return_value = 'testuser'
            mock_auth.UsernamePasswordAuthenticator.return_value = auth_instance
            
            result = logic.user_login(context, data_dict)
            
            assert result == {'name': 'testuser', 'email': 'test@example.com'}
            context['model'].User.get.assert_called_once_with('test@example.com')
            context['model'].User.by_email.assert_called_once_with('test@example.com')
    
    def test_user_login_user_not_found(self):
        """Test login with non-existent user"""
        # Mock context and model
        context = {'model': Mock()}
        context['model'].User.get.return_value = None
        context['model'].User.by_email.return_value = None
        
        data_dict = {'id': 'nonexistent', 'password': 'testpass'}
        
        result = logic.user_login(context, data_dict)
        
        expected_error = {
            'errors': {
                'auth': ['Username or password entered was incorrect']
            },
            'error_summary': {'auth': 'Incorrect username or password'}
        }
        
        assert 'errors' in result
        assert 'auth' in result['errors']

def test_plugin():
    """Original test - keeping for compatibility"""
    pass