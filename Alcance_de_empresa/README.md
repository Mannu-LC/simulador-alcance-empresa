# Proyecto de Ecuaciones Diferenciales: Difusion de conocimiento de una empresa

Este proyecto simula como una empresa se va dando a conocer con el paso del tiempo.

La aplicacion recibe datos iniciales, realiza calculos matematicos y muestra resultados en formato numerico y en graficas.

## Que hace el proyecto

- Calcula cuantas personas conocen la empresa en un tiempo dado.
- Calcula el porcentaje de alcance sobre el mercado potencial.
- Calcula el promedio de personas en un intervalo de tiempo.
- Estima el tiempo necesario para llegar a metas de alcance (25%, 50%, 75%, 90%).
- Muestra resultados en consola y en interfaz grafica.

## Idea matematica usada

Se usa un modelo de crecimiento logistico basado en ecuaciones diferenciales para representar un crecimiento realista:

- Al inicio crece lento
- Luego acelera
- Finalmente se estabiliza cerca de un limite maximo

Ecuacion base:

```text
dE/dt = k * E * (M - E)
```

Variables principales:

- `E0`: personas que conocen la empresa al inicio.
- `M`: maximo de personas que podrian conocerla.
- `k`: velocidad de crecimiento.
- `t`: tiempo que se desea analizar.

## Estructura principal

- `aplicacion_difusion_empresa.py`: logica matematica y version en consola.
- `aplicacion_difusion_gui.py`: version con interfaz grafica.
- `ejemplos_uso.py`: escenarios de ejemplo.
- `test_aplicacion.py`: pruebas rapidas de funcionamiento.
- `requirements.txt`: dependencias del proyecto.
- `docs/`: documentos de apoyo y entregables.

## Requisitos

- Python 3.8 o superior

## Instalacion y ejecucion

1. Instalar dependencias:

```bash
pip install -r requirements.txt
```

2. Ejecutar interfaz grafica:

```bash
python aplicacion_difusion_gui.py
```

3. Ejecutar version consola:

```bash
python aplicacion_difusion_empresa.py
```

4. Ejecutar ejemplos:

```bash
python ejemplos_uso.py
```

5. Ejecutar pruebas:

```bash
python test_aplicacion.py
```

## Salida del programa

El sistema muestra los resultados en numeros enteros para que sean mas faciles de leer en reportes y entregables.

## Uso academico

Proyecto realizado para practicar aplicacion de ecuaciones diferenciales en un caso real de difusion y alcance.
