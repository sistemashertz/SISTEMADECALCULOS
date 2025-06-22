import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import os


class MenuPrincipal:
    """Ventana principal del sistema. Contiene el menú y delega a otras
    pantallas.  Se ha actualizado para que cada módulo (por ejemplo
    `calculosint`) se abra en una ventana hija (`tk.Toplevel`) mientras la
    ventana principal se oculta con `withdraw()`.  Al cerrar la ventana hija
    el menú vuelve a mostrarse con `deiconify()`."""

    def __init__(self, master: tk.Tk):
        self.master = master
        self.master.title("Sistema de Cálculos Eléctricos - NOM-001-SEDE-2012")
        self.master.geometry("800x600")
        self.master.resizable(False, False)

        # Variables para las imágenes
        self.fondo_image = None
        self.logo_image = None

        # Centrar ventana en pantalla
        self.centrar_ventana()

        # Configurar estilos con paleta Hertz
        self.configurar_estilos()

        # Crear interfaz principal
        self.crear_interfaz()

    # ------------------------------------------------------------------
    # Configuración / utilidades generales
    # ------------------------------------------------------------------
    def centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        self.master.update_idletasks()
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        y = (self.master.winfo_screenheight() // 2) - (height // 2)
        self.master.geometry(f"{width}x{height}+{x}+{y}")

    def cargar_imagenes(self):
        """Carga las imágenes del logo y del fondo usando rutas relativas"""
        base_path = os.path.dirname(os.path.abspath(__file__))

        try:
            fondo_path = os.path.join(base_path, "Imagenes", "fondo.jpeg")
            imagen_fondo = Image.open(fondo_path).resize((800, 600), Image.Resampling.LANCZOS)
            self.fondo_image = ImageTk.PhotoImage(imagen_fondo)
        except Exception as e:
            print(f"Error al cargar fondo: {e}")
            self.fondo_image = None

        try:
            logo_path = os.path.join(base_path, "Imagenes", "logo.png")
            imagen_logo = Image.open(logo_path)
            imagen_logo.thumbnail((150, 80), Image.Resampling.LANCZOS)
            self.logo_image = ImageTk.PhotoImage(imagen_logo)
        except Exception as e:
            print(f"Error al cargar logo: {e}")
            self.logo_image = None

    def configurar_estilos(self):
        """Estilos de botones Hertz"""
        self.style = ttk.Style()
        self.style.theme_use("clam")

        color_naranja = "#E85A2B"
        color_naranja_hover = "#F26B3A"
        color_naranja_pressed = "#D44B22"
        color_gris_medio = "#4A4A4A"

        self.style.configure(
            "Hertz.TButton",
            background=color_naranja,
            foreground="white",
            font=("Century Gothic", 12, "bold"),
            borderwidth=0,
            focuscolor="none",
            padding=(20, 12),
        )
        self.style.map(
            "Hertz.TButton",
            background=[("active", color_naranja_hover), ("pressed", color_naranja_pressed)],
        )

        self.style.configure(
            "Exit.TButton",
            background=color_gris_medio,
            foreground="white",
            font=("Century Gothic", 11, "bold"),
            borderwidth=0,
            focuscolor="none",
            padding=(15, 10),
        )

    # ------------------------------------------------------------------
    # Construcción de la interfaz
    # ------------------------------------------------------------------
    def crear_interfaz(self):
        self.cargar_imagenes()

        # Canvas para el fondo
        self.canvas = tk.Canvas(self.master, width=800, height=600, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        if self.fondo_image:
            self.canvas.create_image(0, 0, image=self.fondo_image, anchor="nw")
        else:
            self.canvas.configure(bg="#F5F5F5")

        main_frame = tk.Frame(self.canvas, bg="white", relief="solid", bd=1)
        self.canvas.create_window(400, 300, window=main_frame, width=650, height=550)

        self.crear_contenido(main_frame)

    def crear_contenido(self, parent):
        """Agrupa la creación de secciones de la pantalla"""
        self.crear_header(parent)
        self.crear_titulo_principal(parent)
        self.crear_separador(parent)
        self.crear_botones_principales(parent)
        self.crear_footer(parent)

    def crear_header(self, parent):
        """Crea el header con logo Hertz"""
        header_frame = tk.Frame(parent, bg='white', height=90)
        header_frame.pack(fill='x', padx=20, pady=(15, 0))
        header_frame.pack_propagate(False)
        
        if self.logo_image:
            # Logo Hertz
            logo_label = tk.Label(header_frame, image=self.logo_image, bg='white')
            logo_label.pack(side='left', pady=5)
        else:
            # Texto de respaldo si no se encuentra el logo
            logo_frame = tk.Frame(header_frame, bg='white')
            logo_frame.pack(side='left', pady=10)
            
            tk.Label(logo_frame, 
                    text="HERTZ", 
                    font=('Century Gothic', 18, 'bold'), 
                    bg='white', 
                    fg='#E85A2B').pack(anchor='w')
            
            tk.Label(logo_frame, 
                    text="Ingeniería & Servicios Eléctricos", 
                    font=('Century Gothic', 9), 
                    bg='white', 
                    fg='#E85A2B').pack(anchor='w')
        
        # Información de la norma (alineada a la derecha)
        info_frame = tk.Frame(header_frame, bg='white')
        info_frame.pack(side='right', pady=15)
        
        tk.Label(info_frame, 
                text="NOM-001-SEDE-2012", 
                font=('Century Gothic', 14, 'bold'), 
                bg='white', 
                fg='#2C2C2C').pack(anchor='e')
        
        tk.Label(info_frame, 
                text="Ingeniería & Servicios Eléctricos", 
                font=('Century Gothic', 10), 
                bg='white', 
                fg='#4A4A4A').pack(anchor='e')

    def crear_titulo_principal(self, parent):
        """Crea el título principal"""
        title_frame = tk.Frame(parent, bg='white')
        title_frame.pack(fill='x', padx=30, pady=(20, 10))
        
        tk.Label(title_frame, 
                text="Sistema de Cálculos Eléctricos", 
                font=('Century Gothic', 22, 'bold'), 
                bg='white', 
                fg='#2C2C2C').pack()
        
        tk.Label(title_frame, 
                text="Selecciona una opción para continuar con tus cálculos", 
                font=('Century Gothic', 11), 
                bg='white', 
                fg='#4A4A4A').pack(pady=(5, 0))

    def crear_separador(self, parent):
        """Crea un separador con estilo Hertz"""
        separator_frame = tk.Frame(parent, bg='white')
        separator_frame.pack(fill='x', padx=30, pady=20)
        
        # Línea naranja
        tk.Frame(separator_frame, bg='#E85A2B', height=3).pack(fill='x')

    def crear_botones_principales(self, parent):
        """Crea los botones principales"""
        buttons_frame = tk.Frame(parent, bg='white')
        buttons_frame.pack(fill='both', expand=True, padx=40, pady=15)
        
        # Configuración de botones
        botones_config = [
            {
                'text': '⚡ Cálculos Eléctricos',
                'command': self.abrir_calculos,
                'description': 'Realizar cálculos según norma NOM-001-SEDE-2012'
            },
            {
                'text': '📊 Historial de Cargas',
                'command': self.abrir_historial,
                'description': 'Consultar historial de cálculos realizados'
            },
            {
                'text': 'ℹ️ Acerca del Sistema',
                'command': self.abrir_acerca,
                'description': 'Información sobre el sistema y desarrollador'
            }
        ]
        
        for i, config in enumerate(botones_config):
            self.crear_boton_hertz(buttons_frame, config)
        
        # Espacio antes del botón de salir
        tk.Frame(buttons_frame, bg='white', height=15).pack()
        
        # Botón de salir
        exit_btn = ttk.Button(buttons_frame, 
                  text="🚪 Salir del Sistema", 
                  command=self.confirmar_salida,
                  style='Exit.TButton')
        exit_btn.pack(fill='x', padx=20)

    def crear_boton_hertz(self, parent, config):
        """Crea un botón con estilo Hertz"""
        button_frame = tk.Frame(parent, bg='white')
        button_frame.pack(fill='x', pady=6, padx=20)
        
        # Botón principal
        btn = ttk.Button(button_frame, 
                        text=config['text'], 
                        command=config['command'],
                        style='Hertz.TButton')
        btn.pack(fill='x')
        
        # Descripción
        tk.Label(button_frame, 
                text=config['description'], 
                font=('Century Gothic', 9), 
                bg='white', 
                fg='#666666').pack(pady=(4, 0))

    def crear_footer(self, parent):
        """Crea el footer"""
        footer_frame = tk.Frame(parent, bg='white')
        footer_frame.pack(fill='x', side='bottom', padx=30, pady=(20, 20))
        
        # Separador sutil
        tk.Frame(footer_frame, bg='#E0E0E0', height=1).pack(fill='x', pady=(0, 15))
        
        # Información del desarrollador
        tk.Label(footer_frame, 
                text="Desarrollado por Ariadna Aguilar • Residencia Profesional 2025", 
                font=('Century Gothic', 9), 
                bg='white', 
                fg='#666666').pack()
        
        tk.Label(footer_frame, 
                text="Hertz Ingeniería & Servicios Eléctricos • Versión 1.0", 
                font=('Century Gothic', 8), 
                bg='white', 
                fg='#999999').pack(pady=(2, 0))

    def confirmar_salida(self):
        """Confirma la salida del sistema"""
        resultado = messagebox.askyesno(
            "Confirmar Salida", 
            "¿Está seguro que desea salir del sistema?",
            icon='question'
        )
        if resultado:
            self.master.quit()

    def abrir_calculos(self):
        """Abre la pantalla de cálculos en una ventana hija y oculta el menú."""
        # 1) Oculta el menú principal
        self.master.withdraw()

        # 2) Crea una ventana hija (Toplevel)
        calc_win = tk.Toplevel(self.master)
        calc_win.title("Cálculos Eléctricos - Hertz")
        calc_win.geometry("800x600")
        calc_win.resizable(False, False)

        # 3) Instancia la pantalla de cálculos dentro de esa ventana hija
        try:
            from calculosint import Calculos
            Calculos(calc_win)  # ← importado por demanda
        except ImportError:
            messagebox.showwarning(
                "Módulo no encontrado",
                "No se pudo cargar el módulo de cálculos.\nVerifique que 'calculosint.py' existe.",
            )
            calc_win.destroy()
            self.master.deiconify()
            return

        # 4) Cuando el usuario cierre la ventana hija, se restaura el menú
        def _cerrar_calculos():
            calc_win.destroy()
            self.master.deiconify()

        calc_win.protocol("WM_DELETE_WINDOW", _cerrar_calculos)

    def abrir_historial(self):
        """Abre la ventana de historial"""
        historial_window = tk.Toplevel(self.master)
        historial_window.title("Historial de Cargas - Hertz")
        historial_window.geometry("600x400")
        historial_window.configure(bg='white')
        historial_window.resizable(False, False)
        
        # Centrar ventana
        historial_window.transient(self.master)
        historial_window.grab_set()
        
        # Contenido
        frame = tk.Frame(historial_window, bg='white')
        frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Header con línea naranja
        header_frame = tk.Frame(frame, bg='white')
        header_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(header_frame, 
                text="📊 Historial de Cargas", 
                font=('Century Gothic', 18, 'bold'), 
                bg='white', 
                fg='#2C2C2C').pack()
        
        tk.Frame(header_frame, bg='#E85A2B', height=3).pack(fill='x', pady=(10, 0))
        
        # Contenido
        tk.Label(frame, 
                text="Esta funcionalidad está en desarrollo.\n\nPróximamente podrá consultar el historial\nde todos los cálculos realizados en el sistema.", 
                font=('Century Gothic', 12), 
                bg='white', 
                fg='#4A4A4A',
                justify='center').pack(pady=60)
        
        # Botón cerrar
        ttk.Button(frame, 
                  text="Cerrar", 
                  command=historial_window.destroy,
                  style='Hertz.TButton').pack()

    def abrir_acerca(self):
        """Abre la ventana de información"""
        acerca_window = tk.Toplevel(self.master)
        acerca_window.title("Acerca del Sistema - Hertz")
        acerca_window.geometry("500x400")
        acerca_window.configure(bg='white')
        acerca_window.resizable(False, False)
        
        # Centrar ventana
        acerca_window.transient(self.master)
        acerca_window.grab_set()
        
        # Contenido
        frame = tk.Frame(acerca_window, bg='white')
        frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Logo (si está disponible)
        if self.logo_image:
            logo_label = tk.Label(frame, image=self.logo_image, bg='white')
            logo_label.pack(pady=(0, 20))
        
        # Línea naranja
        tk.Frame(frame, bg='#E85A2B', height=3).pack(fill='x', pady=(0, 20))
        
        # Información
        info_text = """Sistema de Cálculos Eléctricos
        
Desarrollado por: Ariadna Aguilar
Proyecto: Residencia Profesional 2025
Empresa: Hertz Ingeniería & Servicios Eléctricos
Basado en: NOM-001-SEDE-2012

Este sistema permite realizar cálculos eléctricos
conforme a las especificaciones de la norma
mexicana NOM-001-SEDE-2012.

Versión 1.0 • Junio 2025"""
        
        tk.Label(frame, 
                text=info_text, 
                font=('Century Gothic', 11), 
                bg='white', 
                fg='#2C2C2C',
                justify='center').pack(pady=20)
        
        # Botón cerrar
        ttk.Button(frame, 
                  text="Cerrar", 
                  command=acerca_window.destroy,
                  style='Hertz.TButton').pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = MenuPrincipal(root)
    root.mainloop()