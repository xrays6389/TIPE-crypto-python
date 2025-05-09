import os
import tkinter as tk
from tkinter import filedialog, messagebox

fichier_selectionne = ""

def cryptage2(lbl_fichier):
    try:
        output_file = lbl_fichier + ".encrypted"
        decalage = 5
        with open(lbl_fichier, "rb") as file, open(output_file, "wb") as encrypted_file:
            for byte in file.read():
                encrypted_byte = (byte + decalage) % 256
                encrypted_file.write(bytes([encrypted_byte]))
        return output_file
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors du cryptage : {e}")
        return None

def decryptage2(lbl_fichier):
    try:
        if not lbl_fichier.endswith(".encrypted"):
            raise ValueError("Le fichier n'est pas un fichier chiffré")
        output_file = lbl_fichier.replace(".encrypted", ".decrypted")
        decalage = 5
        with open(lbl_fichier, "rb") as file, open(output_file, "wb") as decrypted_file:
            for byte in file.read():
                decrypted_byte = (byte - decalage) % 256
                decrypted_file.write(bytes([decrypted_byte]))
        return output_file
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors du décryptage : {e}")
        return None

def window_crypt():
    global fichier_selectionne

    if not fichier_selectionne:
        messagebox.showwarning("Erreur", "Veuillez sélectionner un fichier !")
        return

    fichier_crypte = cryptage2(fichier_selectionne)
    if fichier_crypte:
        messagebox.showinfo("Succès", f"Fichier crypté enregistré sous : {fichier_crypte}")


def window_uncrypt():
    global fichier_selectionne

    if not fichier_selectionne:
        messagebox.showwarning("Erreur", "Veuillez sélectionner un fichier !")
        return

    fichier_decrypte = decryptage2(fichier_selectionne)
    if fichier_decrypte:
        messagebox.showinfo("Succès", f"Fichier décrypté enregistré sous : {fichier_decrypte}")
    

def choisir_fichier():
    global fichier_selectionne
    fichier_selectionne = filedialog.askopenfilename(title="Sélectionnez un fichier")
    if fichier_selectionne:
        lbl_fichier.config(text=f"📂 Fichier sélectionné : {fichier_selectionne}")

root = tk.Tk()
root.title("Cryptage & Décryptage fichier clé")
root.geometry("500x200")

lbl_fichier = tk.Label(root, text="Aucun fichier sélectionné", fg="blue", wraplength=480)
lbl_fichier.pack(pady=5)
tk.Button(root, text="📂 Choisir un fichier", command=choisir_fichier).pack(pady=5)

tk.Button(root, text="Cryptage", command=window_crypt).pack(pady=15)
tk.Button(root, text="Décryptage", command=window_uncrypt).pack(pady=15)

root.mainloop()
