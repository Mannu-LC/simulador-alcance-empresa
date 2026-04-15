"""
Ejemplos de uso de la aplicación de difusión de empresa
Este archivo muestra diferentes escenarios y cómo usarlos
"""

from aplicacion_difusion_empresa import ModeloDifusionEmpresa

def ejemplo_1_startup_pequena():
    """
    Simula una startup pequena con crecimiento lento por recomendacion.
    """
    print("\n" + "="*60)
    print("EJEMPLO 1: STARTUP PEQUEÑA - CRECIMIENTO POR BOCA A BOCA")
    print("="*60)
    
    # Una startup con 5 personas iniciales
    # En una población potencial de 1000 personas
    # Tasa baja de crecimiento (0.03)
    modelo = ModeloDifusionEmpresa(E0=5, M=1000, k=0.03)
    
    print(f"\nEscenario:")
    print(f"  - Personas iniciales (E₀): 5")
    print(f"  - Población máxima (M): 1,000")
    print(f"  - Tasa de crecimiento (k): 0.03")
    
    # Mostramos evolucion en momentos puntuales.
    for t in [10, 30, 50, 100]:
        personas = modelo.personas_en_tiempo(t)
        porcentaje = modelo.porcentaje_penetracion(t)
        print(f"\n  En t={t} días:")
        print(f"    - Personas: {personas:.0f}")
        print(f"    - Alcance: {porcentaje:.0f}%")
    
    # Resumen del comportamiento global del periodo.
    promedio = modelo.promedio_personas(100)
    print(f"\n  Promedio en [0, 100] días: {promedio:.0f} personas")


def ejemplo_2_empresa_establecida():
    """
    Simula una empresa establecida con mayor alcance por marketing.
    """
    print("\n" + "="*60)
    print("EJEMPLO 2: EMPRESA ESTABLECIDA - CRECIMIENTO CON MARKETING")
    print("="*60)
    
    # Empresa con 100 personas en día 1
    # Población potencial de 50,000
    # Tasa de crecimiento más alta (0.08)
    modelo = ModeloDifusionEmpresa(E0=100, M=50000, k=0.08)
    
    print(f"\nEscenario:")
    print(f"  - Personas iniciales (E₀): 100")
    print(f"  - Población máxima (M): 50,000")
    print(f"  - Tasa de crecimiento (k): 0.08")
    
    # Seguimiento del avance en distintos horizontes.
    for t in [10, 30, 50, 100, 200]:
        personas = modelo.personas_en_tiempo(t)
        porcentaje = modelo.porcentaje_penetracion(t)
        print(f"\n  En t={t} días:")
        print(f"    - Personas: {personas:.0f}")
        print(f"    - Alcance: {porcentaje:.0f}%")
    
    # Encontrar tiempo para hitos importantes
    print(f"\n  Hitos importantes:")
    # Hitos tipicos para medir adopcion del mercado.
    for porcentaje_objetivo in [25, 50, 75, 90]:
        t_necesario = modelo.tiempo_para_penetracion(porcentaje_objetivo)
        print(f"    - {porcentaje_objetivo}% de alcance en {t_necesario:.0f} días")


def ejemplo_3_red_social():
    """
    Simula una difusion viral en redes sociales.
    """
    print("\n" + "="*60)
    print("EJEMPLO 3: PROPAGACIÓN EN REDES SOCIALES - CRECIMIENTO RAPIDO")
    print("="*60)
    
    # Inicio con 50 personas
    # Población potencial de 100,000
    # Tasa muy alta de crecimiento (0.15 - viral)
    modelo = ModeloDifusionEmpresa(E0=50, M=100000, k=0.15)
    
    print(f"\nEscenario:")
    print(f"  - Personas iniciales (E₀): 50")
    print(f"  - Población máxima (M): 100,000")
    print(f"  - Tasa de crecimiento (k): 0.15 (VIRAL)")
    
    # Al ser viral, revisamos tiempos mas cortos.
    for t in [5, 10, 15, 20, 30]:
        personas = modelo.personas_en_tiempo(t)
        porcentaje = modelo.porcentaje_penetracion(t)
        print(f"\n  En t={t} días:")
        print(f"    - Personas: {personas:.0f}")
        print(f"    - Alcance: {porcentaje:.0f}%")
    
    # Comparamos promedio corto vs mediano plazo.
    promedio_15 = modelo.promedio_personas(15)
    promedio_30 = modelo.promedio_personas(30)
    print(f"\n  Promedio [0, 15] días: {promedio_15:.0f} personas")
    print(f"  Promedio [0, 30] días: {promedio_30:.0f} personas")


