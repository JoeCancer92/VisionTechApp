from db_connection import conectar
from image_capture import capturar_imagen
from tkinter import messagebox
from mysql.connector import Error
import face_recognition
import os
import cv2  # Necesario para el manejo de la cámara
import shutil  # Para copiar archivos

# Crear la carpeta temporal si no existe
carpeta_temporal = "temp"
if not os.path.exists(carpeta_temporal):
    os.makedirs(carpeta_temporal)

# Función para registrar usuario
def registrar_usuario(nombre, apellido, usuario, contrasena, img_ruta):
    if usuario == "" or contrasena == "":
        raise ValueError("Usuario y contraseña no pueden estar vacíos")

    # Definir la carpeta y ruta de la imagen registrada
    carpeta_img_registradas = "img_registradas"
    if not os.path.exists(carpeta_img_registradas):
        os.makedirs(carpeta_img_registradas)

    img_ruta_registrada = os.path.join(carpeta_img_registradas, f"{usuario}.jpg")

    # Si la imagen ya existe, no sobreescribirla (para evitar eliminar una imagen ya almacenada)
    if not os.path.exists(img_ruta_registrada):
        shutil.copy(img_ruta, img_ruta_registrada)

    # Proceder a guardar el usuario y la imagen en la base de datos
    conexion = conectar()
    if conexion:
        try:
            # Leer la imagen para almacenar en la base de datos
            with open(img_ruta_registrada, 'rb') as f:
                imagen_blob = f.read()

            cursor = conexion.cursor()
            query = "INSERT INTO usuarios (nombre, apellido, usuario, contrasena, imagen) VALUES (%s, %s, %s, %s, %s)"
            valores = (nombre, apellido, usuario, contrasena, imagen_blob)
            cursor.execute(query, valores)
            conexion.commit()

            messagebox.showinfo("Éxito", "Usuario registrado exitosamente")
        except Error as e:
            raise Exception(f"No se pudo registrar el usuario: {e}")
        finally:
            cursor.close()
            conexion.close()

# Función para validar credenciales del usuario
def validar_credenciales(usuario, contrasena):
    if usuario == "" or contrasena == "":
        raise ValueError("Usuario y contraseña no pueden estar vacíos")

    conexion = conectar()
    if conexion:
        try:
            # Verificar las credenciales en la base de datos
            cursor = conexion.cursor()
            query = "SELECT nombre, apellido, usuario, imagen FROM usuarios WHERE usuario = %s AND contrasena = %s"
            valores = (usuario, contrasena)
            cursor.execute(query, valores)
            resultado = cursor.fetchone()

            if resultado is None:
                raise ValueError("Usuario o contraseña incorrectos")

            # Asignar los valores devueltos por la consulta
            nombre, apellido, usuario_db, imagen_blob = resultado

            # Guardar la imagen de la base de datos temporalmente para la comparación
            img_ruta_db = os.path.join(carpeta_temporal, f"temp_{usuario_db}.jpg")
            with open(img_ruta_db, 'wb') as f:
                f.write(imagen_blob)

            # ACTIVAR LA CÁMARA UNA SOLA VEZ
            camara = cv2.VideoCapture(0)
            cv2.namedWindow("Inicio de Sesión - Captura de Imagen")

            rostro_detectado = False
            img_ruta_captura = None

            while True:
                ret, frame = camara.read()
                if not ret:
                    raise Exception("No se pudo acceder a la cámara")

                rgb_frame = frame[:, :, ::-1]  # Convertir BGR a RGB
                rostros = face_recognition.face_locations(rgb_frame)

                if len(rostros) > 0:
                    cv2.putText(frame, "Rostro detectado - Presiona 'c' para capturar", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                else:
                    cv2.putText(frame, "No se detecta un rostro", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                cv2.imshow("Inicio de Sesión - Captura de Imagen", frame)

                k = cv2.waitKey(1)
                if k % 256 == ord('c') and len(rostros) > 0:
                    img_ruta_captura = os.path.join(carpeta_temporal, f"captura_{usuario}.jpg")
                    cv2.imwrite(img_ruta_captura, frame)
                    rostro_detectado = True
                    break
                elif k % 256 == ord('s'):
                    camara.release()
                    cv2.destroyAllWindows()
                    raise ValueError("Inicio de sesión cancelado por el usuario")

            # Cerrar la cámara después de la captura exitosa
            camara.release()
            cv2.destroyAllWindows()

            if not rostro_detectado:
                raise ValueError("No se detectó un rostro válido")

            # Cargar y comparar las imágenes inmediatamente después de capturar el rostro
            imagen_registrada = face_recognition.load_image_file(img_ruta_db)
            imagen_capturada = face_recognition.load_image_file(img_ruta_captura)

            # Codificar los rostros para la comparación
            try:
                encoding_registrada = face_recognition.face_encodings(imagen_registrada)[0]
                encoding_capturada = face_recognition.face_encodings(imagen_capturada)[0]
            except IndexError:
                raise ValueError("No se detectó un rostro en una de las imágenes")

            # Comparar los rostros capturados
            resultados = face_recognition.compare_faces([encoding_registrada], encoding_capturada)

            if not resultados[0]:
                raise ValueError("El rostro no coincide con el usuario registrado")

            # Eliminación de imágenes temporales (solo después de la autenticación)
            if os.path.exists(img_ruta_db):
                os.remove(img_ruta_db)
            if os.path.exists(img_ruta_captura):
                os.remove(img_ruta_captura)

            # Retornar nombre y apellido si todo fue exitoso
            return nombre, apellido

        except Error as e:
            raise Exception(f"Error al validar las credenciales: {e}")
        finally:
            cursor.close()
            conexion.close()
