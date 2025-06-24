import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import math
from datetime import datetime

class CharolaCalculatorPro:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Cálculos Eléctricos - Hertz Ingeniería")
        self.root.geometry("1450x700")
        self.root.configure(bg="#f8f9fa")
        self.root.resizable(True, True)
        
        # Diccionario de diámetros de conductores (mm)
        self.tabla_diametros = {
            "6": 7.722,
            "4": 8.941,
            "3": 9.652,
            "2": 10.46,
            "1": 12.50,
            "1/0": 13.51,
            "2/0": 14.68,
            "3/0": 16.00,
            "4/0": 17.48,
            "250": 19.43,
            "300": 20.83,
            "350": 22.12,
            "400": 23.32,
            "500": 25.48,
            "600": 28.27
        }
        
        # Anchos comerciales de charola (pulgadas)
        self.anchos_charola_pulgadas = [4, 6, 9, 12, 14, 16, 18, 20, 24, 30, 32, 36, 42, 48]
        
        # Historial de cálculos
        self.historial = []
        
        self.setup_ui()
    
    def setup_ui(self):
        # ============ ENCABEZADO (HEADER) ============
        header = tk.Frame(self.root, bg="#1d3557", height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="SISTEMA DE CÁLCULOS ELÉCTRICOS", 
                bg="#1d3557", fg="white", 
                font=("Century Gothic", 16, "bold")).pack(pady=(10, 0))
        
        tk.Label(header, text="NOM-001-SEDE-2012 • Hertz Ingeniería & Servicios Eléctricos S.A de C.V", 
                bg="#1d3557", fg="#a8dadc", 
                font=("Century Gothic", 10)).pack(pady=(5, 0))
        
        # ============ CONTENEDOR PRINCIPAL ============
        main_container = tk.Frame(self.root, bg="#f8f9fa")
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # ============ PANEL IZQUIERDO: DATOS DE ENTRADA ============
        self.panel_izquierdo = tk.LabelFrame(main_container, 
                                           text="📋 Datos del Circuito Eléctrico", 
                                           font=("Century Gothic", 12, "bold"), 
                                           bg="white", fg="#1d3557",
                                           padx=15, pady=15, 
                                           bd=2, relief="groove")
        self.panel_izquierdo.place(x=0, y=0, width=420, height=500)
        
        # Tipo de charola
        tk.Label(self.panel_izquierdo, text="Tipo de Charola:", 
                font=("Century Gothic", 10, "bold"), bg="white").pack(anchor="w", pady=(0, 5))
        
        self.tipo_charola = tk.StringVar(value="escalera")
        tipo_frame = tk.Frame(self.panel_izquierdo, bg="white")
        tipo_frame.pack(fill="x", pady=(0, 15))
        
        tipo_combo = ttk.Combobox(tipo_frame, textvariable=self.tipo_charola, 
                                 values=["escalera", "fondo_sólido"], 
                                 state="readonly", font=("Century Gothic", 10))
        tipo_combo.pack(fill="x")
        
        # Calibre AWG
        tk.Label(self.panel_izquierdo, text="Calibre AWG:", 
                font=("Century Gothic", 10, "bold"), bg="white").pack(anchor="w", pady=(0, 5))
        
        self.calibre_var = tk.StringVar()
        calibre_frame = tk.Frame(self.panel_izquierdo, bg="white")
        calibre_frame.pack(fill="x", pady=(0, 15))
        
        calibre_combo = ttk.Combobox(calibre_frame, textvariable=self.calibre_var, 
                                    values=list(self.tabla_diametros.keys()), 
                                    state="readonly", font=("Century Gothic", 10))
        calibre_combo.pack(fill="x")
        
        # Separador
        tk.Frame(self.panel_izquierdo, height=2, bg="#e9ecef").pack(fill="x", pady=10)
        
        # ============ CONFIGURACIÓN DE CONDUCTORES ============
        tk.Label(self.panel_izquierdo, text="⚡ Configuración de Conductores", 
                font=("Century Gothic", 11, "bold"), bg="white", fg="#e63946").pack(anchor="w", pady=(0, 10))
        
        # Fases
        fases_frame = tk.Frame(self.panel_izquierdo, bg="white")
        fases_frame.pack(fill="x", pady=5)
        
        self.incluye_fases = tk.BooleanVar(value=True)
        fases_check = tk.Checkbutton(fases_frame, text="Fases", variable=self.incluye_fases,
                                   font=("Century Gothic", 10), bg="white", fg="#1d3557",
                                   command=self.toggle_fases)
        fases_check.pack(side="left")
        
        self.fases_var = tk.IntVar(value=3)
        self.fases_spinbox = tk.Spinbox(fases_frame, from_=1, to=50, 
                                       textvariable=self.fases_var, 
                                       width=8, font=("Century Gothic", 10))
        self.fases_spinbox.pack(side="right")
        
        # Neutros
        neutros_frame = tk.Frame(self.panel_izquierdo, bg="white")
        neutros_frame.pack(fill="x", pady=5)
        
        self.incluye_neutros = tk.BooleanVar(value=True)
        neutros_check = tk.Checkbutton(neutros_frame, text="Neutros", variable=self.incluye_neutros,
                                     font=("Century Gothic", 10), bg="white", fg="#1d3557",
                                     command=self.toggle_neutros)
        neutros_check.pack(side="left")
        
        self.neutros_var = tk.IntVar(value=1)
        self.neutros_spinbox = tk.Spinbox(neutros_frame, from_=1, to=20, 
                                         textvariable=self.neutros_var, 
                                         width=8, font=("Century Gothic", 10))
        self.neutros_spinbox.pack(side="right")
        
        # Tierra
        tierra_frame = tk.Frame(self.panel_izquierdo, bg="white")
        tierra_frame.pack(fill="x", pady=5)
        
        self.incluye_tierra = tk.BooleanVar(value=True)
        tierra_check = tk.Checkbutton(tierra_frame, text="Tierra", variable=self.incluye_tierra,
                                    font=("Century Gothic", 10), bg="white", fg="#1d3557",
                                    command=self.toggle_tierra)
        tierra_check.pack(side="left")
        
        self.tierra_var = tk.IntVar(value=1)
        self.tierra_spinbox = tk.Spinbox(tierra_frame, from_=1, to=10, 
                                        textvariable=self.tierra_var, 
                                        width=8, font=("Century Gothic", 10))
        self.tierra_spinbox.pack(side="right")
        
        # Información adicional
        info_frame = tk.Frame(self.panel_izquierdo, bg="#e7f3ff", relief="groove", bd=1)
        info_frame.pack(fill="x", pady=(20, 0))
        
        tk.Label(info_frame, text="ℹ️ Información", 
                font=("Century Gothic", 9, "bold"), bg="#e7f3ff", fg="#0066cc").pack(pady=5)
        
        tk.Label(info_frame, text="• Método: Suma de lados dinámico\n• Espaciamiento: 2.15 x diámetro\n• Norma: NOM-001-SEDE-2012", 
                font=("Century Gothic", 8), bg="#e7f3ff", fg="#333333", justify="left").pack(pady=(0, 5))
        
        # ============ PANEL CENTRAL: RESULTADOS ============
        self.panel_resultado = tk.LabelFrame(main_container, 
                                           text="📊 Resultados del Cálculo", 
                                           font=("Century Gothic", 12, "bold"), 
                                           bg="white", fg="#1d3557",
                                           padx=15, pady=15, 
                                           bd=2, relief="groove")
        self.panel_resultado.place(x=430, y=0, width=700, height=500)
        
        # Text widget para resultados con scrollbar
        text_frame = tk.Frame(self.panel_resultado, bg="white")
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.text_resultado = tk.Text(text_frame, 
                                     font=("Consolas", 9), 
                                     wrap="word", 
                                     bg="#f8f9fa", 
                                     fg="#212529",
                                     selectbackground="#457b9d",
                                     selectforeground="white")
        
        scrollbar_resultado = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.text_resultado.yview)
        self.text_resultado.configure(yscrollcommand=scrollbar_resultado.set)
        
        self.text_resultado.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_resultado.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configurar tags para colores
        self.text_resultado.tag_configure("titulo", foreground="#1d3557", font=("Consolas", 11, "bold"))
        self.text_resultado.tag_configure("success", foreground="#28a745", font=("Consolas", 10, "bold"))
        self.text_resultado.tag_configure("warning", foreground="#ffc107", font=("Consolas", 10, "bold"))
        self.text_resultado.tag_configure("error", foreground="#dc3545", font=("Consolas", 10, "bold"))
        self.text_resultado.tag_configure("info", foreground="#17a2b8", font=("Consolas", 10, "bold"))
        
        # ============ PANEL DERECHO: HISTORIAL Y REFERENCIAS ============
        self.panel_derecho = tk.LabelFrame(main_container, 
                                         text="📚 Historial y Referencias", 
                                         font=("Century Gothic", 12, "bold"), 
                                         bg="white", fg="#1d3557",
                                         padx=15, pady=15, 
                                         bd=2, relief="groove")
        self.panel_derecho.place(x=1140, y=0, width=300, height=500)
        
        # Notebook para pestañas
        notebook = ttk.Notebook(self.panel_derecho)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña Referencias
        ref_frame = ttk.Frame(notebook)
        notebook.add(ref_frame, text="Referencias")
        
        ref_text = tk.Text(ref_frame, font=("Century Gothic", 8), wrap="word", height=10)
        ref_text.pack(fill=tk.BOTH, expand=True)
        
        referencias = """📋 TABLAS NOM-001-SEDE-2012:

• Tabla 4: Área interna de tuberías EMT
• Tabla 5: Área del conductor (mm²)
• Tabla 310-15(B)(16): Capacidad de corriente
• Tabla 310-15(B)(17): Capacidad en charolas

🔧 ESPECIFICACIONES TÉCNICAS:

• Factor de espaciamiento: 2.15
• Charolas tipo escalera: 2 fases visibles
• Charolas fondo sólido: Fases agrupadas
• Separación mínima: Diámetro × 2.15

⚡ ANCHOS COMERCIALES:
4", 6", 9", 12", 14", 16", 18", 20", 24", 30", 32", 36", 42", 48"

🏢 HERTZ INGENIERÍA & SERVICIOS ELÉCTRICOS S.A DE C.V
"""
        ref_text.insert(tk.END, referencias)
        ref_text.config(state=tk.DISABLED)
        
        # Pestaña Historial
        hist_frame = ttk.Frame(notebook)
        notebook.add(hist_frame, text="Historial")
        
        self.historial_text = tk.Text(hist_frame, font=("Consolas", 8), wrap="word")
        hist_scrollbar = ttk.Scrollbar(hist_frame, orient=tk.VERTICAL, command=self.historial_text.yview)
        self.historial_text.configure(yscrollcommand=hist_scrollbar.set)
        
        self.historial_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        hist_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # ============ BOTONES INFERIORES ============
        botones_frame = tk.Frame(self.root, bg="#f8f9fa", height=60)
        botones_frame.pack(fill="x", side="bottom")
        botones_frame.pack_propagate(False)
        
        # Centrar botones
        botones_container = tk.Frame(botones_frame, bg="#f8f9fa")
        botones_container.pack(expand=True)
        
        # Botón Calcular
        self.btn_calcular = tk.Button(botones_container, text="📐 CALCULAR", 
                                     font=("Century Gothic", 11, "bold"), 
                                     bg="#e63946", fg="white", 
                                     width=15, height=2,
                                     relief="raised", bd=2,
                                     command=self.calcular)
        self.btn_calcular.pack(side="left", padx=10)
        
        # Botón Limpiar
        self.btn_limpiar = tk.Button(botones_container, text="🧹 LIMPIAR", 
                                    font=("Century Gothic", 11, "bold"), 
                                    bg="#6c757d", fg="white", 
                                    width=15, height=2,
                                    relief="raised", bd=2,
                                    command=self.limpiar)
        self.btn_limpiar.pack(side="left", padx=10)
        
        # Botón Exportar PDF
        self.btn_exportar = tk.Button(botones_container, text="📄 EXPORTAR PDF", 
                                     font=("Century Gothic", 11, "bold"), 
                                     bg="#6f42c1", fg="white", 
                                     width=16, height=2,
                                     relief="raised", bd=2,
                                     command=self.exportar_pdf)
        self.btn_exportar.pack(side="left", padx=10)
        
        # Botón Cerrar
        self.btn_cerrar = tk.Button(botones_container, text="❌ CERRAR", 
                                   font=("Century Gothic", 11, "bold"), 
                                   bg="#d62828", fg="white", 
                                   width=15, height=2,
                                   relief="raised", bd=2,
                                   command=self.cerrar_aplicacion)
        self.btn_cerrar.pack(side="left", padx=10)
        
        # Mensaje de bienvenida
        self.mostrar_bienvenida()
    
    def toggle_fases(self):
        if self.incluye_fases.get():
            self.fases_spinbox.config(state='normal')
        else:
            self.fases_spinbox.config(state='disabled')
    
    def toggle_neutros(self):
        if self.incluye_neutros.get():
            self.neutros_spinbox.config(state='normal')
        else:
            self.neutros_spinbox.config(state='disabled')
    
    def toggle_tierra(self):
        if self.incluye_tierra.get():
            self.tierra_spinbox.config(state='normal')
        else:
            self.tierra_spinbox.config(state='disabled')
    
    def validar_entrada(self):
        if not self.calibre_var.get():
            messagebox.showerror("Error de Validación", "⚠️ Selecciona un calibre AWG")
            return False
        
        if not (self.incluye_fases.get() or self.incluye_neutros.get() or self.incluye_tierra.get()):
            messagebox.showerror("Error de Validación", "⚠️ Selecciona al menos un tipo de conductor")
            return False
        
        try:
            if self.incluye_fases.get() and self.fases_var.get() <= 0:
                raise ValueError("El número de fases debe ser mayor a 0")
            if self.incluye_neutros.get() and self.neutros_var.get() <= 0:
                raise ValueError("El número de neutros debe ser mayor a 0")
            if self.incluye_tierra.get() and self.tierra_var.get() <= 0:
                raise ValueError("El número de tierras debe ser mayor a 0")
        except Exception as e:
            messagebox.showerror("Error de Validación", f"⚠️ {str(e)}")
            return False
        
        return True
    
    def realizar_calculo(self, calibre, configuracion):
        if calibre not in self.tabla_diametros:
            raise ValueError("El calibre no tiene diámetro definido")
        
        d = self.tabla_diametros[calibre]
        espaciamiento = 2.15
        tipo_charola = self.tipo_charola.get()
        
        fases = configuracion['fases'] if configuracion['incluye_fases'] else 0
        neutros = configuracion['neutros'] if configuracion['incluye_neutros'] else 0
        tierra = configuracion['tierra'] if configuracion['incluye_tierra'] else 0
        
        # Cálculos según tipo de charola
        if tipo_charola == "fondo_sólido":
            grupos_fase = fases // 3 if fases > 0 else 0
            fases_restantes = fases % 3
            
            largo_grupos_completos = d * 3 * grupos_fase
            largo_fases_restantes = d * fases_restantes
            
            separaciones_entre_grupos = grupos_fase - 1 if grupos_fase > 1 else 0
            
            if fases_restantes > 0 and grupos_fase > 0:
                separaciones_entre_grupos += 1
            
            largo_neutros = d * neutros
            if neutros > 0 and (grupos_fase > 0 or fases_restantes > 0):
                separaciones_entre_grupos += 1
            
            largo_ocupado = largo_grupos_completos + largo_fases_restantes + largo_neutros
            espacios_adicionales = espaciamiento * d * separaciones_entre_grupos
            lado_horizontal = largo_ocupado + espacios_adicionales
            
            hilos_visibles = fases + neutros
            espacios = separaciones_entre_grupos
            
        else:  # escalera
            grupos_fase = fases / 3
            hilos_visibles = 2 * grupos_fase
            espacios = grupos_fase
            
            largo_ocupado = d * hilos_visibles
            espacios_adicionales = espaciamiento * d * espacios
            lado_horizontal = largo_ocupado + espacios_adicionales
        
        suma_total_mm = lado_horizontal
        suma_total_pulg = suma_total_mm * 0.0393701
        
        # Buscar charolas comerciales
        charolas_disponibles = [ancho for ancho in self.anchos_charola_pulgadas if ancho >= suma_total_pulg]
        
        opciones_charola = []
        for i, ancho in enumerate(charolas_disponibles[:3]):
            diferencia_pulg = ancho - suma_total_pulg
            diferencia_mm = diferencia_pulg * 25.4
            porcentaje_uso = (suma_total_pulg / ancho) * 100
            
            opciones_charola.append({
                'ancho': ancho,
                'diferencia_pulg': diferencia_pulg,
                'diferencia_mm': diferencia_mm,
                'porcentaje_uso': porcentaje_uso,
                'recomendada': i == 0
            })
        
        return {
            'tipo_charola': tipo_charola,
            'diametro': d,
            'fases': fases,
            'neutros': neutros,
            'tierra': tierra,
            'lado_horizontal': lado_horizontal,
            'suma_total_mm': suma_total_mm,
            'suma_total_pulg': suma_total_pulg,
            'opciones_charola': opciones_charola,
            'largo_ocupado': largo_ocupado,
            'espacios_adicionales': espacios_adicionales,
            'separaciones': espacios if tipo_charola == "escalera" else separaciones_entre_grupos
        }
    
    def calcular(self):
        if not self.validar_entrada():
            return
        
        calibre = self.calibre_var.get()
        self.calibre_resultante = calibre

        
        configuracion = {
            'incluye_fases': self.incluye_fases.get(),
            'incluye_neutros': self.incluye_neutros.get(),
            'incluye_tierra': self.incluye_tierra.get(),
            'fases': self.fases_var.get() if self.incluye_fases.get() else 0,
            'neutros': self.neutros_var.get() if self.incluye_neutros.get() else 0,
            'tierra': self.tierra_var.get() if self.incluye_tierra.get() else 0
        }
        
        try:
            resultado = self.realizar_calculo(calibre, configuracion)
            
            self.mostrar_resultados(calibre, configuracion, resultado)
            self.agregar_historial(calibre, configuracion, resultado)
        except Exception as e:
            messagebox.showerror("Error en el Cálculo", f"❌ {str(e)}")
    
    def mostrar_resultados(self, calibre, configuracion, resultado):
        self.text_resultado.delete(1.0, tk.END)
        
        # Encabezado del resultado
        texto = "═" * 80 + "\n"
        texto += "        🔌 RESULTADO DEL CÁLCULO DE CHAROLA ELÉCTRICA\n"
        texto += "                   MÉTODO SUMA DE LADOS DINÁMICO\n"
        texto += "═" * 80 + "\n\n"
        
        # Configuración
        texto += "📋 CONFIGURACIÓN DEL CIRCUITO:\n"
        texto += f"   • Tipo de charola: {resultado['tipo_charola'].upper()}\n"
        texto += f"   • Calibre del conductor: {calibre} AWG\n"
        texto += f"   • Diámetro del conductor: {resultado['diametro']:.2f} mm\n"
        if configuracion['incluye_fases']:
            texto += f"   • Fases: {configuracion['fases']} conductor(es)\n"
        if configuracion['incluye_neutros']:
            texto += f"   • Neutros: {configuracion['neutros']} conductor(es)\n"
        if configuracion['incluye_tierra']:
            texto += f"   • Tierra: {configuracion['tierra']} conductor(es)\n"
        texto += "\n"
        
        # Cálculo detallado
        texto += "🔧 CÁLCULO DETALLADO:\n"
        texto += f"   • Factor de espaciamiento: 2.15\n"
        texto += f"   • Largo ocupado por conductores: {resultado['largo_ocupado']:.2f} mm\n"
        texto += f"   • Espacios adicionales: {resultado['espacios_adicionales']:.2f} mm\n"
        texto += f"   • Separaciones requeridas: {resultado['separaciones']:.0f}\n"
        texto += f"   • Ancho total requerido: {resultado['suma_total_mm']:.2f} mm\n"
        texto += f"   • Ancho total requerido: {resultado['suma_total_pulg']:.2f} pulgadas\n\n"
        
        # Opciones de charola
        texto += "🎯 OPCIONES DE CHAROLA COMERCIAL:\n"
        if resultado['opciones_charola']:
            for i, opcion in enumerate(resultado['opciones_charola']):
                if opcion['recomendada']:
                    texto += f"   ✅ RECOMENDADA: Charola de {opcion['ancho']}\" pulgadas\n"
                    texto += f"      • Espacio libre: {opcion['diferencia_pulg']:.2f}\" ({opcion['diferencia_mm']:.2f} mm)\n"
                    texto += f"      • Porcentaje de uso: {opcion['porcentaje_uso']:.1f}%\n\n"
                else:
                    texto += f"   📋 OPCIÓN {i}: Charola de {opcion['ancho']}\" pulgadas\n"
                    texto += f"      • Espacio libre: {opcion['diferencia_pulg']:.2f}\" ({opcion['diferencia_mm']:.2f} mm)\n"
                    texto += f"      • Porcentaje de uso: {opcion['porcentaje_uso']:.1f}%\n\n"
        else:
            texto += "   ❌ NO SE ENCONTRÓ CHAROLA COMERCIAL ADECUADA\n"
            texto += f"   • Se requiere ancho mínimo de: {resultado['suma_total_pulg']:.2f}\"\n\n"
        
        # Pie de página
        texto += "═" * 80 + "\n"
        texto += f"✓ Cálculo realizado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
        texto += "✓ Norma aplicada: NOM-001-SEDE-2012\n"
        texto += "✓ Hertz Ingeniería & Servicios Eléctricos S.A de C.V\n"
        
        self.text_resultado.insert(tk.END, texto)
        
        # Aplicar colores
        self.aplicar_colores_resultado()
    
    def aplicar_colores_resultado(self):
        contenido = self.text_resultado.get(1.0, tk.END)
        
        # Colorear títulos
        self.colorear_texto("RESULTADO DEL CÁLCULO", "titulo")
        self.colorear_texto("CONFIGURACIÓN DEL CIRCUITO", "info")
        self.colorear_texto("CÁLCULO DETALLADO", "info")
        self.colorear_texto("OPCIONES DE CHAROLA", "info")
        
        # Colorear resultados
        self.colorear_texto("RECOMENDADA", "success")
        self.colorear_texto("NO SE ENCONTRÓ", "error")
        self.colorear_texto("✅", "success")
        self.colorear_texto("❌", "error")
    
    def colorear_texto(self, texto_buscar, tag):
        contenido = self.text_resultado.get(1.0, tk.END)
        inicio = 0
        while True:
            inicio = contenido.find(texto_buscar, inicio)
            if inicio == -1:
                break
            fin = inicio + len(texto_buscar)
            linea = contenido[:inicio].count('\n') + 1
            columna = inicio - contenido.rfind('\n', 0, inicio) - 1
            if columna < 0:
                columna = inicio
            
            inicio_pos = f"{linea}.{columna}"
            fin_pos = f"{linea}.{columna + len(texto_buscar)}"
            
            self.text_resultado.tag_add(tag, inicio_pos, fin_pos)
            inicio = fin
    
    def agregar_historial(self, calibre, configuracion, resultado):
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        entrada_historial = f"[{timestamp}] {calibre} AWG - "
        if configuracion['incluye_fases']:
            entrada_historial += f"F:{configuracion['fases']} "
        if configuracion['incluye_neutros']:
            entrada_historial += f"N:{configuracion['neutros']} "
        if configuracion['incluye_tierra']:
            entrada_historial += f"T:{configuracion['tierra']} "
        
        if resultado['opciones_charola']:
            entrada_historial += f"→ {resultado['opciones_charola'][0]['ancho']}\"\n"
        else:
            entrada_historial += "→ Sin charola\n"
        
        self.historial.append(entrada_historial)
        
        # Actualizar historial en la interfaz
        self.historial_text.insert(tk.END, entrada_historial)
        self.historial_text.see(tk.END)
    
    def limpiar(self):
        # Limpiar campos de entrada
        self.calibre_var.set("")
        self.tipo_charola.set("escalera")
        
        # Resetear checkboxes y valores
        self.incluye_fases.set(True)
        self.incluye_neutros.set(True)
        self.incluye_tierra.set(True)
        
        self.fases_var.set(3)
        self.neutros_var.set(1)
        self.tierra_var.set(1)
        
        # Habilitar todos los spinboxes
        self.fases_spinbox.config(state='normal')
        self.neutros_spinbox.config(state='normal')
        self.tierra_spinbox.config(state='normal')
        
        # Limpiar resultados
        self.text_resultado.delete(1.0, tk.END)
        self.mostrar_bienvenida()
        
        messagebox.showinfo("Limpieza Completada", "✅ Todos los campos han sido reiniciados")
    
    def exportar_pdf(self):
        # Verificar si hay resultados para exportar
        contenido = self.text_resultado.get(1.0, tk.END).strip()
        if not contenido or "RESULTADO DEL CÁLCULO" not in contenido:
            messagebox.showwarning("Sin Datos", "⚠️ No hay resultados para exportar. Realiza un cálculo primero.")
            return
        
        # Solicitar ubicación de guardado
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")],
            title="Guardar Reporte de Cálculo"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as file:
                    # Encabezado del archivo
                    file.write("=" * 80 + "\n")
                    file.write("          REPORTE DE CÁLCULO DE CHAROLA ELÉCTRICA\n")
                    file.write("        HERTZ INGENIERÍA & SERVICIOS ELÉCTRICOS S.A DE C.V\n")
                    file.write("=" * 80 + "\n\n")
                    
                    # Información de la empresa
                    file.write("EMPRESA: Hertz Ingeniería & Servicios Eléctricos S.A de C.V\n")
                    file.write(f"FECHA DE GENERACIÓN: {datetime.now().strftime('%d de %B de %Y')}\n")
                    file.write(f"HORA: {datetime.now().strftime('%H:%M:%S')}\n")
                    file.write("NORMA APLICADA: NOM-001-SEDE-2012\n")
                    file.write("MÉTODO: Suma de Lados Dinámico\n\n")
                    
                    # Contenido del cálculo
                    file.write(contenido)
                    
                    # Pie de página
                    file.write("\n\n" + "=" * 80 + "\n")
                    file.write("AVISO LEGAL:\n")
                    file.write("Este cálculo ha sido realizado conforme a la norma NOM-001-SEDE-2012.\n")
                    file.write("Hertz Ingeniería se responsabiliza por la correcta aplicación del método.\n")
                    file.write("Para dudas técnicas, contacte con nuestro departamento de ingeniería.\n")
                    file.write("=" * 80 + "\n")
                
                messagebox.showinfo("Exportación Exitosa", f"✅ Reporte guardado exitosamente en:\n{filename}")
                
            except Exception as e:
                messagebox.showerror("Error de Exportación", f"❌ Error al guardar el archivo:\n{str(e)}")
    
    def cerrar_aplicacion(self):
        respuesta = messagebox.askyesno("Confirmar Cierre", 
                                       "¿Estás seguro de que deseas cerrar la aplicación?")
        if respuesta:
            self.root.quit()
    
    def mostrar_bienvenida(self):
        bienvenida = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    🏢 HERTZ INGENIERÍA & SERVICIOS ELÉCTRICOS                ║
