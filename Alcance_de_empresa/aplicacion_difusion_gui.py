import tkinter as tk
from tkinter import ttk, messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from aplicacion_difusion_empresa import ModeloDifusionEmpresa


class AplicacionDifusionGUI:
    def __init__(self, root):
        """Crea la ventana principal y prepara el estado inicial."""
        # Configuracion base de la ventana.
        self.root = root
        self.root.title("Difusion de Empresa - Ecuaciones Diferenciales")
        self.root.geometry("980x720")
        self.root.minsize(900, 660)

        # Paleta minimalista basada en los tonos de referencia.
        self.color_fondo = "#F3F4F3"
        self.color_tarjeta = "#FFFFFF"
        self.color_texto = "#233332"
        self.color_muted = "#4D6160"
        self.color_acento = "#41E0D6"
        self.color_acento_secundario = "#53B6AF"
        self.color_borde = "#D9DEDD"
        self.color_botones = "#2E3636"

        self.root.configure(bg=self.color_fondo)

        # Estilo visual para resaltar acciones importantes.
        self.estilo = ttk.Style()
        self.estilo.theme_use("clam")
        self.estilo.configure("TFrame", background=self.color_fondo)
        self.estilo.configure("TLabel", background=self.color_fondo, foreground=self.color_texto, font=("Segoe UI", 10))
        self.estilo.configure("TLabelframe", background=self.color_fondo, foreground=self.color_texto)
        self.estilo.configure("TLabelframe.Label", background=self.color_fondo, foreground=self.color_texto, font=("Segoe UI", 10, "bold"))
        self.estilo.configure("Banner.TFrame", background=self.color_botones)
        self.estilo.configure("Banner.TLabel", background=self.color_botones, foreground="#FFFFFF")
        self.estilo.configure("Help.TLabel", background=self.color_fondo, foreground=self.color_muted, font=("Segoe UI", 9))
        self.estilo.configure("TButton", font=("Segoe UI", 10), padding=(10, 7))
        self.estilo.configure("Accent.TButton", background=self.color_acento_secundario, foreground="#FFFFFF")
        self.estilo.map("Accent.TButton", background=[("active", self.color_acento), ("pressed", self.color_acento_secundario)])
        self.estilo.configure("Exit.TButton", background=self.color_botones, foreground="#FFFFFF", font=("Segoe UI", 10, "bold"), padding=(14, 9))
        self.estilo.map("Exit.TButton", background=[("active", self.color_muted), ("pressed", self.color_botones)])

        # Estado interno: se completa luego de calcular.
        self.modelo_actual = None
        self.t_actual = None

        self._construir_ui()

    def _construir_ui(self):
        """Arma todos los controles de la interfaz (entradas, botones y salida)."""
        # Contenedor principal para organizar toda la UI.
        contenedor = ttk.Frame(self.root, padding=18)
        contenedor.pack(fill="both", expand=True)

        banner = ttk.Frame(contenedor, style="Banner.TFrame", padding=(18, 16))
        banner.pack(fill="x", pady=(0, 16))

        titulo = ttk.Label(
            banner,
            text="Calculadora de Difusion de Conocimiento de una Empresa",
            style="Banner.TLabel",
            font=("Segoe UI", 18, "bold"),
        )
        titulo.pack(anchor="w")

        subtitulo = ttk.Label(
            banner,
            text="Modelo logistico para estimar alcance, promedio y comportamiento de crecimiento.",
            style="Banner.TLabel",
            font=("Segoe UI", 10),
        )
        subtitulo.pack(anchor="w", pady=(4, 0))

        marco_entrada = ttk.LabelFrame(contenedor, text="Datos de entrada", padding=14)
        marco_entrada.pack(fill="x")

        # Valores por defecto para poder probar rapido.
        self.e0_var = tk.StringVar(value="10")
        self.m_var = tk.StringVar(value="10000")
        self.k_var = tk.StringVar(value="0.05")
        self.t_var = tk.StringVar(value="100")

        self._fila_input(marco_entrada, 0, "E0 (personas iniciales):", self.e0_var)
        self._fila_input(marco_entrada, 1, "M (personas maximas posibles):", self.m_var)
        self._fila_input(marco_entrada, 2, "k (tasa de crecimiento por unidad de tiempo):", self.k_var)
        self._fila_input(marco_entrada, 3, "t (tiempo en dias, semanas o meses):", self.t_var)

        ayuda = ttk.Label(
            marco_entrada,
            text="Guia: E0 es cuantas personas ya te conocen al inicio. M es el maximo de personas al que podrias llegar. k indica que tan rapido crece. t es el tiempo que quieres revisar.",
            style="Help.TLabel",
        )
        ayuda.grid(row=4, column=0, columnspan=2, sticky="w", pady=(8, 0))

        ayuda2 = ttk.Label(
            marco_entrada,
            text="Reglas: usa numeros positivos. E0 puede ser 0. M debe ser mayor que E0. k debe ser mayor que 0. t puede ser 0 o mayor. Si t esta en dias, piensa k tambien en dias.",
            style="Help.TLabel",
        )
        ayuda2.grid(row=5, column=0, columnspan=2, sticky="w", pady=(4, 0))

        marco_botones = ttk.Frame(contenedor)
        marco_botones.pack(fill="x", pady=14)

        ttk.Button(marco_botones, text="Calcular", command=self.calcular, style="Accent.TButton").pack(side="left")
        ttk.Button(marco_botones, text="Graficar", command=self.graficar).pack(side="left", padx=8)
        ttk.Button(marco_botones, text="Teoria", command=self.mostrar_teoria).pack(side="left")
        ttk.Button(marco_botones, text="Limpiar", command=self.limpiar).pack(side="left")
        ttk.Button(marco_botones, text="Salir", command=self.root.destroy, style="Exit.TButton").pack(side="right")

        marco_salida = ttk.LabelFrame(contenedor, text="Resultados", padding=14)
        marco_salida.pack(fill="both", expand=True)

        self.texto_resultados = tk.Text(
            marco_salida,
            wrap="word",
            font=("Consolas", 11),
            height=18,
            state="disabled",
            bg=self.color_tarjeta,
            fg=self.color_texto,
            insertbackground=self.color_texto,
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.color_borde,
            highlightcolor=self.color_acento,
        )
        self.texto_resultados.pack(fill="both", expand=True)

        self._escribir_resultados(
            "Ingresa los parametros de forma sencilla:\n"
            "- E0: personas que conocen la empresa al inicio\n"
            "- M: personas maximas que podrian conocerla\n"
            "- k: velocidad de crecimiento por unidad de tiempo\n"
            "- t: tiempo que deseas analizar\n\n"
            "Despues presiona Calcular y luego Graficar para ver la curva de difusion."
        )

    def _fila_input(self, parent, fila, etiqueta, variable):
        """Crea una fila de entrada con etiqueta y caja de texto."""
        ttk.Label(parent, text=etiqueta).grid(row=fila, column=0, sticky="w", pady=5)
        entrada = ttk.Entry(parent, textvariable=variable, width=24)
        entrada.grid(row=fila, column=1, sticky="w", pady=5, padx=(10, 0))

    def _leer_float(self, valor, nombre):
        """Convierte un texto a numero decimal y lanza un error claro si falla."""
        try:
            return float(valor)
        except ValueError as exc:
            # Re-lanzamos un mensaje amigable para mostrar en la GUI.
            raise ValueError(f"El campo {nombre} debe ser numerico") from exc

    def _validar_entradas(self, e0, m, k, t):
        """Valida reglas basicas del modelo antes de calcular."""
        if e0 < 0:
            raise ValueError("E0 debe ser mayor o igual a 0")
        if m <= e0:
            raise ValueError("M debe ser mayor que E0")
        if k <= 0:
            raise ValueError("k debe ser mayor que 0")
        if t < 0:
            raise ValueError("t debe ser mayor o igual a 0")

    def _escribir_resultados(self, contenido):
        """Muestra texto en el panel de resultados de forma segura."""
        # Habilitamos temporalmente para escribir y volvemos a solo lectura.
        self.texto_resultados.configure(state="normal")
        self.texto_resultados.delete("1.0", tk.END)
        self.texto_resultados.insert(tk.END, contenido)
        self.texto_resultados.configure(state="disabled")

    def mostrar_teoria(self):
        """Abre una ventana con una explicacion breve de la teoria y las graficas."""
        ventana = tk.Toplevel(self.root)
        ventana.title("Teoria del modelo")
        ventana.geometry("760x520")
        ventana.transient(self.root)
        ventana.grab_set()

        marco = ttk.Frame(ventana, padding=16)
        marco.pack(fill="both", expand=True)

        encabezado = ttk.Frame(marco)
        encabezado.pack(fill="x")

        titulo = ttk.Label(encabezado, text="Teoria del modelo", font=("Segoe UI", 14, "bold"))
        titulo.pack(side="left")

        ttk.Button(encabezado, text="Salir", command=ventana.destroy).pack(side="right")

        texto = tk.Text(marco, wrap="word", font=("Segoe UI", 11))
        texto.pack(fill="both", expand=True)

        contenido = (
            "Modelo logistico de difusion\n\n"
            "La aplicacion usa la ecuacion diferencial dE/dt = k*E*(M - E).\n"
            "E(t) representa cuantas personas conocen la empresa en el tiempo t.\n"
            "M es el tamano maximo del mercado potencial y k controla la velocidad\n"
            "de crecimiento.\n\n"
            "Interpretacion de la grafica izquierda:\n"
            "Muestra cuantas personas conocen la empresa conforme pasa el tiempo.\n"
            "Al inicio el crecimiento suele ser lento, despues se acelera y al final\n"
            "se estabiliza al acercarse al valor maximo M.\n\n"
            "Interpretacion de la grafica derecha:\n"
            "Muestra el porcentaje de alcance sobre el mercado potencial.\n"
            "Un valor bajo indica que aun hay mucho publico por alcanzar.\n"
            "Un valor alto indica que la empresa se aproxima a su saturacion.\n\n"
            "Promedio calculado:\n"
            "El programa tambien calcula el promedio de personas que conocieron\n"
            "la empresa durante el intervalo [0, t]. Esto permite interpretar el\n"
            "comportamiento general y no solo el valor final."
        )

        texto.insert("1.0", contenido)
        texto.configure(state="disabled")

    def mostrar_explicacion_grafica(self):
        """Abre una ventana con una explicacion breve del contenido de cada grafica."""
        ventana = tk.Toplevel(self.root)
        ventana.title("Explicacion de la grafica")
        ventana.geometry("760x430")
        ventana.transient(self.root)
        ventana.grab_set()

        marco = ttk.Frame(ventana, padding=16)
        marco.pack(fill="both", expand=True)

        titulo = ttk.Label(marco, text="Explicacion", font=("Segoe UI", 14, "bold"))
        titulo.pack(anchor="w")

        texto = tk.Text(marco, wrap="word", font=("Segoe UI", 11), height=16)
        texto.pack(fill="both", expand=True, pady=(10, 0))

        contenido = (
            "Grafica izquierda: muestra la cantidad de personas que conocen la empresa\n"
            "a lo largo del tiempo. La curva comienza lenta, luego acelera y finalmente\n"
            "se estabiliza cuando se acerca al maximo del mercado potencial.\n\n"
            "Grafica derecha: muestra el porcentaje de alcance sobre el mercado total.\n"
            "Si el valor es bajo, la empresa aun tiene espacio para crecer. Si es alto,\n"
            "la difusion ya se acerca a su limite.\n\n"
            "La linea horizontal del 50% sirve como referencia visual para identificar\n"
            "el punto medio de alcance."
        )

        texto.insert("1.0", contenido)
        texto.configure(state="disabled")

        botones = ttk.Frame(marco)
        botones.pack(fill="x", pady=(12, 0))
        ttk.Button(botones, text="Salir", command=ventana.destroy, style="Exit.TButton").pack(side="right")

    def mostrar_grafica(self):
        """Abre una ventana con la grafica primero y, debajo, las opciones de explicacion y salida."""
        ventana = tk.Toplevel(self.root)
        ventana.title("Grafica de difusion")
        ventana.geometry("1120x760")
        ventana.transient(self.root)
        ventana.grab_set()

        contenedor = ttk.Frame(ventana, padding=14)
        contenedor.pack(fill="both", expand=True)

        titulo = ttk.Label(contenedor, text="Grafica de difusion de la empresa", font=("Segoe UI", 14, "bold"))
        titulo.pack(anchor="w")

        figura = Figure(figsize=(11, 6), dpi=100)

        t_valores = [i * self.t_actual / 499 for i in range(500)] if self.t_actual else [0]
        E_valores = [self.modelo_actual.personas_en_tiempo(t) for t in t_valores]
        porcentaje_valores = [self.modelo_actual.porcentaje_penetracion(t) for t in t_valores]

        eje_izquierdo = figura.add_subplot(1, 2, 1)
        eje_izquierdo.plot(t_valores, E_valores, "b-", linewidth=2, label="E(t)")
        eje_izquierdo.axhline(y=self.modelo_actual.M, color='r', linestyle='--', label=f"Maximo (M={self.modelo_actual.M:.0f})")
        eje_izquierdo.axhline(y=self.modelo_actual.promedio_personas(self.t_actual), color='g', linestyle='--', label=f"Promedio={round(self.modelo_actual.promedio_personas(self.t_actual))}")
        eje_izquierdo.set_xlabel("Tiempo (unidades)")
        eje_izquierdo.set_ylabel("Numero de personas que conocen la empresa")
        eje_izquierdo.set_title("Numero de personas que conocen la empresa")
        eje_izquierdo.grid(True, alpha=0.3)
        eje_izquierdo.legend(fontsize=8)

        eje_derecho = figura.add_subplot(1, 2, 2)
        eje_derecho.plot(t_valores, porcentaje_valores, "r-", linewidth=2, label="% alcance")
        eje_derecho.axhline(y=50, color='k', linestyle=':', alpha=0.5, label='50% referencia')
        eje_derecho.set_xlabel("Tiempo (unidades)")
        eje_derecho.set_ylabel("Porcentaje de alcance")
        eje_derecho.set_title("Porcentaje de alcance")
        eje_derecho.grid(True, alpha=0.3)
        eje_derecho.legend(fontsize=8)
        eje_derecho.set_ylim(0, 105)

        figura.tight_layout()

        canvas = FigureCanvasTkAgg(figura, master=contenedor)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, pady=(10, 10))

        botones = ttk.Frame(contenedor)
        botones.pack(fill="x")

        ttk.Button(botones, text="Ver explicacion", command=self.mostrar_explicacion_grafica).pack(side="left")
        ttk.Button(botones, text="Salir", command=ventana.destroy).pack(side="right")

    def calcular(self):
        """Lee datos, ejecuta el modelo y presenta resultados en pantalla."""
        try:
            # 1) Leer y convertir entradas.
            e0 = self._leer_float(self.e0_var.get(), "E0")
            m = self._leer_float(self.m_var.get(), "M")
            k = self._leer_float(self.k_var.get(), "k")
            t = self._leer_float(self.t_var.get(), "t")

            # 2) Validar reglas del modelo.
            self._validar_entradas(e0, m, k, t)

            # 3) Calcular metricas principales.
            modelo = ModeloDifusionEmpresa(e0, m, k)

            e_final = modelo.personas_en_tiempo(t)
            promedio = modelo.promedio_personas(t)
            alcance = modelo.porcentaje_penetracion(t)

            # 4) Calcular tiempos para hitos de alcance.
            hitos = []
            for pct in (25, 50, 75, 90):
                tiempo = modelo.tiempo_para_penetracion(pct)
                hitos.append((pct, tiempo))

            # 5) Armar un texto ordenado para mostrar resultados.
            salida = []
            salida.append("PARAMETROS")
            salida.append(f"E0: {round(e0)} personas")
            salida.append(f"M : {round(m)} personas")
            salida.append(f"k : {k:.6f}")
            salida.append(f"t : {round(t)} unidades")
            salida.append("")
            salida.append("RESULTADOS")
            salida.append(f"Personas que conocen la empresa en t: {round(e_final)}")
            salida.append(f"Porcentaje de alcance en t       : {round(alcance)}%")
            salida.append(f"Promedio en [0, t]               : {round(promedio)}")
            salida.append("")
            salida.append("TIEMPOS PARA ALCANCE")
            for pct, tiempo in hitos:
                if tiempo == float("inf"):
                    salida.append(f"{pct}%: no alcanzable")
                else:
                    salida.append(f"{pct}%: {round(tiempo)} unidades")

            self._escribir_resultados("\n".join(salida))

            # Guardamos el ultimo calculo para usarlo al graficar.
            self.modelo_actual = modelo
            self.t_actual = t

        except ValueError as error:
            messagebox.showerror("Datos invalidos", str(error))

    def graficar(self):
        """Abre el grafico del ultimo calculo realizado."""
        # Si no hay calculo previo, avisamos y no intentamos graficar.
        if self.modelo_actual is None or self.t_actual is None:
            messagebox.showwarning("Sin datos", "Primero debes calcular resultados")
            return

        try:
            self.mostrar_grafica()
        except Exception as error:
            messagebox.showerror("Error al graficar", str(error))

    def limpiar(self):
        """Limpia campos y resultados para comenzar un calculo nuevo."""
        # Reiniciamos entradas y estado interno.
        self.e0_var.set("")
        self.m_var.set("")
        self.k_var.set("")
        self.t_var.set("")
        self.modelo_actual = None
        self.t_actual = None
        self._escribir_resultados("Campos limpiados. Ingresa datos nuevos y presiona Calcular.")


def main():
    """Punto de entrada: inicia la aplicacion grafica."""
    root = tk.Tk()
    app = AplicacionDifusionGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
