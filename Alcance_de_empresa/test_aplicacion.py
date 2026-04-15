"""
Script de prueba rápida para verificar que la aplicación funciona
Ejecuta: python test_aplicacion.py
"""

import sys

def test_imports():
    """Comprueba que las librerias y modulos del proyecto cargan bien."""
    print("🔍 Verificando dependencias...")
    
    try:
        # Dependencia principal para calculo numerico.
        import numpy
        print("  ✓ NumPy instalado")
    except ImportError:
        print("  ✗ NumPy NO instalado. Ejecuta: pip install numpy")
        return False
    
    try:
        # Matplotlib es opcional porque solo se usa para graficos.
        import matplotlib
        print("  ✓ Matplotlib instalado")
    except ImportError:
        print("  ✓ Matplotlib no instalado (opcional, para gráficos)")
    
    try:
        # Import del modulo central del proyecto.
        from aplicacion_difusion_empresa import ModeloDifusionEmpresa
        print("  ✓ ModeloDifusionEmpresa importado correctamente")
    except ImportError as e:
        print(f"  ✗ Error importando ModeloDifusionEmpresa: {e}")
        return False
    
    return True


def test_modelo():
    """Valida los calculos principales del modelo con un caso de prueba."""
    print("\n🧪 Probando modelo de difusión...")
    
    from aplicacion_difusion_empresa import ModeloDifusionEmpresa
    
    try:
        # Crear modelo de prueba
        modelo = ModeloDifusionEmpresa(E0=10, M=1000, k=0.05)
        print("  ✓ Modelo creado exitosamente")
        
        # Prueba 1: el valor debe crecer, pero mantenerse bajo el maximo M.
        personas_t50 = modelo.personas_en_tiempo(50)
        assert 10 < personas_t50 < 1000, "Valor fuera de rango esperado"
        print(f"  ✓ Cálculo en t=50: {personas_t50:.0f} personas")
        
        # Prueba 2: el promedio del intervalo debe tener sentido fisico.
        promedio = modelo.promedio_personas(50)
        assert 10 < promedio < personas_t50, "Promedio inválido"
        print(f"  ✓ Promedio en [0, 50]: {promedio:.0f} personas")
        
        # Prueba 3: el porcentaje siempre debe estar entre 0 y 100.
        porcentaje = modelo.porcentaje_penetracion(50)
        assert 0 < porcentaje < 100, "Porcentaje fuera de rango"
        print(f"  ✓ Alcance en t=50: {porcentaje:.0f}%")
        
        # Prueba 4: el tiempo para una meta valida debe ser positivo.
        t_50pct = modelo.tiempo_para_penetracion(50)
        assert t_50pct > 0, "Tiempo inválido"
        print(f"  ✓ Tiempo para 50% de alcance: {t_50pct:.0f} unidades")
        
        return True
        
    except AssertionError as e:
        print(f"  ✗ Error en prueba: {e}")
        return False
    except Exception as e:
        print(f"  ✗ Error inesperado: {e}")
        return False


def test_ejemplos():
    """Verifica que el archivo de ejemplos se puede importar sin errores."""
    print("\n📚 Verificando ejemplos...")
    
    try:
        import ejemplos_uso
        print("  ✓ Módulo de ejemplos importado")
        print("  Nota: Para ver los 5 ejemplos, ejecuta: python ejemplos_uso.py")
        return True
    except ImportError:
        print("  ✗ No se pudo importar ejemplos_uso.py")
        return False


def main():
    """Ejecuta toda la bateria de pruebas y muestra el resultado final."""
    print("\n" + "="*60)
    print("  PRUEBA DE APLICACION - DIFUSION DE EMPRESA")
    print("="*60 + "\n")
    
    # Etapa 1: verificar entorno y modulos.
    if not test_imports():
        print("\n❌ FALLO: Por favor instala las dependencias")
        print("   Ejecuta: pip install -r requirements.txt")
        return False
    
    # Etapa 2: validar calculos del modelo.
    if not test_modelo():
        print("\n❌ FALLO: El modelo tiene errores")
        return False
    
    # Etapa 3: revisar que ejemplos esten disponibles.
    if not test_ejemplos():
        print("\n⚠️  Advertencia: Los ejemplos no se pueden ejecutar")
        return True  # No es fatal
    
    # Éxito
    print("\n" + "="*60)
    print("  ✅ TODAS LAS PRUEBAS PASARON CORRECTAMENTE")
    print("="*60)
    print("\n📝 Próximos pasos:")
    print("  1. Ejecuta: python aplicacion_difusion_empresa.py")
    print("  2. O llama: python ejemplos_uso.py")
    print("\n" + "="*60 + "\n")
    
    return True


if __name__ == "__main__":
    exito = main()
    sys.exit(0 if exito else 1)
