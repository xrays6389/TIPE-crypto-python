import tkinter as tk
from tkinter import filedialog, messagebox
from crypto5 import *
from decrypto4 import *

#V1.2 
# Optimisation et fixe les bugs

fichier_selectionne = ""
dossier_selectionne = ""

def window_crypt():
    """Page de cryptage"""

    global fichier_selectionne, dossier_selectionne

    if not fichier_selectionne or not dossier_selectionne:
        messagebox.showwarning("Erreur", "Veuillez sélectionner un fichier et un dossier !")
        return

    try:
        # Vérifier que le fichier est bien lisible
        with open(fichier_selectionne, "rb") as file:
            contenu = file.read()
            print("Fichier trouvé et ouvert avec succès !")

        # Chiffrement
        fichier_crypte = cryptage(fichier_selectionne, dossier_selectionne)
        messagebox.showinfo("Succès", f"Fichier crypté enregistré sous : {fichier_crypte}")

    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors du cryptage : {e}")

def window_uncrypt():
    """Page de décryptage"""
    # Création de la fenêtre de decryptage
    global fichier_selectionne, dossier_selectionne

    if not fichier_selectionne or not dossier_selectionne:
        messagebox.showwarning("Erreur", "Veuillez sélectionner un fichier et un dossier !")
        return

    try:
        print("ok")
        key = load_key(dossier_selectionne, fichier_selectionne)
        fichier_decrypte = decrypto(fichier_selectionne, dossier_selectionne, key)
        messagebox.showinfo("Succès", f"Fichier décrypté enregistré sous : {fichier_decrypte}")

    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors du décryptage : {e}")


def choisir_fichier():
    """Sélectionne un fichier et met à jour l'affichage"""
    global fichier_selectionne
    fichier_selectionne = filedialog.askopenfilename(title="Sélectionnez un fichier")
    if fichier_selectionne:
        lbl_fichier.config(text=f"📂 Fichier sélectionné : {fichier_selectionne}")

def choisir_dossier():
    """Sélectionne un dossier et met à jour l'affichage"""
    global dossier_selectionne
    dossier_selectionne = filedialog.askdirectory(title="Sélectionnez un dossier")
    if dossier_selectionne:
        lbl_dossier.config(text=f"Dossier sélectionné : {dossier_selectionne}")

    
"""forme de la page """

# Création de la fenêtre principale
root = tk.Tk()
root.title("Cryptage & Décryptage")
root.geometry("600x400")

# Titre
tk.Label(root, text="Sélectionnez la méthode voulue", font=("Arial", 14, "bold")).pack(pady=10)

# Boutons de cryptage et décryptage
tk.Button(root, text="Cryptage", command=window_crypt).pack(pady=15)
tk.Button(root, text="Décryptage", command=window_uncrypt).pack(pady=15)

# Sélection de fichier
lbl_fichier = tk.Label(root, text="Aucun fichier sélectionné", fg="blue", wraplength=480)
lbl_fichier.pack(pady=5)
tk.Button(root, text="📂 Choisir un fichier", command=choisir_fichier).pack(pady=5)

# Sélection de dossier
lbl_dossier = tk.Label(root, text="Aucun dossier sélectionné", wraplength=350, justify="center")
lbl_dossier.pack()
tk.Button(root, text="📁 Choisir un dossier", command=choisir_dossier).pack(pady=20)

# Lancer l'interface graphique
root.mainloop()





