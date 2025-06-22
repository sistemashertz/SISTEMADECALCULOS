import tkinter as tk
from tkinter import ttk, messagebox
import math

class CharolaCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Charolas - Método Suma de Lados Dinámico")
        self.root.geometry("800x700")
        
        # Diccionario de áreas de conductores (mm²) - mantenido por compatibilidad
        self.areas_mm2 = {
            "14": 2.08, "12": 3.31, "10": 5.26, "8": 8.37, "6": 13.3, "4": 21.2, "2": 33.6,
            "1": 42.4, "1/0": 53.5, "2/0": 67.4, "3/0": 85.0, "4/0": 107,
            "250": 127, "300": 152, "400": 203, "500": 253, "600": 304,
            "750": 380, "1000": 507
        }
        
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
        
        # Tabla de áreas de conductores según NOM-001-SEDE-2012 (mm²)
        self.tabla_charola_mm2 = {
            "14": 13.30,
            "12": 19.35,
            "10": 26.67,
            "8": 53.48,
            "6": 66.77,
            "4": 85.29,
            "2": 86.00,
            "1": 122.60,
            "1/0": 143.40,
            "2/0": 169.30,
            "3/0": 201.10,
            "4/0": 239.90,
            "250": 296.50,
            "300": 340.70,
            "400": 427.00,
            "500": 509.70,
            "600": 606.70,
            "750": 744.80,
            "1000": 1006.45
        }
        
        # Lista de calibres (excluyendo 350 como especificaste)
        self.calibres_disponibles = ["14", "12", "10", "8", "6", "4", "2", "1", 
                                   "1/0", "2/0", "3/0", "4/0", "250", "300", 
                                   "400", "500", "600", "750", "1000"]
        
        # Anchos comerciales de charola (pulgadas)
        self.anchos_charola_pulgadas = [6, 9, 12, 14, 16, 20, 24, 30, 32, 36]
        
        self.setup_ui()
    
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        title_label = ttk.Label(main_frame, text="Calculadora de Charolas Eléctricas", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Subtitle - Método
        subtitle_label = ttk.Label(main_frame, text="Método: Suma de Lados Dinámico (MEJORADO)", 
                                  font=('Arial', 10, 'italic'))
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 10))
        
        # Frame de entrada
        input_frame = ttk.LabelFrame(main_frame, text="Configuración de Conductores", padding="10")
        input_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Calibre
        ttk.Label(input_frame, text="Calibre AWG:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.calibre_var = tk.StringVar()
        calibre_combo = ttk.Combobox(input_frame, textvariable=self.calibre_var, 
                                    values=list(self.tabla_diametros.keys()), state="readonly")
        calibre_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # Checkboxes y entradas para tipos de conductores
        # Fases
        self.incluye_fases = tk.BooleanVar(value=True)
        ttk.Checkbutton(input_frame, text="Fases", variable=self.incluye_fases,
                       command=self.toggle_fases).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.fases_var = tk.IntVar(value=3)
        self.fases_entry = ttk.Entry(input_frame, textvariable=self.fases_var, width=10)
        self.fases_entry.grid(row=1, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Neutros
        self.incluye_neutros = tk.BooleanVar(value=True)
        ttk.Checkbutton(input_frame, text="Neutros", variable=self.incluye_neutros,
                       command=self.toggle_neutros).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.neutros_var = tk.IntVar(value=1)
        self.neutros_entry = ttk.Entry(input_frame, textvariable=self.neutros_var, width=10)
        self.neutros_entry.grid(row=2, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Tierra
        self.incluye_tierra = tk.BooleanVar(value=True)
        ttk.Checkbutton(input_frame, text="Tierra", variable=self.incluye_tierra,
                       command=self.toggle_tierra).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.tierra_var = tk.IntVar(value=1)
        self.tierra_entry = ttk.Entry(input_frame, textvariable=self.tierra_var, width=10)
        self.tierra_entry.grid(row=3, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Botón de cálculo
        calc_button = ttk.Button(main_frame, text="Calcular Charola", command=self.calcular)
        calc_button.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Frame de resultados
        result_frame = ttk.LabelFrame(main_frame, text="Resultados", padding="10")
        result_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Text widget para mostrar resultados
        self.resultado_text = tk.Text(result_frame, height=20, width=80, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.resultado_text.yview)
        self.resultado_text.configure(yscrollcommand=scrollbar.set)
        
        self.resultado_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configurar tags para colores
        self.resultado_text.tag_configure("success", foreground="green", font=('Arial', 10, 'bold'))
        self.resultado_text.tag_configure("error", foreground="red", font=('Arial', 10, 'bold'))
        
        # Configurar grid weights
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
        input_frame.columnconfigure(1, weight=1)
    
    def toggle_fases(self):
        if self.incluye_fases.get():
            self.fases_entry.config(state='normal')
        else:
            self.fases_entry.config(state='disabled')
    
    def toggle_neutros(self):
        if self.incluye_neutros.get():
            self.neutros_entry.config(state='normal')
        else:
            self.neutros_entry.config(state='disabled')
    
    def toggle_tierra(self):
        if self.incluye_tierra.get():
            self.tierra_entry.config(state='normal')
        else:
            self.tierra_entry.config(state='disabled')
    
    def validar_entrada(self):
        if not self.calibre_var.get():
            messagebox.showerror("Error", "Selecciona un calibre AWG")
            return False
        
        # Validar que al menos un tipo esté seleccionado
        if not (self.incluye_fases.get() or self.incluye_neutros.get() or self.incluye_tierra.get()):
            messagebox.showerror("Error", "Selecciona al menos un tipo de conductor")
            return False
        
        # Validar valores numéricos
        try:
            if self.incluye_fases.get() and self.fases_var.get() <= 0:
                raise ValueError("Número de fases debe ser mayor a 0")
            if self.incluye_neutros.get() and self.neutros_var.get() <= 0:
                raise ValueError("Número de neutros debe ser mayor a 0")
            if self.incluye_tierra.get() and self.tierra_var.get() <= 0:
                raise ValueError("Número de tierras debe ser mayor a 0")
        except tk.TclError:
            messagebox.showerror("Error", "Ingresa valores numéricos válidos")
            return False
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return False
        
        return True
    
    def realizar_calculo(self, calibre, configuracion):
        """Cálculo DINÁMICO de charola basado en configuración real del usuario"""
        if calibre not in self.tabla_diametros:
            raise ValueError("El calibre no tiene diámetro definido")
        
        d = self.tabla_diametros[calibre]  # diámetro en mm
        espaciamiento = 2.15
        
        # Obtener datos reales introducidos por el usuario
        fases = configuracion['fases'] if configuracion['incluye_fases'] else 0
        neutros = configuracion['neutros'] if configuracion['incluye_neutros'] else 0
        tierra = configuracion['tierra'] if configuracion['incluye_tierra'] else 0
        
        # LÓGICA DINÁMICA MEJORADA:
        
        # 1. Calcular cuántas filas horizontales se necesitan
        # Asumiendo que cada fila acomoda 2 fases optimalmente
        if fases > 0:
            filas_horizontales = math.ceil(fases / 2)
        else:
            filas_horizontales = 1  # Al menos una fila si hay neutros
        
        # 2. Cada fila contiene: 2 fases + neutros proporcionales
        neutros_por_fila = math.ceil(neutros / filas_horizontales) if neutros > 0 else 0
        conductores_por_fila = min(2, fases) + neutros_por_fila  # Máximo 2 fases por fila
        
        # 3. Calcular dimensiones
        hilos_horizontales = conductores_por_fila
        hilos_verticales = filas_horizontales
        
        # Si hay tierra, se añade una capa más
        if tierra > 0:
            hilos_verticales += 1
        
        # Ancho horizontal: diámetros + separaciones entre conductores
        separaciones_horizontales = max(0, hilos_horizontales - 1)
        lado_horizontal = (d * hilos_horizontales) + (espaciamiento * d * separaciones_horizontales)
        
        # Alto vertical: separaciones entre capas
        separaciones_verticales = max(0, hilos_verticales - 1)
        lado_vertical = espaciamiento * d * separaciones_verticales
        
        suma_total_mm = lado_horizontal + lado_vertical
        suma_total_pulg = suma_total_mm / 25.4  # conversión a pulgadas

        # Buscar charola comercial
        charola_sugerida = None
        area_charola_seleccionada = 0
        for ancho in self.anchos_charola_pulgadas:
            if ancho >= suma_total_pulg:
                charola_sugerida = ancho
                area_charola_seleccionada = ancho * ancho
                break

        return {
            'diametro': d,
            'fases': fases,
            'neutros': neutros,
            'tierra': tierra,
            'filas_horizontales': filas_horizontales,
            'neutros_por_fila': neutros_por_fila,
            'conductores_por_fila': conductores_por_fila,
            'horizontales': hilos_horizontales,
            'verticales': hilos_verticales,
            'separaciones_horizontales': separaciones_horizontales,
            'separaciones_verticales': separaciones_verticales,
            'lado_horizontal': lado_horizontal,
            'lado_vertical': lado_vertical,
            'suma_total_mm': suma_total_mm,
            'suma_total_pulg': suma_total_pulg,
            'charola_sugerida': charola_sugerida,
            'area_charola_seleccionada': area_charola_seleccionada
        }
    
    def calcular(self):
        if not self.validar_entrada():
            return
        
        calibre = self.calibre_var.get()
        
        # Configuración de conductores
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
        except Exception as e:
            messagebox.showerror("Error en el cálculo", str(e))
    
    def mostrar_resultados(self, calibre, configuracion, resultado):
        self.resultado_text.delete(1.0, tk.END)

        texto_resultado = "=" * 80 + "\n"
        texto_resultado += "     RESULTADO DEL CÁLCULO DE CHAROLA (SUMA DE LADOS DINÁMICO)\n"
        texto_resultado += "                    CONFIGURACIÓN PERSONALIZADA\n"
        texto_resultado += "=" * 80 + "\n\n"

        texto_resultado += "🎯 DISTRIBUCIÓN CALCULADA DINÁMICAMENTE:\n"
        texto_resultado += f"   • Total de fases: {resultado['fases']}\n"
        texto_resultado += f"   • Total de neutros: {resultado['neutros']}\n"
        texto_resultado += f"   • Total de tierras: {resultado['tierra']}\n"
        texto_resultado += f"   • Filas horizontales necesarias: {resultado['filas_horizontales']}\n"
        texto_resultado += f"   • Conductores por fila: {resultado['conductores_por_fila']}\n"
        if resultado['neutros'] > 0:
            texto_resultado += f"   • Neutros por fila: {resultado['neutros_por_fila']}\n"
        texto_resultado += "\n"

        texto_resultado += "📋 CONFIGURACIÓN DE CONDUCTORES:\n"
        if configuracion['incluye_fases']:
            texto_resultado += f"   • Fases: {configuracion['fases']} conductor(es)\n"
        if configuracion['incluye_neutros']:
            texto_resultado += f"   • Neutros: {configuracion['neutros']} conductor(es)\n"
        if configuracion['incluye_tierra']:
            texto_resultado += f"   • Tierra: {configuracion['tierra']} conductor(es)\n"
        texto_resultado += f"   • Calibre del conductor: {calibre} AWG\n\n"

        texto_resultado += "📐 CÁLCULO DETALLADO:\n"
        texto_resultado += f"   • Diámetro del conductor: {resultado['diametro']:.2f} mm\n"
        texto_resultado += f"   • Factor de espaciamiento: 2.15\n\n"
        
        texto_resultado += "🔸 ANCHO HORIZONTAL (distribución optimizada):\n"
        texto_resultado += f"   • Conductores horizontales por fila: {resultado['horizontales']}\n"
        texto_resultado += f"   • Separaciones horizontales: {resultado['separaciones_horizontales']}\n"
        texto_resultado += f"   • Cálculo: ({resultado['diametro']:.2f} × {resultado['horizontales']}) + (2.15 × {resultado['diametro']:.2f} × {resultado['separaciones_horizontales']})\n"
        texto_resultado += f"   • Lado horizontal: {resultado['lado_horizontal']:.2f} mm\n\n"
        
        texto_resultado += "🔸 ALTO VERTICAL (capas necesarias):\n"
        texto_resultado += f"   • Capas verticales: {resultado['verticales']}\n"
        texto_resultado += f"   • Separaciones verticales: {resultado['separaciones_verticales']}\n"
        texto_resultado += f"   • Cálculo: 2.15 × {resultado['diametro']:.2f} × {resultado['separaciones_verticales']}\n"
        texto_resultado += f"   • Lado vertical: {resultado['lado_vertical']:.2f} mm\n\n"
        
        texto_resultado += f"🔸 SUMA TOTAL:\n"
        texto_resultado += f"   • Total: {resultado['suma_total_mm']:.2f} mm = {resultado['suma_total_pulg']:.2f} pulgadas\n\n"

        texto_resultado += "🎯 CHAROLA SUGERIDA:\n"
        if resultado['charola_sugerida']:
            texto_resultado += f"   ✅ CHAROLA COMERCIAL: {resultado['charola_sugerida']}\" pulgadas de ancho\n"
            porcentaje_uso = (resultado['suma_total_pulg'] ** 2) / resultado['area_charola_seleccionada'] * 100
            texto_resultado += f"   • Porcentaje aproximado de uso: {porcentaje_uso:.2f}%\n"
        else:
            texto_resultado += "   ❌ NO SE ENCONTRÓ CHAROLA COMERCIAL ADECUADA\n"
            texto_resultado += f"   • Se requiere ancho mínimo de: {resultado['suma_total_pulg']:.2f}\"\n"

        texto_resultado += "\n" + "=" * 80 + "\n"
        texto_resultado += "✓ Método: Suma de lados con lógica DINÁMICA\n"
        texto_resultado += "✓ Se adapta automáticamente a cualquier configuración\n"
        texto_resultado += "✓ Optimización de filas: 2 fases por fila horizontal\n"
        texto_resultado += "✓ Norma: NOM-001-SEDE-2012 (criterio físico)\n"

        self.resultado_text.insert(tk.END, texto_resultado)

        if resultado['charola_sugerida']:
            self.colorear_resultado("CHAROLA COMERCIAL", "success", "green")
        else:
            self.colorear_resultado("NO SE ENCONTRÓ CHAROLA", "error", "red")
    
    def colorear_resultado(self, texto_buscar, tag, color):
        """Colorea texto específico en los resultados"""
        contenido = self.resultado_text.get(1.0, tk.END)
        inicio = contenido.find(texto_buscar)
        if inicio != -1:
            fin = inicio + len(texto_buscar)
            self.resultado_text.tag_add(tag, f"1.0+{inicio}c", f"1.0+{fin}c")


# Función principal para ejecutar la aplicación
def main():
    root = tk.Tk()
    app = CharolaCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()