#!/usr/bin/env python3
"""
Script para mantener cuentas Cloudinary activas
Sube un pixel transparente de 1x1 cada 15 días
"""

import requests
import base64
from datetime import datetime
import os

# ==============================================
# TUS 4 CUENTAS CLOUDINARY - ¡EDITA ESTO!
# ==============================================
# ==============================================
# CONFIGURACIÓN DESDE VARIABLES DE ENTORNO
# ==============================================
import os

CLOUDINARY_ACCOUNTS = []

# Agregar cuentas desde variables de entorno
for i in range(1, 5):  # Para 4 cuentas
    cloud_name = os.environ.get(f'CLOUD_NAME_{i}')
    api_key = os.environ.get(f'API_KEY_{i}')
    
    if cloud_name and api_key:
        CLOUDINARY_ACCOUNTS.append({
            "name": f"Cuenta {i}",
            "cloud_name": cloud_name,
            "api_key": api_key,
            "upload_preset": "ml_default"
        })

# Verificar que hay cuentas
if not CLOUDINARY_ACCOUNTS:
    print("❌ ERROR: No se configuraron cuentas Cloudinary")
    print("   Verifica los secrets en GitHub")
    exit(1)

print(f"✅ Cuentas configuradas: {len(CLOUDINARY_ACCOUNTS)}")

# ==============================================
# PIXEL TRANSPARENTE de 1x1 (Base64)
# ==============================================
PIXEL_1x1 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="

def upload_pixel(account):
    """Sube un pixel de 1x1 a Cloudinary"""
    
    print(f"📤 Subiendo pixel a {account['name']}...")
    
    # URL de upload de Cloudinary
    upload_url = f"https://api.cloudinary.com/v1_1/{account['cloud_name']}/image/upload"
    
    # Preparar datos del pixel
    pixel_data = base64.b64decode(PIXEL_1x1)
    
    # Crear FormData simulado
    files = {
        'file': ('pixel.png', pixel_data, 'image/png')
    }
    
    data = {
        'upload_preset': account['upload_preset'],
        'api_key': account['api_key'],
        'public_id': f'keep_alive_{datetime.now().strftime("%Y%m%d")}',
        'tags': 'keep_alive,auto_generated'
    }
    
    try:
        response = requests.post(upload_url, files=files, data=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ {account['name']}: Pixel subido")
            return True
        else:
            print(f"❌ {account['name']}: Error {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ {account['name']}: Error de conexión - {str(e)}")
        return False

def main():
    """Función principal"""
    print("=" * 50)
    print("🔄 INICIANDO MANTENIMIENTO CLOUDINARY")
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    successes = 0
    failures = 0
    
    # Subir pixel a cada cuenta
    for account in CLOUDINARY_ACCOUNTS:
        if upload_pixel(account):
            successes += 1
        else:
            failures += 1
        print("-" * 40)
    
    # Resumen
    print("=" * 50)
    print("📊 RESUMEN:")
    print(f"   ✅ Éxitos: {successes}")
    print(f"   ❌ Fallos: {failures}")
    print("=" * 50)
    
    # Devolver código de salida
    if failures > 0:
        exit(1)
    else:
        exit(0)

if __name__ == "__main__":
    main()