║                           CALCULADORA DE CHAROLAS ELÉCTRICAS                 ║
╚══════════════════════════════════════════════════════════════════════════════╝

🎯 BIENVENIDO AL SISTEMA DE CÁLCULOS ELÉCTRICOS

Esta herramienta profesional te permite calcular las dimensiones óptimas de 
charolas eléctricas utilizando el método de "Suma de Lados Dinámico" conforme 
a la norma NOM-001-SEDE-2012.

📋 INSTRUCCIONES DE USO:

1️⃣ Selecciona el TIPO DE CHAROLA (escalera o fondo sólido)
2️⃣ Elige el CALIBRE AWG del conductor
3️⃣ Configura el número de FASES, NEUTROS y TIERRA
4️⃣ Presiona el botón "📐 CALCULAR"
5️⃣ Revisa los resultados y opciones de charola comercial

⚡ CARACTERÍSTICAS DEL SISTEMA:

✅ Cálculo dinámico que se adapta a cualquier configuración
✅ Múltiples opciones de charola comercial disponibles
✅ Historial de cálculos realizados
✅ Exportación de reportes en formato texto
✅ Interfaz profesional y fácil de usar

🔧 ESPECIFICACIONES TÉCNICAS:

• Factor de espaciamiento: 2.15 × diámetro del conductor
• Charolas tipo escalera: 2 fases visibles por grupo trifásico
• Charolas fondo sólido: Fases agrupadas (3 por grupo)
• Anchos comerciales: 4" a 48" pulgadas

📞 SOPORTE TÉCNICO:
Para consultas adicionales, contacte al departamento de ingeniería de 
Hertz Ingeniería & Servicios Eléctricos S.A de C.V

═══════════════════════════════════════════════════════════════════════════════

                         ¡COMIENZA TU CÁLCULO AHORA! 👆

"""
        self.text_resultado.insert(tk.END, bienvenida)
        
        # Aplicar colores a la bienvenida
        self.colorear_texto("HERTZ INGENIERÍA", "titulo")
        self.colorear_texto("BIENVENIDO", "success")
        self.colorear_texto("INSTRUCCIONES", "info")
        self.colorear_texto("CARACTERÍSTICAS", "info")
        self.colorear_texto("ESPECIFICACIONES", "info")


def lanzar_charola_en_ventana(datos_precargados=None):
    ventana = tk.Toplevel()
    app = CharolaCalculatorPro(ventana)
    
    # Precargar el calibre si se pasó como parámetro
    if datos_precargados and "calibre" in datos_precargados:
        app.calibre_var.set(datos_precargados["calibre"])

    ventana.protocol("WM_DELETE_WINDOW", app.cerrar_aplicacion)
    ventana.mainloop()


