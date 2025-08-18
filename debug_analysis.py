#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de depuración para analizar el problema de login.
"""

def analyze_login_issue():
    """
    Analiza el problema de login basado en la respuesta de la API.
    """
    print("=== Análisis del problema de login ===\n")
    
    print("Problema identificado:")
    print("La API devuelve success=true pero con un result que contiene errores")
    print("Esto sugiere que la función está devolviendo el mensaje de error")
    print("como si fuera un resultado exitoso.\n")
    
    print("Posibles causas:")
    print("1. ❌ La función original no usa ValidationError sino que devuelve diccionarios")
    print("2. ❌ El usuario 'ckan_admin' no existe en la base de datos")
    print("3. ❌ El email 'projas@cazalac.org' no está asociado a ningún usuario")
    print("4. ❌ La contraseña es incorrecta")
    print("5. ❌ El usuario existe pero está inactivo\n")
    
    print("Soluciones implementadas:")
    print("1. ✅ Cambiado para usar ValidationError en lugar de diccionarios")
    print("2. ✅ Agregado logging detallado para depuración")
    print("3. ✅ Validación de usuario activo")
    print("4. ✅ Mejor manejo de errores\n")
    
    print("Para verificar:")
    print("1. Revisar logs de CKAN para ver los mensajes de debug")
    print("2. Verificar que el usuario 'ckan_admin' existe en la DB")
    print("3. Verificar que el email existe y está asociado al usuario correcto")
    print("4. Confirmar que la contraseña es correcta")
    print("5. Verificar que el plugin está cargado correctamente\n")
    
    print("Comandos útiles para verificar en el servidor:")
    print("# Verificar usuarios en CKAN")
    print("docker exec -it ckan /bin/bash")
    print("ckan -c /etc/ckan/production.ini user list")
    print("ckan -c /etc/ckan/production.ini user show ckan_admin")
    print()
    print("# Verificar logs")
    print("tail -f /var/log/ckan/ckan.log")

if __name__ == "__main__":
    analyze_login_issue()
