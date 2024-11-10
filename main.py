import tkinter as tk  # Importa la librería tkinter para crear interfaces gráficas de usuario (GUI).
from tkinter import messagebox  # Importa la funcionalidad para mostrar mensajes emergentes (informativos, de error, etc.).
from tkinter import ttk  # Importa la librería de widgets themed (más modernos) de tkinter, para crear botones, etiquetas, etc.
from PIL import Image, ImageTk  # Importa la librería Pillow para manipular imágenes, incluida su redimensión y uso en tkinter.
from db_connection import conectar  # Importa la función conectar desde el módulo db_connection para realizar la conexión con la base de datos.
from image_capture import capturar_imagen  # Importa la función capturar_imagen desde el módulo image_capture para capturar imágenes (fotografías de usuario).
from auth_logic import registrar_usuario  # Importa la función registrar_usuario desde el módulo auth_logic para registrar nuevos usuarios en la base de datos.
import subprocess  # Importa el módulo subprocess para ejecutar otros programas o scripts desde el código Python actual.

def centrar_ventana(ventana, ancho, alto):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = (pantalla_ancho // 2) - (ancho // 2)
    y = (pantalla_alto // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

def aplicar_estilo():
    estilo = ttk.Style()
    estilo.theme_use('clam')  # Aplicar tema
    estilo.configure("TLabel", font=("Helvetica", 12), foreground="#333", background="#f0f0f0")  # Fondo claro
    estilo.configure("TButton", font=("Helvetica", 10, "bold"), background="#4CAF50", foreground="white", padding=6)
    estilo.map("TButton", background=[("active", "#45a049")])  # Cambiar color al presionar

def registro():
    def registrar_usuario_gui():
        nombre = entrada_nombre.get()
        apellido = entrada_apellido.get()
        contrasena = entrada_contrasena.get()

        try:
            if not nombre or not apellido:
                raise ValueError("Nombre y apellido no pueden estar vacíos")

            # Generar el nombre de usuario automáticamente
            usuario = f"{nombre[0].upper()}{apellido.split()[0].capitalize()}"

            img_ruta = capturar_imagen(usuario)
            if img_ruta is None:
                messagebox.showinfo("Cancelado", "Registro cancelado por el usuario")
                return

            registrar_usuario(nombre, apellido, usuario, contrasena, img_ruta)
            messagebox.showinfo("Éxito", f"Usuario registrado exitosamente. Usuario generado: {usuario}")
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    ventana_registro = tk.Toplevel()
    ventana_registro.configure(bg="#f0f0f0")  # Fondo claro
    ventana_registro.title("Registro de Usuario")
    centrar_ventana(ventana_registro, 400, 400)

    aplicar_estilo()

    etiqueta_nombre = ttk.Label(ventana_registro, text="Nombre:")
    etiqueta_nombre.pack(pady=10)
    entrada_nombre = ttk.Entry(ventana_registro)
    entrada_nombre.pack(pady=5, padx=20, fill='x')

    etiqueta_apellido = ttk.Label(ventana_registro, text="Apellido:")
    etiqueta_apellido.pack(pady=10)
    entrada_apellido = ttk.Entry(ventana_registro)
    entrada_apellido.pack(pady=5, padx=20, fill='x')

    etiqueta_contrasena = ttk.Label(ventana_registro, text="Contraseña:")
    etiqueta_contrasena.pack(pady=10)
    entrada_contrasena = ttk.Entry(ventana_registro, show="*")
    entrada_contrasena.pack(pady=5, padx=20, fill='x')

    boton_registrar = ttk.Button(ventana_registro, text="Registrar", command=registrar_usuario_gui)
    boton_registrar.pack(pady=20)

def main():
    ventana_main = tk.Toplevel()
    ventana_main.configure(bg="#f0f0f0")
    ventana_main.title("Panel Principal - VisionTech Solutions")

    # Centrar ventana
    pantalla_ancho = ventana_main.winfo_screenwidth()
    pantalla_alto = ventana_main.winfo_screenheight()
    ancho = 800
    alto = 600
    x = (pantalla_ancho // 2) - (ancho // 2)
    y = (pantalla_alto // 2) - (alto // 2)
    ventana_main.geometry(f"{ancho}x{alto}+{x}+{y}")

    aplicar_estilo()

    # Crear el contenedor principal
    contenedor_principal = ttk.Frame(ventana_main)
    contenedor_principal.pack(fill='both', expand=True)

    # Crear el sidebar
    frame_sidebar = ttk.Frame(contenedor_principal, padding=10)
    frame_sidebar.grid(row=0, column=0, sticky='ns')

    # Crear un frame para el contenido
    frame_contenido = ttk.Frame(contenedor_principal, padding=10)
    frame_contenido.grid(row=0, column=1, sticky='nsew')

    # Expandir el frame de contenido
    contenedor_principal.columnconfigure(1, weight=1)
    contenedor_principal.rowconfigure(0, weight=1)

    # Añadir el logotipo redimensionado
    imagen_original = Image.open("VisionTech Solutions.png")
    imagen_redimensionada = imagen_original.resize((100, 100), Image.LANCZOS)  # Redimensionar la imagen
    logo = ImageTk.PhotoImage(imagen_redimensionada)

    etiqueta_logo = ttk.Label(frame_contenido, image=logo)
    etiqueta_logo.image = logo  # Mantener una referencia para evitar que sea recolectada por el garbage collector
    etiqueta_logo.pack(pady=10)

    # Mensaje de bienvenida
    etiqueta_bienvenida = ttk.Label(
        frame_contenido, text="Bienvenido a la aplicación de VisionTech Solutions",
        font=("Helvetica", 16), background="#f0f0f0"
    )
    etiqueta_bienvenida.pack(pady=10)

    # Función para actualizar el contenido al hacer clic en los botones del sidebar
    def actualizar_contenido(titulo, contenido):
        for widget in frame_contenido.winfo_children():
            widget.destroy()
        etiqueta_titulo = ttk.Label(frame_contenido, text=titulo, font=("Helvetica", 16), background="#f0f0f0")
        etiqueta_titulo.pack(pady=10)
        etiqueta_contenido = ttk.Label(frame_contenido, text=contenido, font=("Helvetica", 12), background="#f0f0f0")
        etiqueta_contenido.pack(pady=5)

    # Función para cerrar sesión y abrir el formulario de login
    def cerrar_sesion():
        ventana_main.destroy()
        subprocess.Popen(["python", "login_facial.py"])

    # Botones del sidebar
    botones = [
        ("Información de la Empresa", lambda: actualizar_contenido("Información de la Empresa:", "VisionTech Solutions: Innovando el Futuro")),
        ("Contactar Soporte", lambda: actualizar_contenido("Contacto:", "Soporte: soporte@visiontech.com")),
        ("Acceder a Reportes", lambda: actualizar_contenido("Reportes:", "Acceso a reportes")),
        ("Registrar Usuario", registro),  # Llamar a la función de registro para registrar un nuevo usuario
        ("Cerrar Sesión", cerrar_sesion)  # Cerrar sesión y abrir el login
    ]

    for texto, comando in botones:
        ttk.Button(frame_sidebar, text=texto, command=comando, width=25).pack(pady=5)

    # Añadir el footer
    etiqueta_footer = ttk.Label(contenedor_principal, text="© VisionTech Solutions 2024 - Universidad Privada del Norte", font=("Helvetica", 8), foreground="#777", background="#f0f0f0", anchor='center')
    etiqueta_footer.grid(row=1, column=0, columnspan=2, pady=5, sticky='we')

    ventana_main.mainloop()
