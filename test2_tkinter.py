import tkinter as tk
from tkinter import filedialog

#fonctionne permet de chisir un  fichier ou dossiier a regarder pour comprendre comment ca fonctionne

def ouvrir_fichier():
    fichier = filedialog.askopenfilename(title="Choisir un fichier", filetypes=[("Tous les fichiers", "*.*")])
    if fichier:
        lbl_fichier.config(text=f"📂 Fichier : {fichier}")

def ouvrir_dossier():
    dossier = filedialog.askdirectory(title="Choisir un dossier")
    if dossier:
        lbl_dossier.config(text=f"📁 Dossier : {dossier}")

# Création de la fenêtre principale
root = tk.Tk()
root.title("Explorateur de fichiers")
root.geometry("500x300")
root.resizable(False, False)  # Empêche le redimensionnement

# Ajout d'un titre
lbl_titre = tk.Label(root, text="Sélectionnez un fichier ou un dossier", font=("Arial", 14, "bold"))
lbl_titre.pack(pady=10)

# Boutons
btn_ouvrir = tk.Button(root, text="📂 Ouvrir un fichier", command=ouvrir_fichier)
btn_ouvrir.pack(pady=5)
btn_dossier = tk.Button(root, text="📁 Choisir un dossier", command=ouvrir_dossier)
btn_dossier.pack(pady=5)

# Labels pour afficher les résultats
lbl_fichier = tk.Label(root, text="", fg="blue", wraplength=480)
lbl_fichier.pack(pady=5)

lbl_dossier = tk.Label(root, text="", fg="green", wraplength=480)
lbl_dossier.pack(pady=5)

# Lancer l'interface graphique
root.mainloop()
