import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from supabase_client import supabase  # asegúrate que este archivo exista
from menuprincipal import MenuPrincipal  # se importa cuando logea exitosamente
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
        
        # Usuario logueado y su rol
        self.usuario_logueado = None
        self.rol_usuario = None
        
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
        """Maneja el inicio de sesión"""
        usuario = self.usuario_entry.get().strip()
        clave = self.clave_entry.get().strip()
        
        if not usuario or not clave:
            messagebox.showwarning("Campos vacíos", "Por favor, complete todos los campos.")
            return

        try:
            # Buscar el usuario en la tabla
            response = supabase.table("usuarios").select("*").eq("usuario", usuario).execute()

            if not response.data:
                raise Exception("Usuario no encontrado")

            user_data = response.data[0]
            clave_correcta = user_data["clave"]
            rol = user_data["rol"]

            if clave == clave_correcta:
                self.usuario_logueado = usuario
                self.rol_usuario = rol
                
                # Mostrar mensaje de bienvenida
                messagebox.showinfo("✅ Acceso Concedido", 
                                  f"Bienvenido {usuario}\nRol: {rol.upper()}")

                # Si el usuario es admin, mostrar el botón para agregar usuarios
                if rol == "admin":
                    self.boton_registro.pack(fill='x', pady=(5, 0))
                    self.login_frame.configure(height=550)  # Hacer frame más grande
                
                # Abrir menú principal después de un breve delay
                self.master.after(1000, self.abrir_menu_principal)
                
            else:
                messagebox.showerror("❌ Error de Acceso", 
                                   "Usuario o contraseña incorrectos.\nVerifique sus credenciales.")
                self.clave_entry.delete(0, tk.END)
                self.clave_entry.focus()
                
        except Exception as e:
            messagebox.showerror("❌ Error de Conexión", 
                               "No se pudo conectar al sistema.\nVerifique su conexión e intente nuevamente.")
            print(f"Error de login: {e}")

    def abrir_menu_principal(self):
        """Abre el menú principal"""
        self.master.destroy()
        root = tk.Tk()
        MenuPrincipal(root)
        root.mainloop()

    def abrir_registro(self):
        """Abre la ventana de registro"""
        RegistroVentana(self.master)


class RegistroVentana:
    def __init__(self, parent):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Registro de Usuario - Hertz")
        self.ventana.geometry("450x500")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg='white')
        
        # Centrar ventana
        self.centrar_ventana()
        
        # Configurar estilos
        self.configurar_estilos()
        
        # Hacer modal
        self.ventana.transient(parent)
        self.ventana.grab_set()
        
        # Crear interfaz
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
        """Crea la interfaz de registro"""
        # Header
        header_frame = tk.Frame(self.ventana, bg='white', height=80)
        header_frame.pack(fill='x', pady=(20, 0))
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, 
                text="👤 Registro de Usuario", 
                font=('Segoe UI', 18, 'bold'), 
                bg='white', 
                fg='#2C2C2C').pack(pady=10)
        
        tk.Label(header_frame, 
                text="Solo administradores pueden registrar nuevos usuarios", 
                font=('Segoe UI', 9), 
                bg='white', 
                fg='#666666').pack()
        
        # Separador
        separator_frame = tk.Frame(self.ventana, bg='white')
        separator_frame.pack(fill='x', padx=40, pady=15)
        tk.Frame(separator_frame, bg='#E85A2B', height=2).pack(fill='x')
        
        # Formulario
        form_frame = tk.Frame(self.ventana, bg='white')
        form_frame.pack(fill='both', expand=True, padx=40, pady=20)
        
        # Campos del formulario
        campos = [
            ("Nombre de usuario:", "usuario_nuevo"),
            ("Correo electrónico:", "correo_nuevo"),
            ("Contraseña:", "clave_nueva"),
            ("Rol (admin/usuario):", "rol_nuevo")
        ]
        
        for i, (label_text, attr_name) in enumerate(campos):
            tk.Label(form_frame, 
                    text=label_text, 
                    font=('Segoe UI', 10, 'bold'), 
                    bg='white', 
                    fg='#2C2C2C').pack(anchor='w', pady=(10 if i > 0 else 0, 5))
            
            if attr_name == "clave_nueva":
                entry = ttk.Entry(form_frame, show="*", style='Registro.TEntry')
            else:
                entry = ttk.Entry(form_frame, style='Registro.TEntry')
            
            entry.pack(fill='x', pady=(0, 5))
            setattr(self, attr_name, entry)
        
        # Ayuda para el campo rol
        tk.Label(form_frame, 
                text="💡 Escriba 'admin' para administrador o 'usuario' para usuario estándar", 
                font=('Segoe UI', 8), 
                bg='white', 
                fg='#666666',
                wraplength=350).pack(anchor='w', pady=(0, 15))
        
        # Botones
        buttons_frame = tk.Frame(form_frame, bg='white')
        buttons_frame.pack(fill='x', pady=20)
        
        ttk.Button(buttons_frame, 
                  text="✅ Registrar Usuario", 
                  command=self.registrar_usuario,
                  style='Login.TButton').pack(fill='x', pady=(0, 10))
        
        ttk.Button(buttons_frame, 
                  text="❌ Cancelar", 
                  command=self.ventana.destroy,
                  style='Secondary.TButton').pack(fill='x')

    def registrar_usuario(self):
        """Registra un nuevo usuario"""
        user = self.usuario_nuevo.get().strip()
        correo = self.correo_nuevo.get().strip()
        pwd = self.clave_nueva.get().strip()
        rol = self.rol_nuevo.get().strip().lower()

        # Validaciones
        if not all([user, correo, pwd, rol]):
            messagebox.showwarning("⚠️ Campos Incompletos", 
                                 "Por favor, complete todos los campos.")
            return

        if rol not in ["admin", "usuario"]:
            messagebox.showerror("❌ Rol Inválido", 
                               "El rol debe ser 'admin' o 'usuario'.")
            self.rol_nuevo.focus()
            return
        
        if len(pwd) < 6:
            messagebox.showwarning("⚠️ Contraseña Débil", 
                                 "La contraseña debe tener al menos 6 caracteres.")
            self.clave_nueva.focus()
            return
        
        if "@" not in correo:
            messagebox.showwarning("⚠️ Email Inválido", 
                                 "Por favor, ingrese un email válido.")
            self.correo_nuevo.focus()
            return

        try:
            # Verificar si el usuario ya existe
            response = supabase.table("usuarios").select("usuario").eq("usuario", user).execute()
            if response.data:
                messagebox.showerror("❌ Usuario Existente", 
                                   f"El usuario '{user}' ya existe.\nElija otro nombre de usuario.")
                self.usuario_nuevo.focus()
                return
            
            # Insertar nuevo usuario
            supabase.table("usuarios").insert({
                "usuario": user,
                "clave": pwd,
                "correo": correo,
                "rol": rol
            }).execute()
            
            messagebox.showinfo("✅ Registro Exitoso", 
                               f"Usuario '{user}' registrado correctamente.\nRol asignado: {rol.upper()}")
            self.ventana.destroy()
            
        except Exception as e:
            messagebox.showerror("❌ Error de Registro", 
                               f"No se pudo registrar el usuario.\n\nDetalle del error:\n{e}")
            print(f"Error en registro: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginVentana(root)
    root.mainloop()