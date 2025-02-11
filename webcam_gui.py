import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # Importer Image et ImageTk pour la conversion d'image
import numpy as np  # Assurez-vous d'importer numpy

class WebcamApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Webcam Control")
        
        # Initialisation de la webcam
        self.cap = cv2.VideoCapture(0)

        # Cadre pour afficher la vidéo
        self.video_frame = ttk.Label(self.master)
        self.video_frame.grid(row=0, column=0, columnspan=4)

        # Slider pour la luminosité
        self.brightness_slider = ttk.Scale(self.master, from_=0, to_=255, command=self.set_brightness)
        self.brightness_slider.set(128)  # Valeur par défaut
        self.brightness_slider.grid(row=1, column=0)
        ttk.Label(self.master, text="Luminosité").grid(row=2, column=0)

        # Slider pour le contraste
        self.contrast_slider = ttk.Scale(self.master, from_=0, to_=255, command=self.set_contrast)
        self.contrast_slider.set(128)  # Valeur par défaut
        self.contrast_slider.grid(row=1, column=1)
        ttk.Label(self.master, text="Contraste").grid(row=2, column=1)

        # Slider pour la netteté
        self.sharpness_slider = ttk.Scale(self.master, from_=0, to_=100, command=self.set_sharpness)
        self.sharpness_slider.set(50)  # Valeur par défaut
        self.sharpness_slider.grid(row=1, column=2)
        ttk.Label(self.master, text="Netteté").grid(row=2, column=2)

        # Bouton pour quitter
        self.quit_button = ttk.Button(self.master, text="Quitter", command=self.quit)
        self.quit_button.grid(row=1, column=3)

        self.update_frame()

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Appliquer les réglages de luminosité, contraste et netteté
            brightness = int(self.brightness_slider.get())
            contrast = int(self.contrast_slider.get())
            sharpness = int(self.sharpness_slider.get())

            frame = cv2.convertScaleAbs(frame, alpha=contrast/128, beta=brightness-128)

            # Appliquer un filtre de netteté simple (un filtre Gaussian pour la démonstration)
            if sharpness > 0:
                kernel = np.array([[-1, -1, -1],
                                   [-1, 9 + sharpness / 10, -1],
                                   [-1, -1, -1]])
                frame = cv2.filter2D(frame, -1, kernel)

            # Convertir l'image pour l'affichage
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img = img.resize((640, 480), Image.LANCZOS)  # Redimensionner pour l'affichage
            img = ImageTk.PhotoImage(img)

            self.video_frame.img = img
            self.video_frame['image'] = img

        self.master.after(10, self.update_frame)

    def set_brightness(self, value):
        pass  # Passer car la mise à jour est déjà faite dans update_frame

    def set_contrast(self, value):
        pass  # Passer car la mise à jour est déjà faite dans update_frame

    def set_sharpness(self, value):
        pass  # Passer car la mise à jour est déjà faite dans update_frame

    def quit(self):
        self.cap.release()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = WebcamApp(root)
    root.mainloop()
