from tkinter import Tk
import tkinter as tk
from tkinter.filedialog import askopenfilename


root = tk.Tk() #creer une fenetre nommé root
root.title("Cryptage") #titre fenetre
root.geometry("300x200") #taille fenetre
root.minsize(200, 300) #taille min
root.maxsize(2000, 1900) #taille max
root.config(background='#41B77F' ) #couleur fond


label = tk.Label(root, text="Test", font=("Courrier",30),bg='#41B77F', fg='white')
label.pack()

root.mainloop() #ouvre la fenetre nommer root


Tk().withdraw()  # Masque la fenêtre Tkinter principale
fichier = askopenfilename(title="Choisir un fichier", filetypes=[("Tous les fichiers", "*.*")])

if fichier:
    print("Fichier sélectionné :", fichier)

