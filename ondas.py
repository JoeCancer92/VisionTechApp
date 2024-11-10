import tkinter as tk
import math
import time

class WaterWaveEffect:
    def __init__(self, canvas, width, height):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.wave_count = 5
        self.amplitude = 10
        self.frequency = 0.02
        self.phase = 0
        self.lines = []
        self.create_wave_lines()
        self.update_wave()

    def create_wave_lines(self):
        # Crear las lineas iniciales para las ondas
        for i in range(self.wave_count):
            line = self.canvas.create_line(0, 0, self.width, 0, fill="blue")
            self.lines.append(line)

    def update_wave(self):
        # Actualizar las posiciones de las lineas para simular la onda
        self.phase += 0.1
        for i, line in enumerate(self.lines):
            points = []
            y_offset = (i + 1) * (self.height / (self.wave_count + 1))
            for x in range(self.width):
                y = y_offset + self.amplitude * math.sin(self.frequency * x + self.phase)
                points.append(x)
                points.append(y)
            self.canvas.coords(line, *points)
        self.canvas.after(50, self.update_wave)


# Creamos un archivo Python llamado ondas.py
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Efecto de Ondas en Water Wave")
    width, height = 600, 400
    canvas = tk.Canvas(root, width=width, height=height, bg="white")
    canvas.pack()
    water_wave = WaterWaveEffect(canvas, width, height)
    root.mainloop()
