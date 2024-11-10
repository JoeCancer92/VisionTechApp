------------- Descripción del Programa -------------

Este programa es un sistema de reconocimiento facial 
desarrollado para VisionTech Solutions. Utiliza una combinación de 
librerías para crear una interfaz gráfica amigable (Tkinter), realizar autenticación facial 
(face_recognition y OpenCV), y gestionar la captura de imágenes de los usuarios para el registro. 
La aplicación cuenta con una pantalla de inicio de sesión, autenticación de usuarios, y una interfaz principal 
donde se puede acceder a diferentes funcionalidades, como información de la empresa y contacto. 
Además, permite registrar nuevos usuarios utilizando una cámara web para capturar la imagen. 
El sistema está diseñado para ser fácil de usar y brindar una experiencia moderna y rápida al usuario.

-------------README: Explicación de las Importaciones Necesarias-------------

 Importaciones y su Propósito

1. import tkinter as tk:
   - Tkinter se utiliza para crear interfaces gráficas de usuario (GUIs). En este proyecto, es la biblioteca principal para construir ventanas y widgets como botones y etiquetas.

2. from tkinter import messagebox:
   - messagebox proporciona cuadros de diálogo para mostrar mensajes de error, información o advertencias al usuario.

3. from tkinter import ttk:
   - ttk se utiliza para dar estilo a los widgets (como botones, etiquetas y entradas), proporcionando una apariencia más moderna y mejorada a la interfaz.

4. from PIL import Image, ImageTk:
   - PIL (Pillow) se utiliza para manipular y mostrar imágenes. Image permite cargar y redimensionar imágenes, mientras que ImageTk convierte la imagen para ser compatible con Tkinter.

5. from db_connection import conectar:
   - Importa una función personalizada conectar para establecer una conexión con la base de datos. ÚTil para la autenticación y registro de usuarios.

6. from image_capture import capturar_imagen:
   - Importa la función capturar_imagen que permite capturar imágenes a través de una cámara web. Es utilizada para el registro y reconocimiento facial.

7. from auth_logic import validar_credenciales:
   - validar_credenciales es una función para autenticar los datos ingresados por el usuario y permitir o denegar el acceso según corresponda.

8. import threading:
   - threading permite ejecutar tareas en segundo plano sin bloquear la interfaz gráfica. Esto mejora la experiencia del usuario, ya que evita que la interfaz se congele durante procesos largos.

9. import time:
   - Se utiliza para simular retardos, como mostrar una barra de progreso, para mejorar la experiencia visual del usuario.

10. import main:
    - Importa el archivo main, que contiene la lógica para navegar a la interfaz principal de la aplicación luego de que el usuario inicia sesión correctamente.

11. import subprocess:
    - subprocess se utiliza para ejecutar comandos del sistema, como abrir otro archivo Python desde el código. Esto es útil, por ejemplo, para navegar entre diferentes ventanas o funcionalidades.

12. import cv2:
    - cv2 es parte de OpenCV, una biblioteca utilizada para la captura y manipulación de video. En este proyecto, se utiliza para trabajar con la cámara para captura de rostros.

13. import face_recognition:
    - face_recognition es una biblioteca utilizada para el reconocimiento facial, basada en dlib. Es útil para detectar y reconocer rostros.

14. import os:
    - os se usa para interactuar con el sistema operativo, como acceder a archivos y directorios. Es útil para guardar o recuperar imágenes de usuarios.

15. cmake (para face_recognition y dlib):
    - cmake es una herramienta de construcción utilizada para compilar dlib, que es una dependencia de face_recognition. Es esencial para la instalación adecuada de dlib, ya que ayuda a configurar y generar el código fuente correctamente.



