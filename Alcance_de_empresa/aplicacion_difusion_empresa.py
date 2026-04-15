import math
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

class ModeloDifusionEmpresa:
    """
    Representa el modelo logistico de difusion de conocimiento de una empresa.

    Usa la ecuacion dE/dt = k*E*(M - E) para estimar cuantas personas
    conocen la empresa con el paso del tiempo.
    """
    
    def __init__(self, E0, M, k):
        """
        Guarda los parametros iniciales del modelo.
        
        Args:
            E0 (float): Número inicial de personas que conocen la empresa
            M (float): Población máxima/potencial (personas que podrían conocer)
            k (float): Constante de proporcionalidad (tasa de crecimiento)
        """
        # Guardamos los datos base que definen el escenario.
        self.E0 = E0
        self.M = M
        self.k = k
        # A es una constante de la solucion analitica del modelo logistico.
        self.A = (M - E0) / E0 if E0 != 0 else 0
        
    def personas_en_tiempo(self, t):
        """
        Devuelve cuantas personas conocen la empresa en un tiempo t.
        
        Args:
            t (float): Tiempo transcurrido
            
        Returns:
            float: Número de personas que conocen la empresa
        """
        # Si A = 0, el modelo ya parte en el maximo teorico.
        if self.A == 0:
            return self.M
        # Formula cerrada del crecimiento logistico.
        E_t = self.M / (1 + self.A * math.exp(-self.k * t))
        return E_t
    
    def promedio_personas(self, t_final):
        """
        Calcula el promedio de personas en el intervalo [0, t_final].
        
        Args:
            t_final (float): Tiempo final del intervalo
            
        Returns:
            float: Promedio de personas en el intervalo
        """
        if t_final == 0:
            return self.personas_en_tiempo(0)

        # Usar integración numérica para calcular el promedio
        # Promedio = integral(E(t)dt) / t_final desde 0 a t_final
        
        # Muestreamos muchos puntos para aproximar bien el area bajo la curva.
        n_puntos = 1000
        t_valores = np.linspace(0, t_final, n_puntos)
        E_valores = [self.personas_en_tiempo(t) for t in t_valores]
        
        # Integración numérica (regla del trapecio).
        # En NumPy recientes usar trapezoid; mantener fallback por compatibilidad.
        integral = np.trapezoid(E_valores, t_valores) if hasattr(np, 'trapezoid') else np.trapz(E_valores, t_valores)
        # Promedio = area acumulada / longitud del intervalo.
        promedio = integral / t_final
        
        return promedio
    
    def porcentaje_penetracion(self, t):
        """
        Calcula el porcentaje de Difusion en el tiempo t.
        
        Args:
            t (float): Tiempo
            
        Returns:
            float: Porcentaje (0-100)
        """
        # Convertimos personas estimadas a porcentaje del mercado total.
        E_t = self.personas_en_tiempo(t)
        return (E_t / self.M) * 100
    
    def tiempo_para_penetracion(self, porcentaje):
        """
        Estima el tiempo necesario para alcanzar un porcentaje objetivo.
        
        Args:
            porcentaje (float): Porcentaje deseado (0-100)
            
        Returns:
            float: Tiempo necesario
        """
        if porcentaje >= 100:
            return float('inf')
        
        # Traducimos el porcentaje objetivo a cantidad de personas.
        E_objetivo = (porcentaje / 100) * self.M
        
        if E_objetivo <= self.E0:
            return 0
        
        # Despejar t de: E(t) = M / (1 + A*e^(-kt))
        # E_objetivo = M / (1 + A*e^(-kt))
        # 1 + A*e^(-kt) = M / E_objetivo
        # A*e^(-kt) = M/E_objetivo - 1
        # e^(-kt) = (M/E_objetivo - 1) / A
        # -kt = ln((M/E_objetivo - 1) / A)
        # t = -ln((M/E_objetivo - 1) / A) / k
        
        if self.A == 0:
            return 0
        
        # Validamos que el logaritmo reciba un valor positivo.
        argumento = (self.M / E_objetivo - 1) / self.A
        if argumento <= 0:
            return 0
        
        # Tiempo despejado de la ecuacion logistica.
        t = -math.log(argumento) / self.k
        return max(0, t)


def obtener_datos_usuario():
    """
    Pide por consola los datos de entrada y valida reglas basicas.
    
    Returns:
        tuple: (E0, M, k, t_final)
    """
    print("\n" + "="*60)
    print("  CÁLCULO DE DIFUSIÓN DE CONOCIMIENTO SOBRE UNA EMPRESA")
    print("  Basado en Ecuaciones Diferenciales")
    print("="*60 + "\n")
    
    try:
        print("Ingresa los siguientes parámetros:\n")
        
        # Leemos y validamos cada dato para evitar escenarios invalidos.
        E0 = float(input("1. Número inicial de personas que conocen la empresa (E₀): "))
        if E0 < 0:
            print("   Error: El número inicial debe ser mayor o igual a 0")
            return None
        
        M = float(input("2. Población máxima/potencial (M): "))
        if M <= E0:
            print("   Error: La población máxima debe ser mayor que E₀")
            return None
        
        k = float(input("3. Constante de proporcionalidad/tasa de crecimiento (k): "))
        if k <= 0:
            print("   Error: La constante k debe ser mayor a 0")
            return None
        
        t_final = float(input("4. Tiempo transcurrido en días/horas/unidades (t): "))
        if t_final < 0:
            print("   Error: El tiempo debe ser mayor o igual a 0")
            return None
        
        # Devolvemos todos los parametros en una tupla para usarla en el flujo principal.
        return (E0, M, k, t_final)
    
    except ValueError:
        print("   Error: Ingresa valores numéricos válidos")
        return None


