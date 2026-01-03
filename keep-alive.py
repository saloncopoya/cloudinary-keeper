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
CLOUDINARY_ACCOUNTS = [
    {
        "name": "Cuenta 1",
        "cloud_name": "dxjgyqcby",  # Ejemplo: "dvcuroh7"
        "api_key": "871575764573387",        # Ejemplo: "123456789012345"
        "upload_preset": "sinfirmaupload"
    },
    {
        "name": "Cuenta 2",
        "cloud_name": "dvcuroh7x",
        "api_key": "994915652739941",
        "upload_preset": "sinfirmaupload"
    },
    {
        "name": "Cuenta 3",
        "cloud_name": "dnfbrycla",
        "api_key": "966771178448349",
        "upload_preset": "presetsinfirma3"
    },
    {
        name": "Cuenta 4",
        "cloud_name": "davovja1g",
        "api_key": "688569119694815",
        "upload_preset": "sinfirmaupload"
    }
]

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
