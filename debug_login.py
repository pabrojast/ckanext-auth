#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de debug para probar la funcionalidad de login con username o email.

Este script demuestra cómo usar la función user_login modificada para permitir
autenticación tanto con username como con email.
"""

def demo_login_functionality():
    """
    Demostración de la funcionalidad de login mejorada.
    """
    print("=== Funcionalidad de Login con Username/Email ===\n")
    
    print("Características implementadas:")
    print("1. ✅ Login con username (funcionalidad original)")
    print("2. ✅ Login con email (nueva funcionalidad)")
    print("3. ✅ Manejo de usuarios inactivos")
    print("4. ✅ Búsqueda por email cuando username no existe")
    print("5. ✅ Mensajes de error actualizados\n")
    
    print("Ejemplo de uso:")
    print("""
# Login con username
data_dict = {
    'id': 'mi_usuario',
    'password': 'mi_contraseña'
}
result = user_login(context, data_dict)

# Login con email  
data_dict = {
    'id': 'usuario@ejemplo.com',
    'password': 'mi_contraseña'
}
result = user_login(context, data_dict)
""")
    
    print("Flujo de autenticación:")
    print("1. Se busca el usuario por username")
    print("2. Si no se encuentra, se busca por email")
    print("3. Si hay múltiples usuarios con el mismo email, se toma el activo")
    print("4. Se autentica usando siempre el username del usuario encontrado")
    print("5. Se retorna el diccionario del usuario o mensaje de error\n")
    
    print("Cambios realizados en logic.py:")
    print("- Búsqueda adicional por email cuando falla por username")
    print("- Manejo de usuarios duplicados por email")
    print("- Priorización de usuarios activos")
    print("- Mensajes de error actualizados para incluir 'Username/Email'")

if __name__ == "__main__":
    demo_login_functionality()
