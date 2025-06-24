import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from supabase_client import supabase  # asegúrate que este archivo exista
from menuprincipal import MenuPrincipal  # se importa cuando logea exitosamente
import bcrypt
import re
import os


class LoginVentana:
    def __init__(self, master):
        self.master = master
        self.master.title("Inicio de Sesión - Hertz")
        self.master.geometry("500x650")
        self.master.resizable(False, False)
        self.master.configure(bg='#F5F5F5')
        
        # Variables para imágenes
        self.fondo_image = None
        self.logo_image = None
        
        # Usuario logueado y datos completos
        self.usuario_logueado = None
        self.datos_usuario = None
        self.is_admin = False
        
        # Centrar ventana
        self.centrar_ventana()
        
        # Configurar estilos
        self.configurar_estilos()
        
        # Cargar imágenes
        self.cargar_imagenes()
        
        # Crear interfaz
        self.crear_interfaz()

    def centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        self.master.update_idletasks()
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        y = (self.master.winfo_screenheight() // 2) - (height // 2)
        self.master.geometry(f'{width}x{height}+{x}+{y}')

    def cargar_imagenes(self):
        """Carga las imágenes del logo y fondo usando rutas relativas seguras"""
        base_path = os.path.dirname(os.path.abspath(__file__))

        try:
            fondo_path = os.path.join(base_path, "Imagenes", "fondo.jpeg")
            imagen_fondo = Image.open(fondo_path).resize((800, 600), Image.Resampling.LANCZOS)
            self.fondo_image = ImageTk.PhotoImage(imagen_fondo)
            print("Fondo cargado exitosamente desde:", fondo_path)
        except Exception as e:
            print(f"Error al cargar fondo ({fondo_path}): {e}")
            self.fondo_image = None

        try:
            logo_path = os.path.join(base_path, "Imagenes", "logo.png")
            imagen_logo = Image.open(logo_path)
            imagen_logo.thumbnail((150, 80), Image.Resampling.LANCZOS)
            self.logo_image = ImageTk.PhotoImage(imagen_logo)
            print("Logo cargado exitosamente desde:", logo_path)
        except Exception as e:
            print(f"Error al cargar logo ({logo_path}): {e}")
            self.logo_image = None

    def configurar_estilos(self):
        """Configura los estilos personalizados con paleta Hertz"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Colores Hertz
        color_naranja = '#E85A2B'
        color_naranja_hover = '#F26B3A'
        color_naranja_pressed = '#D44B22'
        color_gris_oscuro = '#2C2C2C'
        color_gris_medio = '#4A4A4A'
        
        # Estilo para botón principal de login
        self.style.configure('Login.TButton',
                           background=color_naranja,
                           foreground='white',
                           font=('Segoe UI', 12, 'bold'),
                           borderwidth=0,
                           focuscolor='none',
                           padding=(20, 12))
        
        self.style.map('Login.TButton',
                      background=[('active', color_naranja_hover),
                                ('pressed', color_naranja_pressed)])
        
        # Estilo para botón secundario
        self.style.configure('Secondary.TButton',
                           background=color_gris_medio,
                           foreground='white',
                           font=('Segoe UI', 10, 'bold'),
                           borderwidth=0,
                           focuscolor='none',
                           padding=(15, 8))
        
        self.style.map('Secondary.TButton',
                      background=[('active', '#5A5A5A'),
                                ('pressed', '#3A3A3A')])
        
        # Estilo para campos de entrada
        self.style.configure('Login.TEntry',
                           fieldbackground='white',
                           borderwidth=2,
                           relief='solid',
                           padding=10,
                           font=('Segoe UI', 11))

    def crear_interfaz(self):
        """Crea la interfaz principal de login"""
        # Canvas para el fondo
        self.canvas = tk.Canvas(self.master, width=500, height=650, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Establecer fondo
        if self.fondo_image:
            self.canvas.create_image(0, 0, image=self.fondo_image, anchor="nw")
        else:
            self.canvas.configure(bg='#F5F5F5')
        
        # Frame principal de login
        self.login_frame = tk.Frame(self.canvas, bg='white', relief='solid', bd=1)
        self.canvas.create_window(250, 325, window=self.login_frame, width=400, height=500)
        
        # Crear contenido del login
        self.crear_contenido_login()

    def crear_contenido_login(self):
        """Crea el contenido del formulario de login"""
        # Header con logo
        self.crear_header_login()
        
        # Título
        self.crear_titulo_login()
        
        # Separador
        self.crear_separador_login()
        
        # Formulario
        self.crear_formulario_login()
        
        # Botones
        self.crear_botones_login()
        
        # Footer
        self.crear_footer_login()

    def crear_header_login(self):
        """Crea el header del login con logo"""
        header_frame = tk.Frame(self.login_frame, bg='white', height=100)
        header_frame.pack(fill='x', pady=(20, 10))
        header_frame.pack_propagate(False)
        
        if self.logo_image:
            logo_label = tk.Label(header_frame, image=self.logo_image, bg='white')
            logo_label.pack()
        else:
            # Texto de respaldo
            tk.Label(header_frame, 
                    text="HERTZ", 
                    font=('Segoe UI', 24, 'bold'), 
                    bg='white', 
                    fg='#E85A2B').pack(pady=10)
            
            tk.Label(header_frame, 
                    text="Ingeniería & Servicios Eléctricos", 
                    font=('Segoe UI', 10), 
                    bg='white', 
                    fg='#E85A2B').pack()

    def crear_titulo_login(self):
        """Crea el título del login"""
        title_frame = tk.Frame(self.login_frame, bg='white')
        title_frame.pack(fill='x', pady=(10, 5))
        
        tk.Label(title_frame, 
                text="Inicio de Sesión", 
                font=('Segoe UI', 18, 'bold'), 
                bg='white', 
                fg='#2C2C2C').pack()
        
        tk.Label(title_frame, 
                text="Sistema de Cálculos Eléctricos", 
                font=('Segoe UI', 11), 
                bg='white', 
                fg='#4A4A4A').pack(pady=(2, 0))

    def crear_separador_login(self):
        """Crea separador con estilo Hertz"""
        separator_frame = tk.Frame(self.login_frame, bg='white')
        separator_frame.pack(fill='x', padx=40, pady=15)
        
        tk.Frame(separator_frame, bg='#E85A2B', height=2).pack(fill='x')

    def crear_formulario_login(self):
        """Crea el formulario de login"""
        form_frame = tk.Frame(self.login_frame, bg='white')
        form_frame.pack(fill='x', padx=40, pady=20)
        
        # Campo Usuario
        tk.Label(form_frame, 
                text="Usuario:", 
                font=('Segoe UI', 11, 'bold'), 
                bg='white', 
                fg='#2C2C2C').pack(anchor='w', pady=(0, 5))
        
        self.usuario_entry = ttk.Entry(form_frame, style='Login.TEntry', font=('Segoe UI', 11))
        self.usuario_entry.pack(fill='x', pady=(0, 15))
        self.usuario_entry.focus()  # Foco inicial
        
        # Campo Contraseña
        tk.Label(form_frame, 
                text="Contraseña:", 
                font=('Segoe UI', 11, 'bold'), 
                bg='white', 
                fg='#2C2C2C').pack(anchor='w', pady=(0, 5))
        
        self.clave_entry = ttk.Entry(form_frame, show="*", style='Login.TEntry', font=('Segoe UI', 11))
        self.clave_entry.pack(fill='x', pady=(0, 10))
        
        # Bind Enter key para login rápido
        self.usuario_entry.bind('<Return>', lambda e: self.clave_entry.focus())
        self.clave_entry.bind('<Return>', lambda e: self.iniciar_sesion())

    def crear_botones_login(self):
        """Crea los botones del login"""
        buttons_frame = tk.Frame(self.login_frame, bg='white')
        buttons_frame.pack(fill='x', padx=40, pady=20)
        
        # Botón Iniciar Sesión
        self.login_button = ttk.Button(buttons_frame, 
                                      text="🔐 Iniciar Sesión", 
                                      command=self.iniciar_sesion,
                                      style='Login.TButton')
        self.login_button.pack(fill='x', pady=(0, 10))
        
        # Botón Agregar Usuario (oculto por defecto)
        self.boton_registro = ttk.Button(buttons_frame, 
                                        text="👤 Agregar Usuario", 
                                        command=self.abrir_registro,
                                        style='Secondary.TButton')
        # Ocultarlo por defecto
        self.boton_registro.pack(fill='x')
        self.boton_registro.pack_forget()

    def crear_footer_login(self):
        """Crea el footer del login"""
        footer_frame = tk.Frame(self.login_frame, bg='white')
        footer_frame.pack(fill='x', side='bottom', padx=30, pady=20)
        
        # Línea separadora
        tk.Frame(footer_frame, bg='#E0E0E0', height=1).pack(fill='x', pady=(0, 10))
        
        tk.Label(footer_frame, 
                text="NOM-001-SEDE-2012", 
                font=('Segoe UI', 9, 'bold'), 
                bg='white', 
                fg='#666666').pack()
        
        tk.Label(footer_frame, 
                text="Hertz Ingeniería & Servicios Eléctricos", 
                font=('Segoe UI', 8), 
                bg='white', 
                fg='#999999').pack(pady=(2, 0))

    def iniciar_sesion(self):
        """Maneja el inicio de sesión con bcrypt y detección de admin"""
        usuario = self.usuario_entry.get().strip()
        clave = self.clave_entry.get().strip()
        
        if not usuario or not clave:
            messagebox.showwarning("Campos vacíos", "Por favor, complete todos los campos.")
            return

        # Mostrar indicador de carga
        self.mostrar_carga(True)

        try:
            # Buscar el usuario en la tabla
            response = supabase.table("usuarios").select("*").eq("usuario", usuario).execute()

            if not response.data:
                messagebox.showerror("❌ Error de Acceso", 
                                   "Usuario no encontrado.\nVerifique sus credenciales.")
                self.clave_entry.delete(0, tk.END)
                self.clave_entry.focus()
                return

            user_data = response.data[0]
            
            # Verificar contraseña (soporta tanto bcrypt como texto plano para transición)
            clave_bd = user_data["clave"]
            password_valid = False
            
            try:
                # Intentar verificar con bcrypt primero
                if clave_bd.startswith('$2b$') or clave_bd.startswith('$2a$'):
                    password_valid = bcrypt.checkpw(clave.encode('utf-8'), clave_bd.encode('utf-8'))
                    print("✅ Contraseña verificada con bcrypt")
                else:
                    # Fallback a texto plano (para compatibilidad temporal)
                    password_valid = (clave == clave_bd)
                    print("⚠️ ADVERTENCIA: Contraseña en texto plano detectada")
            except Exception as e:
                print(f"Error al verificar contraseña con bcrypt: {e}")
                # Fallback a comparación directa
                password_valid = (clave == clave_bd)

            if password_valid:
                # Guardar datos del usuario
                self.usuario_logueado = usuario
                self.datos_usuario = user_data
                self.is_admin = (user_data["rol"] == "admin")
                
                # Mensaje de bienvenida
                nombre_completo = user_data.get('nombre', usuario)
                if user_data.get('apellidos'):
                    nombre_completo += f" {user_data['apellidos']}"
                
                rol_display = "Administrador" if self.is_admin else "Usuario"
                messagebox.showinfo("✅ Acceso Concedido", 
                                  f"Bienvenido {nombre_completo}\nRol: {rol_display}")

                # Si es admin, mostrar botón de registro
                if self.is_admin:
                    self.boton_registro.pack(fill='x', pady=(5, 0))
                    # Ajustar tamaño de la ventana para el botón extra
                    canvas_window = self.canvas.find_all()[1] if len(self.canvas.find_all()) > 1 else None
                    if canvas_window:
                        self.canvas.itemconfig(canvas_window, height=550)
                
                # Abrir menú principal después de un breve delay
                self.master.after(1500, self.abrir_menu_principal)
                
            else:
                messagebox.showerror("❌ Error de Acceso", 
                                   "Usuario o contraseña incorrectos.\nVerifique sus credenciales.")
                self.clave_entry.delete(0, tk.END)
                self.clave_entry.focus()
                
        except Exception as e:
            messagebox.showerror("❌ Error de Conexión", 
                               f"No se pudo conectar al sistema.\nVerifique su conexión e intente nuevamente.\n\nError: {str(e)}")
            print(f"Error de login: {e}")
        
        finally:
            self.mostrar_carga(False)

    def mostrar_carga(self, mostrar):
        """Muestra/oculta indicador de carga"""
        if mostrar:
            self.login_button.config(text="⏳ Verificando...")
            self.login_button.config(state='disabled')
            self.master.config(cursor="wait")
            self.master.update()
        else:
            self.login_button.config(text="🔐 Iniciar Sesión")
            self.login_button.config(state='normal')
            self.master.config(cursor="")

    def abrir_menu_principal(self):
            """Abre el menú principal pasando los datos del usuario"""
            # Debug: Verificar datos antes de pasar al menú
            print(f"🔍 DEBUG - Usuario logueado: {self.usuario_logueado}")
            print(f"🔍 DEBUG - Es admin: {self.is_admin}")
            print(f"🔍 DEBUG - Datos usuario completos: {self.datos_usuario}")
            
            self.master.destroy()
            root = tk.Tk()
            
            # Crear el menú principal
            menu = MenuPrincipal(root)
            
            # IMPORTANTE: Pasar los datos del usuario al menú principal
            menu.usuario_logueado = self.usuario_logueado
            menu.datos_usuario = self.datos_usuario
            menu.is_admin = self.is_admin
            
            # Debug: Verificar que se asignó correctamente en el menú
            print(f"🔍 DEBUG - Menu.is_admin después de asignar: {menu.is_admin}")
            
            # NUEVO: Actualizar la interfaz con los datos del usuario
            menu.actualizar_interfaz_usuario()
            
            # Actualizar el título de la ventana con el nombre del usuario
            if self.datos_usuario and self.datos_usuario.get('nombre'):
                nombre_display = self.datos_usuario['nombre']
                if self.datos_usuario.get('apellidos'):
                    nombre_display += f" {self.datos_usuario['apellidos']}"
            else:
                nombre_display = self.usuario_logueado
            
            root.title(f"Sistema de Cálculos Eléctricos - Usuario: {nombre_display}")
            
            print(f"🔍 DEBUG - Abriendo MenuPrincipal...")
            
            root.mainloop()

    def abrir_registro(self):
        """Abre la ventana de registro"""
        RegistroVentana(self.master)

class RegistroVentana:
    def __init__(self, parent):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Registro de Usuario - Hertz")
        self.ventana.geometry("520x400")  # Ventana AÚN más pequeña
        self.ventana.resizable(False, False)
        self.ventana.configure(bg='white')
        
        # Centrar ventana
        self.centrar_ventana()
        
        # Configurar estilos
        self.configurar_estilos()
        
        # Hacer modal
        self.ventana.transient(parent)
        self.ventana.grab_set()
        
        # Crear interfaz con scroll
        self.crear_interfaz_registro()

    def centrar_ventana(self):
        """Centra la ventana de registro"""
        self.ventana.update_idletasks()
        width = self.ventana.winfo_width()
        height = self.ventana.winfo_height()
        x = (self.ventana.winfo_screenwidth() // 2) - (width // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (height // 2)
        self.ventana.geometry(f'{width}x{height}+{x}+{y}')

    def configurar_estilos(self):
        """Configura estilos para la ventana de registro"""
        self.style = ttk.Style()
        
        # Estilo para campos de entrada
        self.style.configure('Registro.TEntry',
                           fieldbackground='#F8F9FA',
                           borderwidth=2,
                           relief='solid',
                           padding=8,
                           font=('Segoe UI', 10))

    def crear_interfaz_registro(self):
        """Crea la interfaz de registro con scroll y botones fijos"""
        
        # Frame principal que contendrá todo
        main_container = tk.Frame(self.ventana, bg='white')
        main_container.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Frame para el área de scroll (parte superior)
        scroll_container = tk.Frame(main_container, bg='white')
        scroll_container.pack(fill='both', expand=True)
        
        # Canvas para el contenido con scroll
        self.canvas = tk.Canvas(
            scroll_container, 
            bg='white', 
            highlightthickness=0,
            height=280  # Altura mucho más pequeña
        )
        
        # Scrollbar vertical (siempre visible)
        scrollbar = ttk.Scrollbar(scroll_container, orient="vertical", command=self.canvas.yview)
        
        # Frame que contendrá el contenido desplazable
        self.scrollable_frame = tk.Frame(self.canvas, bg='white')
        
        # Configurar el scroll
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        # Crear ventana en el canvas
        canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Configurar el ancho del contenido para que se ajuste al canvas
        def configure_canvas_width(event):
            canvas_width = event.width - scrollbar.winfo_reqwidth()
            self.canvas.itemconfig(canvas_window, width=canvas_width)
        
        self.canvas.bind('<Configure>', configure_canvas_width)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar canvas y scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Crear contenido dentro del frame desplazable (SIN los botones)
        self.crear_contenido_formulario()
        
        # NUEVO: Frame fijo para botones en la parte inferior
        self.crear_botones_fijos(main_container)
        
        # Bind para scroll con rueda del mouse
        self.bind_scroll_events()
        
        # Actualizar scroll después de crear contenido
        self.ventana.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def bind_scroll_events(self):
        """Configura el scroll con la rueda del mouse"""
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_to_mousewheel(event):
            self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        def _unbind_from_mousewheel(event):
            self.canvas.unbind_all("<MouseWheel>")
        
        # Bind cuando el mouse entra y sale de la ventana
        self.canvas.bind('<Enter>', _bind_to_mousewheel)
        self.canvas.bind('<Leave>', _unbind_from_mousewheel)

    def crear_contenido_formulario(self):
        """Crea el contenido del formulario dentro del frame desplazable"""
        
        # Header
        header_frame = tk.Frame(self.scrollable_frame, bg='white')
        header_frame.pack(fill='x', pady=(20, 0), padx=20)
        
        tk.Label(header_frame, 
                text="👤 Registro de Usuario", 
                font=('Segoe UI', 20, 'bold'), 
                bg='white', 
                fg='#2C2C2C').pack(pady=(10, 5))
        
        tk.Label(header_frame, 
                text="Solo administradores pueden registrar nuevos usuarios", 
                font=('Segoe UI', 10), 
                bg='white', 
                fg='#666666').pack(pady=(0, 10))
        
        # Separador
        separator_frame = tk.Frame(self.scrollable_frame, bg='white')
        separator_frame.pack(fill='x', padx=40, pady=15)
        tk.Frame(separator_frame, bg='#E85A2B', height=3).pack(fill='x')
        
        # Formulario
        form_frame = tk.Frame(self.scrollable_frame, bg='white')
        form_frame.pack(fill='x', padx=40, pady=20)
        
        # Campos del formulario
        campos = [
            ("Nombre de usuario:", "usuario_nuevo", "Ingrese el nombre de usuario único"),
            ("Nombre completo:", "nombre_nuevo", "Ingrese el nombre real del usuario"),
            ("Apellidos:", "apellidos_nuevo", "Ingrese los apellidos del usuario"),
            ("Correo electrónico:", "correo_nuevo", "Ingrese un email válido"),
            ("Contraseña:", "clave_nueva", "Mínimo 8 caracteres"),
            ("Confirmar contraseña:", "clave_confirmar", "Repita la contraseña anterior"),
            ("Rol (admin/user):", "rol_nuevo", "admin = Administrador, user = Usuario estándar")
        ]
        
        for i, (label_text, attr_name, help_text) in enumerate(campos):
            # Frame para cada campo
            field_frame = tk.Frame(form_frame, bg='white')
            field_frame.pack(fill='x', pady=(20 if i > 0 else 0, 0))  # Más espacio entre campos
            
            # Label del campo
            tk.Label(field_frame, 
                    text=label_text, 
                    font=('Segoe UI', 11, 'bold'), 
                    bg='white', 
                    fg='#2C2C2C').pack(anchor='w', pady=(0, 8))
            
            # Entry del campo
            if "clave" in attr_name:
                entry = ttk.Entry(field_frame, show="*", style='Registro.TEntry', font=('Segoe UI', 10))
            else:
                entry = ttk.Entry(field_frame, style='Registro.TEntry', font=('Segoe UI', 10))
            
            entry.pack(fill='x', pady=(0, 5))
            setattr(self, attr_name, entry)
            
            # Texto de ayuda
            tk.Label(field_frame, 
                    text=f"💡 {help_text}", 
                    font=('Segoe UI', 9), 
                    bg='white', 
                    fg='#888888').pack(anchor='w', pady=(0, 10))
        
        # Indicador de fuerza de contraseña
        self.password_strength_frame = tk.Frame(form_frame, bg='white')
        self.password_strength_frame.pack(fill='x', pady=(10, 0))
        
        tk.Label(self.password_strength_frame, 
                text="Fuerza de contraseña:", 
                font=('Segoe UI', 9, 'bold'), 
                bg='white', 
                fg='#2C2C2C').pack(anchor='w')
        
        self.strength_label = tk.Label(self.password_strength_frame, 
                                     text="", 
                                     font=('Segoe UI', 9), 
                                     bg='white')
        self.strength_label.pack(anchor='w')
        
        # Bind para validación en tiempo real
        self.clave_nueva.bind("<KeyRelease>", self.validar_password_strength)
        
        # Espacio final para asegurar que hay contenido suficiente para scroll
        tk.Frame(self.scrollable_frame, bg='white', height=100).pack()  # Más espacio

    def crear_botones_fijos(self, parent):
        """Crea los botones en la parte inferior de la ventana (fijos, no scrolleables)"""
        # Separador
        separator_frame = tk.Frame(parent, bg='white')
        separator_frame.pack(fill='x', pady=(10, 0))
        tk.Frame(separator_frame, bg='#E0E0E0', height=1).pack(fill='x', padx=20)
        
        # Frame para los botones (fijo en la parte inferior)
        buttons_frame = tk.Frame(parent, bg='white')
        buttons_frame.pack(fill='x', padx=40, pady=(15, 20))
        
        self.registro_btn = ttk.Button(buttons_frame, 
                  text="✅ Registrar Usuario", 
                  command=self.registrar_usuario,
                  style='Login.TButton')
        self.registro_btn.pack(fill='x', pady=(0, 10))
        
        ttk.Button(buttons_frame, 
                  text="❌ Cancelar", 
                  command=self.ventana.destroy,
                  style='Secondary.TButton').pack(fill='x')

    def validar_password_strength(self, event=None):
        """Valida la fuerza de la contraseña en tiempo real"""
        password = self.clave_nueva.get()
        
        if len(password) == 0:
            self.strength_label.config(text="", fg="black")
            return
            
        score = 0
        feedback = []
        
        if len(password) >= 8:
            score += 1
        else:
            feedback.append("mínimo 8 caracteres")
            
        if re.search(r"[a-z]", password):
            score += 1
        else:
            feedback.append("letra minúscula")
            
        if re.search(r"[A-Z]", password):
            score += 1
        else:
            feedback.append("letra mayúscula")
            
        if re.search(r"\d", password):
            score += 1
        else:
            feedback.append("número")
            
        if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            score += 1
        else:
            feedback.append("carácter especial")
        
        # Mostrar resultado
        if score < 2:
            self.strength_label.config(text="❌ Débil - Falta: " + ", ".join(feedback[:2]), fg="red")
        elif score < 4:
            self.strength_label.config(text="⚠️ Media - Mejora: " + ", ".join(feedback[:2]), fg="orange")
        else:
            self.strength_label.config(text="✅ Fuerte - Muy segura", fg="green")

    def registrar_usuario(self):
        """Registra un nuevo usuario con bcrypt"""
        # Obtener datos
        user = self.usuario_nuevo.get().strip()
        nombre = self.nombre_nuevo.get().strip()
        apellidos = self.apellidos_nuevo.get().strip()
        correo = self.correo_nuevo.get().strip()
        pwd = self.clave_nueva.get().strip()
        pwd_confirm = self.clave_confirmar.get().strip()
        rol = self.rol_nuevo.get().strip().lower()

        # Validaciones
        if not all([user, nombre, correo, pwd, pwd_confirm, rol]):
            messagebox.showwarning("⚠️ Campos Incompletos", 
                                 "Por favor, complete todos los campos obligatorios.")
            return

        if pwd != pwd_confirm:
            messagebox.showerror("❌ Contraseñas no coinciden", 
                               "Las contraseñas ingresadas no coinciden.")
            self.clave_confirmar.focus()
            return

        if rol not in ["admin", "user"]:
            messagebox.showerror("❌ Rol Inválido", 
                               "El rol debe ser 'admin' o 'user'.")
            self.rol_nuevo.focus()
            return
        
        if len(pwd) < 8:
            messagebox.showwarning("⚠️ Contraseña Débil", 
                                 "La contraseña debe tener al menos 8 caracteres.")
            self.clave_nueva.focus()
            return
        
        # Validación de email mejorada
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', correo):
            messagebox.showwarning("⚠️ Email Inválido", 
                                 "Por favor, ingrese un email válido.")
            self.correo_nuevo.focus()
            return

        # Mostrar indicador de progreso
        self.mostrar_progreso(True)

        try:
            # Verificar si el usuario ya existe
            response = supabase.table("usuarios").select("usuario").eq("usuario", user).execute()
            if response.data:
                messagebox.showerror("❌ Usuario Existente", 
                                   f"El usuario '{user}' ya existe.\nElija otro nombre de usuario.")
                self.usuario_nuevo.focus()
                return
            
            # Verificar si el correo ya existe
            response = supabase.table("usuarios").select("correo").eq("correo", correo).execute()
            if response.data:
                messagebox.showerror("❌ Correo Existente", 
                                   f"El correo '{correo}' ya está registrado.\nUse otro correo electrónico.")
                self.correo_nuevo.focus()
                return
            
            # Hash de la contraseña con bcrypt
            hashed_password = bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # Insertar nuevo usuario
            insert_data = {
                "usuario": user,
                "clave": hashed_password,
                "correo": correo,
                "rol": rol,
                "nombre": nombre,
                "apellidos": apellidos
            }
            
            response = supabase.table("usuarios").insert(insert_data).execute()
            
            if response.data:
                rol_display = "Administrador" if rol == "admin" else "Usuario estándar"
                messagebox.showinfo("✅ Registro Exitoso", 
                                   f"Usuario '{user}' registrado correctamente.\n"
                                   f"Nombre: {nombre} {apellidos}\n"
                                   f"Rol asignado: {rol_display}\n"
                                   f"Contraseña encriptada con bcrypt.")
                self.ventana.destroy()
            else:
                raise Exception("No se recibieron datos en la respuesta")
            
        except Exception as e:
            error_msg = str(e)
            if "duplicate key" in error_msg.lower() or "unique" in error_msg.lower():
                messagebox.showerror("❌ Datos Duplicados", 
                                   "Ya existe un usuario con ese nombre o correo.\n"
                                   "Verifique los datos ingresados.")
            else:
                messagebox.showerror("❌ Error de Registro", 
                                   f"No se pudo registrar el usuario.\n\nDetalle del error:\n{error_msg}")
            print(f"Error en registro: {e}")
        
        finally:
            self.mostrar_progreso(False)

    def mostrar_progreso(self, mostrar):
        """Muestra/oculta indicador de progreso"""
        if mostrar:
            self.registro_btn.config(text="⏳ Registrando...")
            self.registro_btn.config(state='disabled')
            self.ventana.config(cursor="wait")
            self.ventana.update()
        else:
            self.registro_btn.config(text="✅ Registrar Usuario")
            self.registro_btn.config(state='normal')
            self.ventana.config(cursor="")


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginVentana(root)
    root.mainloop()