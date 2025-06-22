import tkinter as tk
from tkinter import ttk, messagebox

class TuberiaCalculo:
    def __init__(self, datos_precargados=None):
        # Crear ventana principal
        self.root = tk.Toplevel()
        self.root.title("Sistema de Cálculos Eléctricos")
        self.root.geometry("1400x800")
        self.root.configure(bg="#f0f0f0")

        # Precargar datos si vienen desde calculosint.py
        if datos_precargados:
            calibre = datos_precargados.get("calibre", "")
            cantidad = str(datos_precargados.get("cantidad", ""))
            aislamiento = datos_precargados.get("aislamiento", "")
        else:
            calibre = ""
            cantidad = ""
            aislamiento = ""

        # ------------------ ENCABEZADO ------------------
        header = tk.Frame(self.root, bg="#1d3557", height=60)
        header.pack(fill=tk.X)

        tk.Label(header, text="SISTEMA DE CÁLCULOS ELÉCTRICOS",
                 bg="#1d3557", fg="white", font=("Century Gothic", 16, "bold")).pack(pady=5)

        tk.Label(header, text="NOM-001-SEDE-2012 • Hertz Ingeniería & Servicios Eléctricos S.A de C.V",
                 bg="#1d3557", fg="white", font=("Century Gothic", 10)).pack()

        # ------------------ CONTENIDO PRINCIPAL ------------------
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        left_frame = tk.LabelFrame(main_frame, text="Datos del Circuito Eléctrico", font=("Century Gothic", 10, "bold"),
                                   bg="white", labelanchor="n", width=400)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=10)

        center_frame = tk.LabelFrame(main_frame, text="Resultados del Cálculo", font=("Century Gothic", 10, "bold"),
                                     bg="white", labelanchor="n")
        center_frame.grid(row=0, column=1, sticky="nsew", padx=10)

        right_frame = tk.LabelFrame(main_frame, text="Historial y Referencias", font=("Century Gothic", 10, "bold"),
                                    bg="white", labelanchor="n", width=350)
        right_frame.grid(row=0, column=2, sticky="nsew", padx=10)

        # Configurar el grid para que se ajuste
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        # ------------------ VALORES DE TABLAS ------------------
        self.areas_tabla5 = {
            "14": 23.23,
            "12": 32.26,
            "10": 41.16,
            "8": 60.06,
            "6": 46.84,
            "4": 62.77,
            "3": 73.16,
            "2": 86.00,
            "1": 103.23,
            "1/0": 143.40,
            "2/0": 169.30,
            "3/0": 201.10,
            "4/0": 239.90,
            "250": 296.50,
            "300": 340.70,
            "350": 384.90,
            "400": 427.00,
            "500": 509.70,
            "600": 627.70,
            "700": 729.70,
            "800": 831.70,
            "1000": 1033.50
        }

        self.tuberias_emt = {
            "1/2": 196,
            "3/4": 343,
            "1": 556,
            "1 1/4": 968,
            "1 1/2": 1314,
            "2": 2165,
            "2 1/2": 3783,
            "3": 5701,
            "3 1/2": 7451,
            "4": 9521
        }

        self.referencias = [
            "• Tabla 5: Área aproximada del conductor (mm²)",
            "• Artículo 300.17: Límite del 40% de llenado",
            "• Tabla 4: Área interna de tuberías EMT (mm²)",
            "• NOM-001-SEDE-2012: Norma general de instalaciones",
            "• Artículo 250.122: Conductores de puesta a tierra"
        ]

        # ------------------ ENTRADAS MEJORADAS ------------------
        # Crear un frame scrollable para las entradas
        canvas = tk.Canvas(left_frame, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # --- SEPARADOR FASE ---
        separator1 = tk.Frame(scrollable_frame, height=2, bg="#1d3557")
        separator1.pack(fill=tk.X, pady=10)
        
        tk.Label(scrollable_frame, text="⚡ CONDUCTORES DE FASE", 
                bg="white", fg="#1d3557", font=("Century Gothic", 11, "bold")).pack(pady=5)

        ttk.Label(scrollable_frame, text="Calibre de Fase (AWG/kcmil):", background="white", 
                 font=("Century Gothic", 9)).pack(pady=2)
        self.combo_fase = ttk.Combobox(scrollable_frame, values=list(self.areas_tabla5.keys()), state="readonly", width=20)
        self.combo_fase.pack(pady=2)

        ttk.Label(scrollable_frame, text="Cantidad de Fases:", background="white", 
                 font=("Century Gothic", 9)).pack(pady=2)
        self.entry_fases = ttk.Entry(scrollable_frame, width=20)
        self.entry_fases.pack(pady=2)

        # --- SEPARADOR NEUTRO ---
        separator2 = tk.Frame(scrollable_frame, height=2, bg="#457b9d")
        separator2.pack(fill=tk.X, pady=10)
        
        tk.Label(scrollable_frame, text="⚪ CONDUCTOR NEUTRO (OPCIONAL)", 
                bg="white", fg="#457b9d", font=("Century Gothic", 11, "bold")).pack(pady=5)

        ttk.Label(scrollable_frame, text="¿Lleva neutro?", background="white", 
                 font=("Century Gothic", 9)).pack(pady=2)
        self.combo_neutro_si_no = ttk.Combobox(scrollable_frame, values=["No", "Sí"], state="readonly", width=20)
        self.combo_neutro_si_no.pack(pady=2)
        self.combo_neutro_si_no.set("No")

        ttk.Label(scrollable_frame, text="Calibre de Neutro (AWG/kcmil):", background="white", 
                 font=("Century Gothic", 9)).pack(pady=2)
        self.combo_neutro = ttk.Combobox(scrollable_frame, values=list(self.areas_tabla5.keys()), state="readonly", width=20)
        self.combo_neutro.pack(pady=2)

        # --- SEPARADOR TIERRA ---
        separator3 = tk.Frame(scrollable_frame, height=2, bg="#2a9d8f")
        separator3.pack(fill=tk.X, pady=10)
        
        tk.Label(scrollable_frame, text="🌍 CONDUCTOR DE TIERRA (OBLIGATORIO)", 
                bg="white", fg="#2a9d8f", font=("Century Gothic", 11, "bold")).pack(pady=5)

        ttk.Label(scrollable_frame, text="Calibre de Tierra Física (AWG/kcmil):", background="white", 
                 font=("Century Gothic", 9)).pack(pady=2)
        self.combo_tierra = ttk.Combobox(scrollable_frame, values=list(self.areas_tabla5.keys()), state="readonly", width=20)
        self.combo_tierra.pack(pady=2)

        # --- SEPARADOR ADICIONAL ---
        separator4 = tk.Frame(scrollable_frame, height=2, bg="#e76f51")
        separator4.pack(fill=tk.X, pady=10)
        
        tk.Label(scrollable_frame, text="🔧 INFORMACIÓN ADICIONAL", 
                bg="white", fg="#e76f51", font=("Century Gothic", 11, "bold")).pack(pady=5)

        ttk.Label(scrollable_frame, text="Tipo de aislamiento:", background="white", 
                 font=("Century Gothic", 9)).pack(pady=2)
        self.combo_aislamiento = ttk.Combobox(scrollable_frame, values=["THHN", "THWN", "XHHW", "USE", "RHW", "THWN-2"], state="readonly", width=20)
        self.combo_aislamiento.pack(pady=2)

        # Configurar el canvas y scrollbar
        canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y")

        # Precargar valores si existen (adaptado para el nuevo sistema)
        if calibre:
            self.combo_fase.set(calibre)
        if cantidad:
            self.entry_fases.insert(0, cantidad)
        if aislamiento:
            self.combo_aislamiento.set(aislamiento)

        # ------------------ RESULTADO ------------------
        self.resultado = tk.Text(center_frame, height=30, width=80, wrap=tk.WORD, 
                                font=("Consolas", 10), bg="#f8f9fa")
        scrollbar_resultado = ttk.Scrollbar(center_frame, orient="vertical", command=self.resultado.yview)
        self.resultado.configure(yscrollcommand=scrollbar_resultado.set)
        
        self.resultado.pack(side="left", fill="both", expand=True, pady=10, padx=5)
        scrollbar_resultado.pack(side="right", fill="y", pady=10)

        # ------------------ REFERENCIAS ------------------
        tk.Label(right_frame, text="Referencias Normativas Aplicadas:", bg="white", anchor="w",
                 font=("Century Gothic", 10, "bold")).pack(anchor="w", padx=5, pady=5)

        for ref in self.referencias:
            tk.Label(right_frame, text=ref, bg="white", font=("Century Gothic", 9), 
                    anchor="w", justify="left", wraplength=300).pack(anchor="w", padx=10, pady=2)

        # Agregar información adicional
        tk.Label(right_frame, text="\n💡 Información Técnica:", bg="white", anchor="w",
                 font=("Century Gothic", 10, "bold")).pack(anchor="w", padx=5, pady=5)
        
        info_adicional = [
            "• Factor de llenado: 40% (más de 2 conductores)",
            "• Temperatura ambiente: 30°C",
            "• Material: Cobre (Cu)",
            "• Instalación: Tubería EMT"
        ]
        
        for info in info_adicional:
            tk.Label(right_frame, text=info, bg="white", font=("Century Gothic", 9), 
                    anchor="w", justify="left", wraplength=300).pack(anchor="w", padx=10, pady=1)

        # ------------------ CONTROLES INFERIORES ------------------
        bottom_frame = tk.Frame(self.root, bg="#f0f0f0")
        bottom_frame.pack(pady=10)

        tk.Button(bottom_frame, text="🧮 CALCULAR", bg="#d62828", fg="white",
                  font=("Century Gothic", 12, "bold"), width=15, height=2, 
                  command=self.calcular).grid(row=0, column=0, padx=10)

        tk.Button(bottom_frame, text="🧹 LIMPIAR", bg="#6c757d", fg="white",
                  font=("Century Gothic", 12, "bold"), width=15, height=2, 
                  command=self.limpiar).grid(row=0, column=1, padx=10)

        tk.Button(bottom_frame, text="📄 EXPORTAR PDF", bg="#6a4c93", fg="white",
                  font=("Century Gothic", 12, "bold"), width=15, height=2).grid(row=0, column=2, padx=10)

        tk.Button(bottom_frame, text="❌ CERRAR", bg="#e76f51", fg="white",
                  font=("Century Gothic", 12, "bold"), width=15, height=2, 
                  command=self.root.destroy).grid(row=0, column=3, padx=10)

        # ------------------ SERVICIOS ADICIONALES ------------------
        servicios = tk.LabelFrame(self.root, text="Servicios Adicionales", font=("Century Gothic", 10, "bold"),
                                  bg="white", labelanchor="n")
        servicios.pack(fill=tk.X, padx=10, pady=5)

        tk.Button(servicios, text="📋 Memoria Técnica PDF", bg="#adb5bd", fg="black",
                  font=("Century Gothic", 10, "bold")).pack(side=tk.LEFT, padx=5, pady=5)
        
        tk.Button(servicios, text="📊 Reporte Detallado", bg="#adb5bd", fg="black",
                  font=("Century Gothic", 10, "bold")).pack(side=tk.LEFT, padx=5, pady=5)

    def calcular(self):
        try:
            # Validar datos de entrada
            if not self.combo_fase.get():
                messagebox.showerror("Error", "Debe seleccionar el calibre de fase")
                return
            
            if not self.entry_fases.get():
                messagebox.showerror("Error", "Debe ingresar la cantidad de fases")
                return
                
            if not self.combo_tierra.get():
                messagebox.showerror("Error", "Debe seleccionar el calibre de tierra física")
                return

            # Obtener datos de fase
            calibre_fase = self.combo_fase.get()
            num_fases = int(self.entry_fases.get())
            area_fase = self.areas_tabla5[calibre_fase]

            # Obtener datos de neutro
            lleva_neutro = self.combo_neutro_si_no.get() == "Sí"
            area_neutro = 0
            calibre_neutro = ""
            
            if lleva_neutro:
                if not self.combo_neutro.get():
                    messagebox.showerror("Error", "Debe seleccionar el calibre de neutro")
                    return
                calibre_neutro = self.combo_neutro.get()
                area_neutro = self.areas_tabla5[calibre_neutro]

            # Obtener datos de tierra
            calibre_tierra = self.combo_tierra.get()
            area_tierra = self.areas_tabla5[calibre_tierra]

            # Calcular área total
            area_total = (num_fases * area_fase) + area_neutro + area_tierra
            area_100 = (area_total * 100) / 40

            # Buscar tubería recomendada
            tuberia_recomendada = "No encontrada"
            area_disponible = None
            for tuberia, area in self.tuberias_emt.items():
                if area >= area_100:
                    tuberia_recomendada = tuberia
                    area_disponible = area
                    break

            # Mostrar resultados detallados
            self.resultado.delete("1.0", tk.END)
            self.resultado.insert(tk.END, "=" * 60 + "\n")
            self.resultado.insert(tk.END, "🔌 RESULTADO DEL CÁLCULO DE TUBERÍA EMT\n")
            self.resultado.insert(tk.END, "=" * 60 + "\n\n")

            # Desglose por tipo de conductor
            self.resultado.insert(tk.END, "📊 DESGLOSE DE CONDUCTORES:\n")
            self.resultado.insert(tk.END, "-" * 40 + "\n")
            
            self.resultado.insert(tk.END, f"⚡ FASE ({num_fases} × {calibre_fase} AWG):\n")
            self.resultado.insert(tk.END, f"   • Área individual: {area_fase:.2f} mm²\n")
            self.resultado.insert(tk.END, f"   • Área total: {area_fase:.2f} × {num_fases} = {area_fase * num_fases:.2f} mm²\n\n")

            if lleva_neutro:
                self.resultado.insert(tk.END, f"⚪ NEUTRO ({calibre_neutro} AWG):\n")
                self.resultado.insert(tk.END, f"   • Área: {area_neutro:.2f} mm²\n\n")
            else:
                self.resultado.insert(tk.END, "⚪ NEUTRO: No aplica\n\n")

            self.resultado.insert(tk.END, f"🌍 TIERRA FÍSICA ({calibre_tierra} AWG):\n")
            self.resultado.insert(tk.END, f"   • Área: {area_tierra:.2f} mm²\n\n")

            # Resumen del cálculo
            self.resultado.insert(tk.END, "📦 RESUMEN DEL CÁLCULO:\n")
            self.resultado.insert(tk.END, "-" * 40 + "\n")
            self.resultado.insert(tk.END, f"• Área total ocupada (40%): {area_total:.2f} mm²\n")
            self.resultado.insert(tk.END, f"• Área interna requerida (100%): {area_100:.2f} mm²\n\n")

            # Resultado final
            if area_disponible:
                self.resultado.insert(tk.END, "✅ TUBERÍA RECOMENDADA:\n")
                self.resultado.insert(tk.END, "-" * 40 + "\n")
                self.resultado.insert(tk.END, f"🔧 EMT {tuberia_recomendada}\" ({area_disponible:.0f} mm² disponibles)\n")
                porcentaje_uso = (area_total / area_disponible) * 100
                self.resultado.insert(tk.END, f"📊 Porcentaje de uso: {porcentaje_uso:.1f}%\n\n")
            else:
                self.resultado.insert(tk.END, "❌ RESULTADO:\n")
                self.resultado.insert(tk.END, "-" * 40 + "\n")
                self.resultado.insert(tk.END, "No se encontró una tubería EMT estándar que cumpla\n")
                self.resultado.insert(tk.END, "con el área requerida según la Tabla 4.\n\n")

            # Explicación técnica
            self.resultado.insert(tk.END, "🧠 METODOLOGÍA DE CÁLCULO:\n")
            self.resultado.insert(tk.END, "=" * 40 + "\n")
            self.resultado.insert(tk.END, "1. Se consultó la Tabla 5 de la NOM-001-SEDE-2012 para\n")
            self.resultado.insert(tk.END, "   obtener el área de cada tipo de conductor.\n\n")
            
            self.resultado.insert(tk.END, "2. Se aplicó el Artículo 300.17 que establece que cuando\n")
            self.resultado.insert(tk.END, "   hay más de 2 conductores, solo se puede ocupar el\n")
            self.resultado.insert(tk.END, "   40% del área interna de la tubería.\n\n")
            
            self.resultado.insert(tk.END, "3. Fórmula aplicada:\n")
            self.resultado.insert(tk.END, f"   Área requerida = ({area_total:.2f} × 100) ÷ 40 = {area_100:.2f} mm²\n\n")
            
            self.resultado.insert(tk.END, "4. Se seleccionó la tubería EMT más pequeña de la Tabla 4\n")
            self.resultado.insert(tk.END, "   que cumpla con el área mínima requerida.\n\n")

            # Información adicional
            aislamiento = self.combo_aislamiento.get()
            if aislamiento:
                self.resultado.insert(tk.END, f"📋 ESPECIFICACIONES ADICIONALES:\n")
                self.resultado.insert(tk.END, "-" * 40 + "\n")
                self.resultado.insert(tk.END, f"• Tipo de aislamiento: {aislamiento}\n")
                self.resultado.insert(tk.END, f"• Material del conductor: Cobre (Cu)\n")
                self.resultado.insert(tk.END, f"• Temperatura ambiente: 30°C\n")
                self.resultado.insert(tk.END, f"• Norma aplicada: NOM-001-SEDE-2012\n\n")

            self.resultado.insert(tk.END, "=" * 60 + "\n")
            self.resultado.insert(tk.END, "✨ Cálculo realizado por Hertz Ingeniería & Servicios Eléctricos\n")
            self.resultado.insert(tk.END, "=" * 60 + "\n")

        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos")
        except KeyError:
            messagebox.showerror("Error", "Calibre no encontrado en las tablas")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")

    def limpiar(self):
        """Limpiar todos los campos de entrada y el resultado"""
        self.combo_fase.set("")
        self.entry_fases.delete(0, tk.END)
        self.combo_neutro_si_no.set("No")
        self.combo_neutro.set("")
        self.combo_tierra.set("")
        self.combo_aislamiento.set("")
        self.resultado.delete("1.0", tk.END)

    def mostrar(self):
        """Mostrar la ventana principal"""
        self.root.mainloop()

# Función para inicializar desde calculosint.py
def iniciar_calculo_tuberia(datos_precargados=None):
    """
    Función para inicializar la calculadora de tuberías
    
    Args:
        datos_precargados (dict, optional): Diccionario con datos precargados
                                          {'calibre': str, 'cantidad': int, 'aislamiento': str}
    """
    app = TuberiaCalculo(datos_precargados)
    app.mostrar()

# Ejecutar directamente si es el archivo principal
if __name__ == "__main__":
    # Ejemplo de datos precargados (simula venir de calculosint.py)
    datos_ejemplo = {
        "calibre": "12",
        "cantidad": 3,
        "aislamiento": "THHN"
    }
    
    # Iniciar con datos precargados (descomentar para probar)
    # iniciar_calculo_tuberia(datos_ejemplo)
    
    # Iniciar vacío
    iniciar_calculo_tuberia()