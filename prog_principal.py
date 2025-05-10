import tkinter as tk
from tkinter import filedialog, messagebox
from crypto5 import *
from decrypto4 import *
from threading import Thread 
from concurrent.futures import ThreadPoolExecutor

fichier_selectionne = ""
dossier_selectionne = ""
dossier_clé = ""
executor = ThreadPoolExecutor(max_workers=2)

def window_crypt():
    """Page de cryptage"""

    global fichier_selectionne, dossier_selectionne, dossier_clé

    if not fichier_selectionne or not dossier_selectionne or not dossier_clé:
        messagebox.showwarning("Erreur", "Veuillez sélectionner un fichier, un dossier et le dossier pour la clé !")
        return

    try:
        # Vérifier que le fichier est bien lisible
        with open(fichier_selectionne, "rb") as file:
            contenu = file.read()
            print("Fichier trouvé et ouvert avec succès !")

        # Chiffrement
        future = executor.submit(encrypt_file, fichier_selectionne, dossier_selectionne, dossier_clé)
        def on_done(future):
            try:
                chemin = future.result()
                # Afficher un message de succès
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors du cryptage : {e}")
                return
            else:
                root.after(0, lambda: messagebox.showinfo("Succès", f"Fichier crypté enregistré sous : {chemin}"))
        future.add_done_callback(on_done)

    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors du cryptage : {e}")

def window_uncrypt():
    """Page de décryptage"""
    # Création de la fenêtre de decryptage
    global fichier_selectionne, dossier_selectionne, dossier_clé

    if not fichier_selectionne or not dossier_selectionne or not dossier_clé:
        messagebox.showwarning("Erreur", "Veuillez sélectionner un fichier, un dossier et le dossier pour la clé !")
        return

    try:
        key = load_key(fichier_selectionne, dossier_clé)
        fichier_decrypte = decrypt_file(fichier_selectionne, dossier_selectionne, key)
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
    dossier_selectionne = filedialog.askdirectory(title="Sélectionnez un dossier de sauvegarde")
    if dossier_selectionne:
        lbl_dossier.config(text=f"Dossier sélectionné : {dossier_selectionne}")

def choisir_d_clé():
    """Sélectionne le fichier clé et met a jour l'affichage"""
    global dossier_clé
    dossier_clé = filedialog.askdirectory(title="Sélectionnez le dossier avec la clé")
    if dossier_clé:
        lbl_clé.config(text=f"Fichier clé : {dossier_clé}")


    
"""forme de la page """

# Création de la fenêtre principale
root = tk.Tk()
root.title("Cryptage & Décryptage")
root.geometry("700x500")

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
lbl_dossier = tk.Label(root, text="Aucun dossier sélectionné", fg="blue", wraplength=350, justify="center")
lbl_dossier.pack()
tk.Button(root, text="📁 Choisir un dossier", command=choisir_dossier).pack(pady=20)

# Sélection du fichier clé
lbl_clé = tk.Label(root, text="Aucun dossier clé sélectionné", fg="blue", wraplength=220)
lbl_clé.pack()
tk.Button(root, text="📁 Choisir un dossier clé", command=choisir_d_clé).pack(pady=20)

# Lancer l'interface graphique
root.mainloop()