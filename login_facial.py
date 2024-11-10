import tkinter as tk  # Importa la librería tkinter para crear interfaces gráficas de usuario (GUI).
from tkinter import messagebox  # Importa la funcionalidad para mostrar mensajes emergentes (informativos, de error, etc.).
from tkinter import ttk  # Importa la librería de widgets themed de tkinter, que proporciona widgets con un aspecto más moderno.
from PIL import Image, ImageTk  # Importa la librería Pillow para manipular imágenes, específicamente para redimensionarlas y usarlas en tkinter.
from db_connection import conectar  # Importa la función conectar desde el módulo db_connection para gestionar la conexión a la base de datos.
from image_capture import capturar_imagen  # Importa la función capturar_imagen del módulo image_capture para tomar fotos o imágenes de los usuarios.
from auth_logic import validar_credenciales  # Importa la función validar_credenciales desde el módulo auth_logic para autenticar a los usuarios.
import threading  # Importa threading para manejar hilos, útil para evitar que la interfaz gráfica se congele durante procesos largos.
import time  # Importa la librería time para simular tiempos de espera, como en una barra de progreso.
import main  # Importa el módulo main para permitir la navegación entre ventanas dentro de la aplicación.


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

def iniciar_sesion():
    def validar_credenciales_gui():
        usuario = entrada_usuario.get()
        contrasena = entrada_contrasena.get()

        def proceso_verificacion():
            try:
                # Mostrar spinner durante la verificación
                progreso = ttk.Progressbar(ventana_inicio, mode='indeterminate')
                progreso.pack(pady=10)
                progreso.start()

                # Simular el tiempo de procesamiento
                time.sleep(2)

                # Validar credenciales (esto debe ejecutarse en el hilo principal)
                ventana_inicio.after(0, verificar_credenciales, usuario, contrasena, progreso)

            except Exception as e:
                progreso.stop()
                progreso.pack_forget()
                ventana_inicio.after(0, lambda: messagebox.showerror("Error", str(e)))

        # Ejecutar la verificación en un hilo para no congelar la UI
        threading.Thread(target=proceso_verificacion).start()

    def verificar_credenciales(usuario, contrasena, progreso):
        try:
            # Llamar a la función de validación
            nombre, apellido = validar_credenciales(usuario, contrasena)

            # Detener y ocultar el progreso
            progreso.stop()
            progreso.pack_forget()

            # Mostrar mensaje de bienvenida (en el hilo principal)
            messagebox.showinfo("Éxito", f"Bienvenido {nombre} {apellido}")

            # Ocultar ventanas actuales y abrir main.py
            ventana_inicio.withdraw()  # Ocultar ventana de inicio de sesión
            ventana.withdraw()  # Ocultar ventana principal
            main.main()  # Llamar a la función principal del archivo main

        except ValueError as ve:
            progreso.stop()
            progreso.pack_forget()
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            progreso.stop()
            progreso.pack_forget()
            messagebox.showerror("Error", str(e))

    ventana_inicio = tk.Toplevel()
    ventana_inicio.configure(bg="#f0f0f0")  # Fondo claro
    ventana_inicio.title("Inicio de Sesión")
    centrar_ventana(ventana_inicio, 400, 250)

    aplicar_estilo()

    etiqueta_usuario = ttk.Label(ventana_inicio, text="Usuario:")
    etiqueta_usuario.pack(pady=10)
    entrada_usuario = ttk.Entry(ventana_inicio)
    entrada_usuario.pack(pady=5, padx=20, fill='x')

    etiqueta_contrasena = ttk.Label(ventana_inicio, text="Contraseña:")
    etiqueta_contrasena.pack(pady=10)
    entrada_contrasena = ttk.Entry(ventana_inicio, show="*")
    entrada_contrasena.pack(pady=5, padx=20, fill='x')

    boton_validar = ttk.Button(ventana_inicio, text="Iniciar Sesión", command=validar_credenciales_gui)
    boton_validar.pack(pady=20)

# Crear la ventana principal
ventana = tk.Tk()
ventana.configure(bg="#f0f0f0")  # Fondo claro
ventana.title("Sistema de Reconocimiento Facial - VisionTech Solutions")
centrar_ventana(ventana, 450, 500)

aplicar_estilo()

# Añadir el logotipo redimensionado
imagen_original = Image.open("VisionTech Solutions.png")
imagen_redimensionada = imagen_original.resize((150, 150), Image.LANCZOS)  # Redimensionar la imagen a 150x150 píxeles
logo = ImageTk.PhotoImage(imagen_redimensionada)

etiqueta_logo = ttk.Label(ventana, image=logo, background="#f0f0f0")
etiqueta_logo.image = logo  # Mantener una referencia para evitar que sea recolectada por el garbage collector
etiqueta_logo.pack(pady=10)

# Crear el botón de inicio de sesión
boton_inicio_sesion = ttk.Button(ventana, text="Inicio de Sesión", command=iniciar_sesion, width=20)
boton_inicio_sesion.pack(pady=10)

# Crear el botón de salir
boton_salir = ttk.Button(ventana, text="Salir", command=ventana.quit, width=20)
boton_salir.pack(pady=10)

# Cambiar el color del botón de salir al pasar el mouse
boton_salir.configure(style="Salir.TButton")

# Añadir el estilo para el botón de salir
estilo = ttk.Style()
estilo.configure("Salir.TButton", font=("Helvetica", 10, "bold"), background="black", foreground="white", padding=6)
estilo.map("Salir.TButton", background=[("active", "red")])  # Cambiar color al pasar el mouse

etiqueta_footer = ttk.Label(ventana, text="© VisionTech Solutions 2024 - Universidad Privada del Norte", font=("Helvetica", 8), foreground="#777", background="#f0f0f0")
etiqueta_footer.pack(side="bottom", pady=5)

# Ejecutar la aplicación
ventana.mainloop()

