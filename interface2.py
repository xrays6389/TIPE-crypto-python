import tkinter as tk
from tkinter import filedialog, messagebox
from crypto4 import *

#V1.1

def window_crypt(doc,ch_dep):
    """Page de cryptage"""
    # Création de la fenêtre de cryptage
    root_crypt = tk.Toplevel(root)
    root_crypt.title("Cryptage")
    root_crypt.geometry("500x300")
    label_crypt = tk.Label(root_crypt, text="Cryptage", font=("Arial", 14, "bold"))
    btn_retour = tk.Button(root_crypt, text="Fermer", command=root_crypt.destroy)
    btn_retour.pack()
    
    #permet de verifier que le fichier est bien trouvé par le programme
    with open(doc, "rb") as file:
        contenu = file.read()
        print("Fichier trouvé et ouvert avec succès !")
    #chiffrement
    doc = doc.strip()
    doc = cryptage(doc,ch_dep)
    return doc

def window_uncrypt():
    """Page de décryptage"""
    # Création de la fenêtre de decryptage
    root_uncrypt = tk.Toplevel(root)
    root_uncrypt.title("Décryptage")
    root_uncrypt.geometry("500x300")
    label_uncrypt = tk.Label(root_uncrypt, text="Décryptage", font=("Arial", 14, "bold"))
    btn_retour = tk.Button(root_uncrypt, text="Fermer", command=root_uncrypt.destroy)
    btn_retour.pack()
    # Bouton pour sélectionner un fichier
    btn_choisir = tk.Button(root_uncrypt, text="📂 Choisir un fichier", command=choisir_fichier)
    btn_choisir.pack(pady=5)
    # Label pour afficher le fichier sélectionné
    lbl_fichier = tk.Label(root_uncrypt, text="Aucun fichier sélectionné", fg="blue", wraplength=480)
    lbl_fichier.pack(pady=5)
    # Bouton pour sélectionner un dossier
    btn = tk.Button(root_uncrypt, text="Choisir un dossier", command=choisir_dossier)
    btn.pack(pady=20)

def choisir_fichier():
    #Ouvre un explorateur de fichiers et récupère le chemin du fichier sélectionné.
    fichier = filedialog.askopenfilename(title="Sélectionnez un fichier")
    if fichier:  # Vérifier si un fichier a été sélectionné
        lbl_fichier.config(text=f"📂 Fichier sélectionné : {fichier}")
        #btn_utiliser.config(state=tk.NORMAL)  # Activer le bouton "Utiliser le fichier"
        global fichier_selectionne
        fichier_selectionne = fichier  # Stocker le fichier sélectionné
        return fichier_selectionne

def utiliser_fichier():
    #Utilise le fichier sélectionné dans une fonction.
    if fichier_selectionne:
        messagebox.showinfo("Traitement", f"Le fichier {fichier_selectionne} est en cours d'utilisation.")
        traiter_fichier(fichier_selectionne)  # Appelle une fonction de traitement

def choisir_dossier():
    dossier = filedialog.askdirectory()  # Ouvre la boîte de dialogue
    if dossier:  # Vérifie si un dossier a été sélectionné
        label.config(text=f"Dossier sélectionné:\n{dossier}")
        dossier_selectionne = dossier
        return dossier_selectionne

def traiter_fichier(fichier):
    #Exemple de fonction utilisant le fichier.
    print(f"Traitement du fichier : {fichier}")

    
"""forme de la page """

# Création de la fenêtre principale
root = tk.Tk()
root.title("Cryptage & Décryptage")
root.geometry("600x400")

# Titre
lbl_titre = tk.Label(root, text="Sélectionnez la méthode voulue", font=("Arial", 14, "bold"))
lbl_titre.pack(pady=10)

# Bouton pour choisir entre cryptage et decryptage
btn_cryptage = tk.Button(root, text="Cryptage", command=window_crypt)
btn_cryptage.pack(pady=15)

btn_decryptage = tk.Button(root, text="Décryptage", command=window_uncrypt)
btn_decryptage.pack(pady=15)

# Label pour afficher le fichier sélectionné
lbl_fichier = tk.Label(root, text="Aucun fichier sélectionné", fg="blue", wraplength=480)
lbl_fichier.pack(pady=5)

# Label pour afficher le dossier sélectionné
label = tk.Label(root, text="Aucun dossier sélectionné", wraplength=350, justify="center")
label.pack()

# Bouton pour sélectionner un fichier
btn_choisir = tk.Button(root, text="📂 Choisir un fichier", command=choisir_fichier)
btn_choisir.pack(pady=5)
# Label pour afficher le fichier sélectionné
lbl_fichier = tk.Label(root, text="Aucun fichier sélectionné", fg="blue", wraplength=480)
lbl_fichier.pack(pady=5)
# Bouton pour sélectionner un dossier
btn = tk.Button(root, text="Choisir un dossier", command=choisir_dossier)
btn.pack(pady=20)

# Lancer l'interface graphique
root.mainloop()