def ejemplo_4_comparacion():
    """
    Compara varios escenarios cambiando solo la tasa de crecimiento k.
    """
    print("\n" + "="*60)
    print("EJEMPLO 4: COMPARACION DE TASAS DE CRECIMIENTO")
    print("="*60)
    
    escenarios = [
        ("Muy lento", 2, 5000, 0.01),
        ("Lento", 5, 5000, 0.03),
        ("Moderado", 5, 5000, 0.05),
        ("Rápido", 5, 5000, 0.10),
        ("Muy rápido", 5, 5000, 0.15),
    ]
    
    t_analisis = [10, 30, 50, 100]
    
    # Recorremos escenarios para ver el efecto de cambiar k.
    for nombre, E0, M, k in escenarios:
        modelo = ModeloDifusionEmpresa(E0=E0, M=M, k=k)
        print(f"\n{nombre.upper()} (k={k}):")
        
        # Guardamos valores para imprimirlos en una sola linea.
        valores = []
        for t in t_analisis:
            personas = modelo.personas_en_tiempo(t)
            porcentaje = modelo.porcentaje_penetracion(t)
            valores.append(f"{personas:.0f}")
        
        print(f"  Personas en días {t_analisis}: {' → '.join(valores)}")
        
        # Tiempo para 50% de alcance
        t_50 = modelo.tiempo_para_penetracion(50)
        print(f"  Tiempo para 50% de alcance: {t_50:.0f} días")


def ejemplo_5_caso_real():
    """
    Presenta un caso realista de una app movil durante 12 meses.
    """
    print("\n" + "="*60)
    print("EJEMPLO 5: CASO REAL - APLICACION MOVIL")
    print("="*60)
    
    print("\nPremisas:")
    print("  - Aplicación móvil lanzada con 50 descargas iniciales")
    print("  - Población objetivo: 10,000 usuarios potenciales")
    print("  - Tasa de crecimiento: 0.05 (marketing orgánico)")
    print("  - Período de análisis: 1 año (365 días)")
    
    modelo = ModeloDifusionEmpresa(E0=50, M=10000, k=0.05)
    
    print(f"\nProyección:")
    print(f"{'Mes':<8} {'Días':<8} {'Descargas':<15} {'%Alcance':<15} {'Promedio':<15}")
    print("-" * 60)
    
    # Proyeccion mensual del primer ano.
    for mes in range(1, 13):
        t = mes * 30
        personas = modelo.personas_en_tiempo(t)
        porcentaje = modelo.porcentaje_penetracion(t)
        promedio = modelo.promedio_personas(t)
        print(f"{mes:<8} {t:<8} {personas:<15.0f} {porcentaje:<14.0f}% {promedio:<15.0f}")
    
    promedio_anual = modelo.promedio_personas(365)
    print(f"\nPromedio anual de descargas: {promedio_anual:.0f}")
    
    # En 365 días cuánto creció
    crecimiento_porcentual = ((modelo.personas_en_tiempo(365) - 50) / 50) * 100
    print(f"Crecimiento en 365 días: {crecimiento_porcentual:.0f}%")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("EJEMPLOS DE USO - APLICACION DE DIFUSION")
    print("="*60)
    
    # Ejecutar todos los ejemplos
    ejemplo_1_startup_pequena()
    ejemplo_2_empresa_establecida()
    ejemplo_3_red_social()
    ejemplo_4_comparacion()
    ejemplo_5_caso_real()
    
    print("\n" + "="*60)
    print("FIN DE LOS EJEMPLOS")
    print("="*60 + "\n")