def mostrar_resultados(modelo, t_final):
    """
    Muestra por consola los resultados principales del analisis.
    
    Args:
        modelo (ModeloDifusionEmpresa): El modelo calculado
        t_final (float): Tiempo final
    """
    print("\n" + "="*60)
    print("  RESULTADOS DEL ANÁLISIS")
    print("="*60 + "\n")
    
    # Calculamos metricas principales para mostrarlas juntas.
    E_inicial = modelo.personas_en_tiempo(0)
    E_final = modelo.personas_en_tiempo(t_final)
    promedio = modelo.promedio_personas(t_final)
    porcentaje_final = modelo.porcentaje_penetracion(t_final)
    
    print(f"PARÁMETROS DEL MODELO:")
    print(f"  E₀ (inicial):        {round(E_inicial)} personas")
    print(f"  M (máximo potencial): {round(modelo.M)} personas")
    print(f"  k (tasa crecimiento): {modelo.k:.4f}")
    print(f"\nRESULTADOS EN t = {round(t_final)} unidades:")
    print(f"  Personas que conocen la empresa: {round(E_final)}")
    print(f"  Porcentaje de alcance:          {round(porcentaje_final)}%")
    print(f"\nPROMEDIO en el intervalo [0, {round(t_final)}]:")
    print(f"  Promedio de personas: {round(promedio)}")
    
    # Puntos adicionales de interés
    print(f"\nPUNTOS DE INTERÉS:")
    for porcentaje in [25, 50, 75, 90]:
        t_necesario = modelo.tiempo_para_penetracion(porcentaje)
        if t_necesario != float('inf'):
            print(f"  Tiempo para {porcentaje}% de alcance: {round(t_necesario)} unidades")
    
    print("\n" + "="*60 + "\n")


def generar_grafico(modelo, t_final, graficar=True):
    """
    Dibuja y guarda los graficos de crecimiento y alcance.
    
    Args:
        modelo (ModeloDifusionEmpresa): El modelo
        t_final (float): Tiempo final
        graficar (bool): Si True, muestra el gráfico
    """
    if not graficar:
        return
    
    # Generamos puntos de tiempo para dibujar curvas suaves.
    t_valores = np.linspace(0, t_final, 500)
    E_valores = [modelo.personas_en_tiempo(t) for t in t_valores]
    
    plt.figure(figsize=(12, 5))
    
    # Gráfico 1: Número de personas
    plt.subplot(1, 2, 1)
    plt.plot(t_valores, E_valores, 'b-', linewidth=2, label='E(t)')
    plt.axhline(y=modelo.M, color='r', linestyle='--', label=f'Máximo (M={modelo.M:.0f})')
    plt.axhline(y=modelo.promedio_personas(t_final), color='g', linestyle='--', 
                label=f'Promedio={round(modelo.promedio_personas(t_final))}')
    plt.xlabel('Tiempo (unidades)')
    plt.ylabel('Número de personas')
    plt.title('Difusión de conocimiento sobre la empresa')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Gráfico 2: Porcentaje de alcance
    plt.subplot(1, 2, 2)
    porcentaje_valores = [modelo.porcentaje_penetracion(t) for t in t_valores]
    plt.plot(t_valores, porcentaje_valores, 'r-', linewidth=2)
    plt.axhline(y=50, color='k', linestyle=':', alpha=0.5, label='50% alcance')
    plt.xlabel('Tiempo (unidades)')
    plt.ylabel('Porcentaje de alcance (%)')
    plt.title('Alcance de mercado')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.ylim(0, 105)
    
    # Ajustamos margenes y guardamos el resultado en un archivo.
    plt.tight_layout()
    plt.savefig('grafico_difusion.png')
    print("✓ Gráfico guardado como 'grafico_difusion.png'")
    plt.show()


def menu_principal():
    """Ejecuta el flujo interactivo principal de la aplicacion en consola."""
    while True:
        # Pedimos datos para una corrida completa del modelo.
        datos = obtener_datos_usuario()
        
        if datos is None:
            reintentar = input("\n¿Deseas intentar de nuevo? (s/n): ").lower()
            if reintentar != 's':
                print("\n¡Hasta luego!")
                break
            continue
        
        # Desempaquetamos los parametros ingresados por el usuario.
        E0, M, k, t_final = datos
        
        # Crear el modelo
        modelo = ModeloDifusionEmpresa(E0, M, k)
        
        # Mostrar resultados
        mostrar_resultados(modelo, t_final)
        
        # Preguntar si desea gráfico
        grafico = input("¿Deseas generar un gráfico? (s/n): ").lower()
        if grafico == 's':
            try:
                generar_grafico(modelo, t_final, graficar=True)
            except Exception as e:
                print(f"No se pudo generar el gráfico: {e}")
        
        # Preguntar si desea continuar
        continuar = input("\n¿Deseas hacer otro cálculo? (s/n): ").lower()
        if continuar != 's':
            print("\n¡Gracias por usar la aplicación!")
            break


if __name__ == "__main__":
    print("\n" + "="*60)
    print("  Iniciando aplicación...")
    print("="*60)
    menu_principal()
