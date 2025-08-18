#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para debuggear el login por email en ckanext-auth
"""

import requests
import json
import sys

def test_login(base_url, username_or_email, password):
    """Test login functionality"""
    
    endpoint = f"{base_url}/api/3/action/user_login"
    
    payload = {
        "id": username_or_email,
        "password": password
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    print(f"🔍 Testing login with: {username_or_email}")
    print(f"📡 Endpoint: {endpoint}")
    print(f"📦 Payload: {json.dumps(payload, indent=2)}")
    print("-" * 50)
    
    try:
        response = requests.post(endpoint, json=payload, headers=headers)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📋 Response:")
        
        if response.headers.get('content-type', '').startswith('application/json'):
            response_data = response.json()
            print(json.dumps(response_data, indent=2))
            
            if response_data.get('success'):
                print("✅ Login successful!")
                user_data = response_data.get('result', {})
                print(f"👤 User: {user_data.get('name', 'N/A')}")
                print(f"📧 Email: {user_data.get('email', 'N/A')}")
            else:
                print("❌ Login failed!")
                if 'result' in response_data and 'errors' in response_data['result']:
                    errors = response_data['result']['errors']
                    print(f"🚨 Errors: {errors}")
        else:
            print("⚠️  Non-JSON response:")
            print(response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"🔥 Request failed: {e}")
    
    print("=" * 50)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python debug_login.py <base_url> <username_or_email> <password>")
        print("Example: python debug_login.py https://data.dev-wins.com projas@cazalac.org mypassword")
        sys.exit(1)
    
    base_url = sys.argv[1]
    username_or_email = sys.argv[2]
    password = sys.argv[3]
    
    # Test with the provided credentials
    test_login(base_url, username_or_email, password)
    
    # If it's an email, also try to find the username and test with that
    if "@" in username_or_email:
        print("\n🔄 Email detected, you might also want to try with the username instead")
        print("💡 Check what the actual username is in CKAN admin interface")
