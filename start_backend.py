#!/usr/bin/env python3
"""
Script para iniciar el backend de CleanPoints.
Ejecuta la migración de la base de datos y luego inicia el servidor.
"""

import subprocess
import sys
import os

def main():
    print("🚀 Iniciando Backend de CleanPoints...")
    
    # Cambiar al directorio del script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # 1. Instalar dependencias si es necesario
    print("📦 Verificando dependencias...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Dependencias instaladas/verificadas")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Advertencia al instalar dependencias: {e}")
    
    # 2. Ejecutar migración de la base de datos
    print("🗄️  Ejecutando migración de la base de datos...")
    try:
        subprocess.run([sys.executable, "migrate_db.py"], check=True)
        print("✅ Migración completada")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Advertencia en la migración: {e}")
    
    # 3. Iniciar el servidor
    print("🌐 Iniciando servidor FastAPI...")
    print("📍 El backend estará disponible en: http://127.0.0.1:5000")
    print("📚 Documentación de la API: http://127.0.0.1:5000/docs")
    print("🔧 Para detener el servidor, presiona Ctrl+C")
    print("-" * 50)
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "127.0.0.1", 
            "--port", "5000", 
            "--reload"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al iniciar el servidor: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Servidor detenido por el usuario")
        sys.exit(0)

if __name__ == "__main__":
    main()
