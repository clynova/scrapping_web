# Scraper de Mercado Libre - Viaje Azul Chile
# Script automatizado para extraer productos de la tienda

import subprocess
import sys
import os

def main():
    print("\n" + "="*70)
    print(" SCRAPER AUTOMÁTICO - TIENDA VIAJE AZUL (MERCADO LIBRE CHILE)")
    print("="*70)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists('scraper_mercadolibre_v2.py'):
        print("\n❌ Error: No se encuentra el archivo scraper_mercadolibre_v2.py")
        print("Asegúrate de ejecutar este script desde el directorio correcto")
        sys.exit(1)
    
    # Activar entorno virtual y ejecutar scraper
    print("\n🚀 Iniciando scraper...")
    print("⏳ Este proceso puede tardar varios minutos\n")
    
    cmd = [
        'bash', '-c',
        'source venv/bin/activate && python scraper_mercadolibre_v2.py'
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False, text=True)
        
        print("\n" + "="*70)
        print("✅ SCRAPING COMPLETADO EXITOSAMENTE")
        print("="*70)
        
        # Verificar archivos generados
        if os.path.exists('viaje_azul_productos.xlsx'):
            size_excel = os.path.getsize('viaje_azul_productos.xlsx') / 1024
            print(f"\n📄 Archivo Excel generado: viaje_azul_productos.xlsx ({size_excel:.1f} KB)")
        
        if os.path.exists('viaje_azul_productos.csv'):
            size_csv = os.path.getsize('viaje_azul_productos.csv') / 1024
            print(f"📄 Archivo CSV generado: viaje_azul_productos.csv ({size_csv:.1f} KB)")
        
        if os.path.exists('imagenes_mercadolibre'):
            num_imagenes = len([f for f in os.listdir('imagenes_mercadolibre') if f.endswith('.jpg')])
            print(f"🖼️  Imágenes descargadas: {num_imagenes} archivos en imagenes_mercadolibre/")
        
        print("\n💡 Puedes abrir los archivos con:")
        print("   - Excel/LibreOffice: viaje_azul_productos.xlsx")
        print("   - Editor de texto: viaje_azul_productos.csv")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error al ejecutar el scraper: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Proceso interrumpido por el usuario")
        sys.exit(0)

if __name__ == "__main__":
    main()
