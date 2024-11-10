import cv2
import face_recognition
import os

def capturar_imagen(usuario, carpeta_destino="img_registradas"):
    # Crear la carpeta especificada si no existe
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)

    camara = cv2.VideoCapture(0)
    cv2.namedWindow("Registro - Captura de Imagen")

    capturado = False  # Nueva variable para asegurarnos de que solo se capture una vez

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

        cv2.imshow("Registro - Captura de Imagen", frame)

        k = cv2.waitKey(1)
        if k % 256 == ord('c') and len(rostros) > 0 and not capturado:
            # Captura solo si no se ha realizado antes
            img_nombre = f"{usuario}.jpg"
            img_ruta = os.path.join(carpeta_destino, img_nombre)
            cv2.imwrite(img_ruta, frame)
            capturado = True  # Establece la captura a verdadera para evitar duplicados
            break
        elif k % 256 == ord('s'):
            camara.release()
            cv2.destroyAllWindows()
            return None

    camara.release()
    cv2.destroyAllWindows()
    return img_ruta
