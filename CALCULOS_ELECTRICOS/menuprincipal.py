import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import os
import logging


class Config:
    """Clase de configuración centralizada"""
    WINDOW_SIZE = (950, 750)
    MIN_WINDOW_SIZE = (800, 600)
    
    COLORS = {
        'primary': '#E85A2B',
        'hover': '#F26B3A',
        'pressed': '#D44B22',
        'gray': '#4A4A4A',
        'white': '#FFFFFF',
        'text_primary': '#2C2C2C',
        'text_secondary': '#4A4A4A',
        'text_light': '#666666',
        'separator': '#E0E0E0'
    }

    FONTS = {
        'title': ('Century Gothic', 20, 'bold'),
        'subtitle': ('Century Gothic', 18, 'bold'),
        'button': ('Century Gothic', 12, 'bold'),
        'button_small': ('Century Gothic', 11, 'bold'),
        'text': ('Century Gothic', 11),
        'text_small': ('Century Gothic', 10),
        'text_tiny': ('Century Gothic', 9),
        'footer': ('Century Gothic', 8)
    }
    
    IMAGES = {
        'fondo': 'fondo.jpeg',
        'logo': 'logo.png',
        'icon_user': 'iconUser.png'
    }


class MenuPrincipal:
    """Ventana principal del sistema con funcionalidad de administrador"""

    def __init__(self, master: tk.Tk):
        self.master = master
        self.master.title("Sistema de Cálculos Eléctricos - NOM-001-SEDE-2012")
        
        # Configurar logging
        self.setup_logging()
        
        # Verificar dependencias
        if not self.verificar_dependencias():
            return
        
        # Variables del usuario (se asignan desde LoginVentana)
        self.usuario_logueado = None
        self.datos_usuario = None
        self.is_admin = False
        
        # Variables para las imágenes
        self.fondo_image = None
        self.logo_image = None
        self.icon_user = None
        self.admin_icon = None
        
        # Configurar ventana
        self.configurar_ventana()
        
        # Configurar estilos con paleta Hertz
        self.configurar_estilos()
        
        # Crear interfaz principal
        self.crear_interfaz()
        
        # Configurar cierre de aplicación
        self.master.protocol("WM_DELETE_WINDOW", self.confirmar_salida)

    def setup_logging(self):
        """Configura el sistema de logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def verificar_dependencias(self):
        """Verifica que todas las dependencias estén disponibles"""
        dependencias = {
            'PIL': 'Pillow',
            'tkinter': 'Tkinter'
        }
        faltantes = []
        
        for modulo, nombre in dependencias.items():
            try:
                if modulo == 'PIL':
                    from PIL import Image, ImageTk
                else:
                    __import__(modulo)
            except ImportError:
                faltantes.append(nombre)
        
        if faltantes:
            error_msg = f"Dependencias faltantes: {', '.join(faltantes)}"
            self.logger.error(error_msg)
            messagebox.showerror("Error de Dependencias", error_msg)
            return False
        return True

    def configurar_ventana(self):
        """Configura las propiedades de la ventana principal"""
        # Ajustar tamaño según resolución
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        
        if screen_width < 1024 or screen_height < 768:
            width, height = Config.MIN_WINDOW_SIZE
        else:
            width, height = Config.WINDOW_SIZE
            
        self.master.geometry(f"{width}x{height}")
        self.master.resizable(False, False)
        
        # Centrar ventana en pantalla
        self.centrar_ventana()

    def centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        self.master.update_idletasks()
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        y = (self.master.winfo_screenheight() // 2) - (height // 2)
        self.master.geometry(f"{width}x{height}+{x}+{y}")

    def cargar_imagenes(self):
        """Carga las imágenes incluyendo el icono de administrador"""
        base_path = os.path.dirname(os.path.abspath(__file__))
        images_path = os.path.join(base_path, "Imagenes")
        
        # Verificar que el directorio de imágenes existe
        if not os.path.exists(images_path):
            self.logger.warning(f"Directorio de imágenes no encontrado: {images_path}")
            return
        
        # Cargar imagen de fondo
        try:
            fondo_path = os.path.join(images_path, Config.IMAGES['fondo'])
            if os.path.exists(fondo_path):
                imagen_fondo = Image.open(fondo_path)
                window_size = (self.master.winfo_width(), self.master.winfo_height())
                imagen_fondo = imagen_fondo.resize(window_size, Image.Resampling.LANCZOS)
                self.fondo_image = ImageTk.PhotoImage(imagen_fondo)
                self.logger.info("Imagen de fondo cargada correctamente")
            else:
                self.logger.warning(f"Archivo de fondo no encontrado: {fondo_path}")
        except Exception as e:
            self.logger.error(f"Error al cargar imagen de fondo: {e}")
            self.fondo_image = None

        # Cargar logo
        try:
            logo_path = os.path.join(images_path, Config.IMAGES['logo'])
            if os.path.exists(logo_path):
                imagen_logo = Image.open(logo_path)
                imagen_logo.thumbnail((130, 60), Image.Resampling.LANCZOS)
                self.logo_image = ImageTk.PhotoImage(imagen_logo)
                self.logger.info("Logo cargado correctamente")
            else:
                self.logger.warning(f"Archivo de logo no encontrado: {logo_path}")
        except Exception as e:
            self.logger.error(f"Error al cargar logo: {e}")
            self.logo_image = None
        
        # Cargar icono de usuario
        try:
            icon_user_path = os.path.join(images_path, Config.IMAGES['icon_user'])
            if os.path.exists(icon_user_path):
                imagen_icon_user = Image.open(icon_user_path)
                imagen_icon_user.thumbnail((50, 50), Image.Resampling.LANCZOS)
                self.icon_user = ImageTk.PhotoImage(imagen_icon_user)
                self.logger.info("Icono de usuario cargado correctamente")
            else:
                self.logger.warning(f"Archivo de icono de usuario no encontrado: {icon_user_path}")
        except Exception as e:
            self.logger.error(f"Error al cargar icono de usuario: {e}")
            self.icon_user = None

        # NUEVO: Cargar icono de administrador
        try:
            admin_icon_path = os.path.join(images_path, "admin_icon.png")
            if os.path.exists(admin_icon_path):
                imagen_admin = Image.open(admin_icon_path)
                imagen_admin.thumbnail((32, 32), Image.Resampling.LANCZOS)
                self.admin_icon = ImageTk.PhotoImage(imagen_admin)
                self.logger.info("Icono de administrador cargado correctamente")
            else:
                # Crear icono simple si no existe
                self.crear_icono_admin_simple(admin_icon_path)
                imagen_admin = Image.open(admin_icon_path)
                imagen_admin.thumbnail((32, 32), Image.Resampling.LANCZOS)
                self.admin_icon = ImageTk.PhotoImage(imagen_admin)
        except Exception as e:
            self.logger.error(f"Error al cargar icono de admin: {e}")
            self.admin_icon = None

    def crear_icono_admin_simple(self, path):
        """Crea un icono simple de administrador si no existe"""
        try:
            from PIL import Image, ImageDraw
            
            # Crear imagen 32x32 con un ícono de usuario + engranaje
            img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Dibujar usuario
            draw.ellipse([6, 2, 18, 14], fill='#E85A2B', outline='#D44B22', width=2)  # Cabeza
            draw.ellipse([2, 12, 22, 28], fill='#E85A2B', outline='#D44B22', width=2)  # Cuerpo
            
            # Dibujar engranaje pequeño (símbolo de admin)
            draw.ellipse([20, 20, 30, 30], fill='#4A4A4A', outline='#2C2C2C', width=1)
            draw.ellipse([23, 23, 27, 27], fill='white')
            
            img.save(path, "PNG")
            self.logger.info(f"Icono de admin creado en: {path}")
            
        except Exception as e:
            self.logger.error(f"Error al crear icono de admin: {e}")

    def configurar_estilos(self):
        """Estilos de botones Hertz"""
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Estilo para botones principales
        self.style.configure(
            "Hertz.TButton",
            background=Config.COLORS['primary'],
            foreground=Config.COLORS['white'],
            font=Config.FONTS['button'],
            borderwidth=0,
            focuscolor="none",
            padding=(20, 12),
        )
        self.style.map(
            "Hertz.TButton",
            background=[
                ("active", Config.COLORS['hover']), 
                ("pressed", Config.COLORS['pressed'])
            ],
        )

        # Estilo para botón de salir
        self.style.configure(
            "Exit.TButton",
            background=Config.COLORS['gray'],
            foreground=Config.COLORS['white'],
            font=Config.FONTS['button_small'],
            borderwidth=0,
            focuscolor="none",
            padding=(15, 10),
        )
        
        self.style.map(
            "Exit.TButton",
            background=[("active", "#5A5A5A"), ("pressed", "#3A3A3A")],
        )

    def crear_interfaz(self):
        """Crea la interfaz principal"""
        self.cargar_imagenes()

        # Canvas para el fondo
        self.canvas = tk.Canvas(
            self.master, 
            width=self.master.winfo_width(), 
            height=self.master.winfo_height(), 
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)
        
        if self.fondo_image:
            self.canvas.create_image(0, 0, image=self.fondo_image, anchor="nw")
        else:
            self.canvas.configure(bg="#F5F5F5")

        # Frame principal
        main_frame = tk.Frame(self.canvas, bg=Config.COLORS['white'], relief="solid", bd=1)
        canvas_width = self.canvas.winfo_reqwidth()
        canvas_height = self.canvas.winfo_reqheight()
        
        self.canvas.create_window(
            canvas_width // 2, 
            canvas_height // 2, 
            window=main_frame,
            width=min(800, canvas_width - 100),
            height=min(700, canvas_height - 50)
        )

        self.crear_contenido(main_frame)

    def crear_contenido(self, parent):
        """Agrupa la creación de secciones de la pantalla"""
        self.crear_header(parent)
        self.crear_titulo_principal(parent)
        self.crear_separador(parent)
        self.crear_botones_principales(parent)
        self.crear_footer(parent)

    def crear_header(self, parent):
        """Crea el header con logo Hertz y botón de admin si corresponde"""
        header_frame = tk.Frame(parent, bg=Config.COLORS['white'], height=90)
        header_frame.pack(fill='x', padx=20, pady=(15, 0))
        header_frame.pack_propagate(False)
        
        # Logo Hertz (lado izquierdo)
        if self.logo_image:
            logo_label = tk.Label(header_frame, image=self.logo_image, bg=Config.COLORS['white'])
            logo_label.pack(side='left', pady=5)
        else:
            # Texto de respaldo si no se encuentra el logo
            logo_frame = tk.Frame(header_frame, bg=Config.COLORS['white'])
            logo_frame.pack(side='left', pady=10)
            
            tk.Label(
                logo_frame, 
                text="HERTZ", 
                font=Config.FONTS['subtitle'], 
                bg=Config.COLORS['white'], 
                fg=Config.COLORS['primary']
            ).pack(anchor='w')
            
            tk.Label(
                logo_frame, 
                text="Ingeniería & Servicios Eléctricos", 
                font=Config.FONTS['text_tiny'], 
                bg=Config.COLORS['white'], 
                fg=Config.COLORS['primary']
            ).pack(anchor='w')

        # NUEVO: Sección del usuario logueado (centro)
        if self.usuario_logueado:
            user_info_frame = tk.Frame(header_frame, bg=Config.COLORS['white'])
            user_info_frame.pack(side='left', expand=True, padx=20)
            
            # Información del usuario
            welcome_text = f"Bienvenido: {self.usuario_logueado}"
            if self.datos_usuario and self.datos_usuario.get('nombre'):
                welcome_text = f"Bienvenido: {self.datos_usuario['nombre']}"
            
            tk.Label(
                user_info_frame,
                text=welcome_text,
                font=Config.FONTS['text_small'],
                bg=Config.COLORS['white'],
                fg=Config.COLORS['text_primary']
            ).pack(anchor='center')
            
            # Mostrar rol
            rol_display = "Administrador" if self.is_admin else "Usuario"
            tk.Label(
                user_info_frame,
                text=f"Rol: {rol_display}",
                font=Config.FONTS['text_tiny'],
                bg=Config.COLORS['white'],
                fg=Config.COLORS['text_secondary']
            ).pack(anchor='center')

        # NUEVO: Botón de administrador (solo visible para admin)
        if self.is_admin:
            self.crear_boton_admin(header_frame)
        
        # Información de la norma (lado derecho)
        info_frame = tk.Frame(header_frame, bg=Config.COLORS['white'])
        info_frame.pack(side='right', pady=15)
        
        tk.Label(
            info_frame, 
            text="NOM-001-SEDE-2012", 
            font=Config.FONTS['button'], 
            bg=Config.COLORS['white'], 
            fg=Config.COLORS['text_primary']
        ).pack(anchor='e')
        
        tk.Label(
            info_frame, 
            text="Ingeniería & Servicios Eléctricos", 
            font=Config.FONTS['text_small'], 
            bg=Config.COLORS['white'], 
            fg=Config.COLORS['text_secondary']
        ).pack(anchor='e')

    def crear_boton_admin(self, parent):
        """Crea el botón de administrador"""
        try:
            admin_frame = tk.Frame(parent, bg=Config.COLORS['white'])
            admin_frame.pack(side='right', padx=(0, 20))
            
            # Botón con icono
            if self.admin_icon:
                admin_btn = tk.Label(
                    admin_frame,
                    image=self.admin_icon,
                    bg=Config.COLORS['white'],
                    cursor="hand2",
                    relief="flat",
                    borderwidth=0
                )
            else:
                # Botón de texto si no hay icono
                admin_btn = tk.Label(
                    admin_frame,
                    text="👤+",
                    font=Config.FONTS['text'],
                    bg=Config.COLORS['white'],
                    fg=Config.COLORS['primary'],
                    cursor="hand2",
                    relief="flat",
                    borderwidth=1,
                    padx=8,
                    pady=4
                )
            
            admin_btn.pack()
            
            # Efectos hover
            def on_enter(e):
                admin_btn.config(bg="#F0F0F0")
            
            def on_leave(e):
                admin_btn.config(bg=Config.COLORS['white'])
            
            def on_click(e):
                self.abrir_dialogo_admin()
            
            admin_btn.bind("<Enter>", on_enter)
            admin_btn.bind("<Leave>", on_leave)
            admin_btn.bind("<Button-1>", on_click)
            
            # Tooltip
            self.crear_tooltip(admin_btn, "Agregar nuevo usuario")
            
            # Etiqueta descriptiva
            tk.Label(
                admin_frame,
                text="Agregar Usuario",
                font=Config.FONTS['text_tiny'],
                bg=Config.COLORS['white'],
                fg=Config.COLORS['text_light']
            ).pack(pady=(2, 0))
            
            self.logger.info("Botón de administrador creado")
            
        except Exception as e:
            self.logger.error(f"Error al crear botón admin: {e}")

    def crear_tooltip(self, widget, text):
        """Crea un tooltip para el widget"""
        def mostrar_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            tooltip.configure(bg="#FFFFE0")
            
            label = tk.Label(
                tooltip, 
                text=text, 
                background="#FFFFE0", 
                relief="solid", 
                borderwidth=1,
                font=Config.FONTS['text_tiny'],
                padx=8,
                pady=4
            )
            label.pack()
            
            # Auto-ocultar después de 3 segundos
            tooltip.after(3000, tooltip.destroy)
        
        widget.bind("<Enter>", mostrar_tooltip)

    def abrir_dialogo_admin(self):
        """Abre el diálogo para agregar un nuevo usuario"""
        try:
            # Importar aquí para evitar dependencias circulares
            from login import RegistroVentana
            
            # Crear la ventana de registro
            RegistroVentana(self.master)
            
            self.logger.info("Diálogo de registro de usuario abierto")
            
        except Exception as e:
            self.logger.error(f"Error al abrir diálogo de admin: {e}")
            messagebox.showerror("Error", f"No se pudo abrir el diálogo de registro:\n{e}")

    def crear_titulo_principal(self, parent):
        """Crea el título principal"""
        title_frame = tk.Frame(parent, bg=Config.COLORS['white'])
        title_frame.pack(fill='x', padx=25, pady=(18, 8))
        
        tk.Label(
            title_frame, 
            text="Sistema de Cálculos Eléctricos", 
            font=Config.FONTS['title'], 
            bg=Config.COLORS['white'], 
            fg=Config.COLORS['text_primary']
        ).pack()
        
        tk.Label(
            title_frame, 
            text="Selecciona una opción para continuar con tus cálculos", 
            font=Config.FONTS['text'], 
            bg=Config.COLORS['white'], 
            fg=Config.COLORS['text_secondary']
        ).pack(pady=(5, 0))

    def crear_separador(self, parent):
        """Crea un separador con estilo Hertz"""
        separator_frame = tk.Frame(parent, bg=Config.COLORS['white'])
        separator_frame.pack(fill='x', padx=30, pady=20)
        
        # Línea naranja
        tk.Frame(separator_frame, bg=Config.COLORS['primary'], height=3).pack(fill='x')

    def crear_botones_principales(self, parent):
        """Crea los botones principales"""
        buttons_frame = tk.Frame(parent, bg=Config.COLORS['white'])
        buttons_frame.pack(fill='both', expand=True, padx=40, pady=10)
        
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
        
        for config in botones_config:
            self.crear_boton_hertz(buttons_frame, config)
        
        # Espacio antes del botón de salir
        tk.Frame(buttons_frame, bg=Config.COLORS['white'], height=15).pack()
        
        # Botón de salir
        exit_btn = ttk.Button(
            buttons_frame, 
            text="🚪 Salir del Sistema", 
            command=self.confirmar_salida,
            style='Exit.TButton'
        )
        exit_btn.pack(fill='x', padx=20)

    def crear_boton_hertz(self, parent, config):
        """Crea un botón con estilo Hertz"""
        button_frame = tk.Frame(parent, bg=Config.COLORS['white'])
        button_frame.pack(fill='x', pady=6, padx=20)
        
        # Botón principal
        btn = ttk.Button(
            button_frame, 
            text=config['text'], 
            command=config['command'],
            style='Hertz.TButton'
        )
        btn.pack(fill='x')
        
        # Descripción
        tk.Label(
            button_frame, 
            text=config['description'], 
            font=Config.FONTS['text_tiny'], 
            bg=Config.COLORS['white'], 
            fg=Config.COLORS['text_light']
        ).pack(pady=(4, 0))

    def crear_footer(self, parent):
        """Crea el footer"""
        footer_frame = tk.Frame(parent, bg=Config.COLORS['white'])
        footer_frame.pack(fill='x', side='bottom', padx=30, pady=(20, 20))
        
        # Separador sutil
        tk.Frame(footer_frame, bg=Config.COLORS['separator'], height=1).pack(fill='x', pady=(0, 15))
        
        # Información del desarrollador
        tk.Label(
            footer_frame, 
            text="Desarrollado por Jessica Zagal Mercado • Residencia Profesional 2025", 
            font=Config.FONTS['text_tiny'], 
            bg=Config.COLORS['white'], 
            fg=Config.COLORS['text_light']
        ).pack()
        
        tk.Label(
            footer_frame, 
            text="Hertz Ingeniería & Servicios Eléctricos • Versión 1.0", 
            font=Config.FONTS['footer'], 
            bg=Config.COLORS['white'], 
            fg='#999999'
        ).pack(pady=(2, 0))

    def confirmar_salida(self):
        """Confirma la salida del sistema"""
        resultado = messagebox.askyesno(
            "Confirmar Salida", 
            "¿Está seguro que desea salir del sistema?",
            icon='question'
        )
        if resultado:
            self.limpiar_recursos()
            self.master.quit()

    def limpiar_recursos(self):
        """Limpia los recursos antes de cerrar"""
        try:
            if hasattr(self, 'fondo_image') and self.fondo_image:
                del self.fondo_image
            if hasattr(self, 'logo_image') and self.logo_image:
                del self.logo_image
            if hasattr(self, 'icon_user') and self.icon_user:
                del self.icon_user
            if hasattr(self, 'admin_icon') and self.admin_icon:
                del self.admin_icon
            self.logger.info("Recursos limpiados correctamente")
        except Exception as e:
            self.logger.error(f"Error al limpiar recursos: {e}")

    def abrir_calculos(self):
        """Abre la pantalla de cálculos en una ventana hija y oculta el menú."""
        try:
            # 1) Oculta el menú principal
            self.master.withdraw()

            # 2) Crea una ventana hija (Toplevel)
            calc_win = tk.Toplevel(self.master)
            calc_win.title("Cálculos Eléctricos - Hertz")
            calc_win.geometry("800x600")
            calc_win.resizable(False, False)

            # 3) Intenta importar y crear la ventana de cálculos
            try:
                from calculosint import Calculos
                
                # Verificar que la clase existe y es válida
                if not hasattr(Calculos, '__init__'):
                    raise AttributeError("La clase Calculos no tiene un constructor válido")
                
                # Instanciar la pantalla de cálculos
                Calculos(calc_win)
                self.logger.info("Módulo de cálculos cargado correctamente")
                
            except ImportError as e:
                self.logger.error(f"No se pudo importar el módulo calculosint: {e}")
                messagebox.showerror(
                    "Módulo no encontrado",
                    "No se pudo cargar el módulo de cálculos.\n"
                    "Verifique que 'calculosint.py' existe en el directorio del proyecto."
                )
                calc_win.destroy()
                self.master.deiconify()
                return
                
            except AttributeError as e:
                self.logger.error(f"Error en la clase Calculos: {e}")
                messagebox.showerror(
                    "Error en el módulo",
                    f"Error al cargar la clase de cálculos: {str(e)}"
                )
                calc_win.destroy()
                self.master.deiconify()
                return
                
            except Exception as e:
                self.logger.error(f"Error inesperado al cargar cálculos: {e}")
                messagebox.showerror(
                    "Error inesperado",
                    f"Error al abrir la ventana de cálculos: {str(e)}"
                )
                calc_win.destroy()
                self.master.deiconify()
                return

            # 4) Configurar el comportamiento al cerrar la ventana hija
            def _cerrar_calculos():
                calc_win.destroy()
                self.master.deiconify()
                self.logger.info("Ventana de cálculos cerrada")

            calc_win.protocol("WM_DELETE_WINDOW", _cerrar_calculos)
            
        except Exception as e:
            self.logger.error(f"Error general al abrir cálculos: {e}")
            messagebox.showerror("Error", f"Error al abrir la ventana de cálculos: {str(e)}")
            if hasattr(self, 'master'):
                self.master.deiconify()

    def abrir_historial(self):
        """Abre la ventana de historial"""
        try:
            historial_window = tk.Toplevel(self.master)
            historial_window.title("Historial de Cargas - Hertz")
            historial_window.geometry("600x400")
            historial_window.configure(bg=Config.COLORS['white'])
            historial_window.resizable(False, False)
            
            # Centrar ventana
            historial_window.transient(self.master)
            historial_window.grab_set()
            
            # Contenido
            frame = tk.Frame(historial_window, bg=Config.COLORS['white'])
            frame.pack(fill='both', expand=True, padx=30, pady=30)
            
            # Header con línea naranja
            header_frame = tk.Frame(frame, bg=Config.COLORS['white'])
            header_frame.pack(fill='x', pady=(0, 20))
            
            tk.Label(
                header_frame, 
                text="📊 Historial de Cargas", 
                font=Config.FONTS['subtitle'], 
                bg=Config.COLORS['white'], 
                fg=Config.COLORS['text_primary']
            ).pack()
            
            tk.Frame(header_frame, bg=Config.COLORS['primary'], height=3).pack(fill='x', pady=(10, 0))
            
            # Contenido
            tk.Label(
                frame, 
                text="Esta funcionalidad está en desarrollo.\n\n"
                     "Próximamente podrá consultar el historial\n"
                     "de todos los cálculos realizados en el sistema.", 
                font=Config.FONTS['button'], 
                bg=Config.COLORS['white'], 
                fg=Config.COLORS['text_secondary'],
                justify='center'
            ).pack(pady=60)
            
            # Botón cerrar
            ttk.Button(
                frame, 
                text="Cerrar", 
                command=historial_window.destroy,
                style='Hertz.TButton'
            ).pack()
            
            self.logger.info("Ventana de historial abierta")
            
        except Exception as e:
            self.logger.error(f"Error al abrir historial: {e}")
            messagebox.showerror("Error", f"Error al abrir el historial: {str(e)}")

    def abrir_acerca(self):
        """Abre la pantalla de información en una ventana hija y oculta el menú."""
        try:
            # 1) Oculta el menú principal
            self.master.withdraw()

            # 2) Crea una ventana hija (Toplevel)
            info_win = tk.Toplevel(self.master)
            info_win.title("Acerca del Sistema - Hertz")
            info_win.geometry("600x500")
            info_win.resizable(False, False)

            # 3) Intenta importar y crear la ventana de información
            try:
                from informacion import NOMElectricalInterface
                
                # Verificar que la clase existe y es válida
                if not hasattr(NOMElectricalInterface, '__init__'):
                    raise AttributeError("La clase Informacion no tiene un constructor válido")
                
                # Instanciar la pantalla de información
                NOMElectricalInterface(info_win)
                self.logger.info("Módulo de información cargado correctamente")
                
            except ImportError as e:
                self.logger.error(f"No se pudo importar el módulo informacion: {e}")
                messagebox.showerror(
                    "Módulo no encontrado",
                    "No se pudo cargar el módulo de información.\n"
                    "Verifique que 'informacion.py' existe en el directorio del proyecto."
                )
                info_win.destroy()
                self.master.deiconify()
                return
                
            except AttributeError as e:
                self.logger.error(f"Error en la clase Informacion: {e}")
                messagebox.showerror(
                    "Error en el módulo",
                    f"Error al cargar la clase de información: {str(e)}"
                )
                info_win.destroy()
                self.master.deiconify()
                return
                
            except Exception as e:
                self.logger.error(f"Error inesperado al cargar información: {e}")
                messagebox.showerror(
                    "Error inesperado",
                    f"Error al abrir la ventana de información: {str(e)}"
                )
                info_win.destroy()
                self.master.deiconify()
                return

            # 4) Configurar el comportamiento al cerrar la ventana hija
            def _cerrar_informacion():
                info_win.destroy()
                self.master.deiconify()
                self.logger.info("Ventana de información cerrada")

            info_win.protocol("WM_DELETE_WINDOW", _cerrar_informacion)
            
        except Exception as e:
            self.logger.error(f"Error general al abrir información: {e}")
            messagebox.showerror("Error", f"Error al abrir la ventana de información: {str(e)}")
            if hasattr(self, 'master'):
                self.master.deiconify()

    def actualizar_interfaz_usuario(self):
        """Actualiza la interfaz después de recibir los datos del usuario"""
        print(f"🔧 Actualizando interfaz. is_admin = {self.is_admin}")
        
        # Encontrar el frame principal y recrear su contenido
        canvas_items = self.canvas.find_all()
        
        for item in canvas_items:
            if self.canvas.type(item) == "window":
                try:
                    window_widget_name = self.canvas.itemcget(item, "window")
                    if window_widget_name:
                        main_frame = self.master.nametowidget(window_widget_name)
                        
                        # Limpiar contenido actual
                        for child in main_frame.winfo_children():
                            child.destroy()
                        
                        # Recrear contenido con datos del usuario
                        self.crear_contenido(main_frame)
                        print(f"✅ Interfaz actualizada. Botón admin debería aparecer: {self.is_admin}")
                        break
                except Exception as e:
                    print(f"Error al actualizar interfaz: {e}")
                    continue

    def __del__(self):
        """Destructor para limpiar recursos"""
        self.limpiar_recursos()


def main():
    """Función principal para ejecutar la aplicación"""
    try:
        root = tk.Tk()
        app = MenuPrincipal(root)
        root.mainloop()
    except Exception as e:
        logging.error(f"Error crítico en la aplicación: {e}")
        messagebox.showerror("Error Crítico", f"Error al iniciar la aplicación: {str(e)}")


if __name__ == "__main__":
    main()