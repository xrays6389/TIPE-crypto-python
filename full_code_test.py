import os
import math
import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet
from concurrent.futures import ThreadPoolExecutor, as_completed

# --- Crypto Functions ---
# génération de la clé
def generate_key(file_name, key_dir):
    key_path = os.path.join(key_dir, "key.key")
    os.makedirs(key_dir, exist_ok=True)
    # Crée le fichier de clés s'il n'existe pas
    if not os.path.exists(key_path):
        open(key_path, "w").close()
        os.chmod(key_path, 0o600)
    # Vérifie si la clé existe déjà
    with open(key_path, "r", encoding="utf-8") as key_file:
        for line in key_file.readlines():
            try:
                fichier, cle = line.strip().split("|")
                if fichier == file_name:
                    return cle.encode()
            except ValueError:
                print(f"[Erreur] Ligne incorrecte dans le fichier de clés : {line.strip()}")
    # Génération d'une nouvelle clé si aucune clé existante n'a été trouvée
    new_key = Fernet.generate_key()
    with open(key_path, "a", encoding="utf-8") as key_file:
        key_file.write(f"{file_name}|{new_key.decode()}\n")
    print(f"[Info] Nouvelle clé générée pour {file_name}")
    return new_key

# Fonction pour chiffrer un morceau de fichier
def encrypt_chunk(file_path, chunk_index, key, chunk_size):
    chunk_name = f"{file_path}_part{chunk_index}" # nom du morceau
    with open(file_path, "rb") as f: 
        f.seek(chunk_index * chunk_size)
        chunk_data = f.read(chunk_size)

     # Chiffrement du morceau
    if chunk_data:
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(chunk_data)
        with open(chunk_name, "wb") as chunk_file:
            chunk_file.write(encrypted_data)

    return chunk_name

# Fonction pour assembler les morceaux chiffrés
def assemble_encrypted_file(output_path, chunks):
    try:
        chunks.sort(key=lambda x: int(x.split('_part')[-1]))
    except ValueError as e:
        print(f"[Erreur] Numéro de morceau invalide : {e}")
        return False
    # Vérification des morceaux avant assemblage
    with open(output_path, "wb") as final_file:
        for chunk in chunks:
            if not os.path.exists(chunk):
                print(f"[Erreur] Le morceau {chunk} est manquant !")
                return False
            with open(chunk, "rb") as chunk_file:
                final_file.write(chunk_file.read())
    print(f"[Succès] Fichier assemblé sous {output_path}")
    return True

# Fonction pour nettoyer les morceaux temporaires
def cleanup_chunks(chunks):
    for chunk in chunks:
        try:
            os.remove(chunk)
        except FileNotFoundError:
            print(f"[Avertissement] Le morceau {chunk} n'existe pas ou a déjà été supprimé.")

# Fonction principale de cryptage
def encrypt_file(file_path, output_dir, key_dir, num_chunks=4):
    file_name = os.path.basename(file_path)
    key = generate_key(file_name, key_dir)
    file_size = os.path.getsize(file_path)
    chunk_size = math.ceil(file_size / num_chunks)

    with ThreadPoolExecutor(max_workers=num_chunks) as executor:
        chunks = list(executor.map(
            lambda i: encrypt_chunk(file_path, i, key, chunk_size),
            range(num_chunks)
        ))

    # Assemblage des morceaux chiffrés
    output_file = os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}_encrypted{os.path.splitext(file_name)[1]}")
    if assemble_encrypted_file(output_file, chunks):
        cleanup_chunks(chunks) # Nettoyage des morceaux temporaires
        os.remove(file_path) # Suppression du fichier original
        print(f"[Succès] Fichier chiffré sauvegardé sous {output_file}")
        return output_file
    else:
        print("[Erreur] Assemblage des morceaux échoué.")
        return None

# --- Decrypt Functions ---
# Fonction pour charger la clé
def load_key(doc, ch_clé):
    key_path = os.path.join(str(ch_clé), "key.key")
    if not os.path.exists(key_path):
        raise FileNotFoundError(f"Clé introuvable : {key_path}")
     # Vérifie si le fichier de clés existe
    with open(key_path, "r", encoding="utf-8") as key_file:
        lignes = key_file.readlines()

    for ligne in lignes:
        ligne = ligne.strip()
        if not ligne: # Ignore les lignes vides
            continue
        try:
            fichier, cle = ligne.split("|") # Sépare le fichier et la clé
            base, ext = os.path.splitext(fichier) 
            fichier = base + "_encrypted" + ext # Ajoute le suffixe "_encrypted"
            L2 = os.path.basename(doc) 
            if fichier == L2: # Vérifie si c'est la bonne clé
                return cle.encode() # Convertit la clé en format binaire
        except ValueError:
            continue

    raise ValueError(f"Aucune clé trouvée pour {doc}") # Lève une exception si aucune clé n'est trouvée

# Fonction pour déchiffrer un morceau spécifique
def decrypt_chunk(chunk, fernet):
    with open(chunk, "rb") as chunk_file:
        encrypted_data = chunk_file.read()
        decrypted_data = fernet.decrypt(encrypted_data)
    return decrypted_data, chunk
# Fonction principale de déchiffrement
def decrypt_file(doc_crypt, output_dir, key_dir, num_threads=4):
    doc_crypt = str(doc_crypt)
    output_dir = str(output_dir)
    key_dir = str(key_dir)
    # Récupération de la clé
    key = load_key(doc_crypt, key_dir)
    fernet = Fernet(key)

    # Determine taille des chunks (same logic as encryption)
    file_size = os.path.getsize(doc_crypt)
    num_chunks = num_threads  # or infer from encryption if stored
    chunk_size = math.ceil(file_size / num_chunks)

    # Prepare output file
    base_name = os.path.basename(doc_crypt)
    name, ext = os.path.splitext(base_name)
    output_file = os.path.join(output_dir, f"{name.replace('_encrypted', '')}{ext}")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Diviser le fichier en morceaux
    # Crée une liste pour stocker les noms des morceaux
    chunk_files = []
    with open(doc_crypt, "rb") as infile:
        for i in range(num_chunks):
            chunk_data = infile.read(chunk_size)
            if not chunk_data:
                break
            chunk_name = f"{doc_crypt}_part{i}"
            with open(chunk_name, "wb") as chunk_file:
                chunk_file.write(chunk_data)
            chunk_files.append(chunk_name)

    # Décryptage ckunk en parralelle
    decrypted_chunks = [None] * len(chunk_files)
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = {executor.submit(decrypt_chunk, chunk, fernet): idx for idx, chunk in enumerate(chunk_files)}
        for future in as_completed(futures):
            decrypted_data, chunk = future.result()
            idx = futures[future]
            decrypted_chunks[idx] = decrypted_data
            os.remove(chunk)

    # Ecris les données déchiffrées dans l'ordre dans le fichier de sortie
    with open(output_file, "wb") as final_file:
        for data in decrypted_chunks:
            final_file.write(data)

    print(f"[Succès] Fichier déchiffré sauvegardé sous {output_file}")
    return output_file

# --- Interface Graphique ---
# variables globales
fichier_selectionne = ""
dossier_selectionne = ""
dossier_clé = ""
executor = ThreadPoolExecutor(max_workers=2)
# --- Fonction pour le bouton de cryptage ---
def window_crypt():
    global fichier_selectionne, dossier_selectionne, dossier_clé

    if not fichier_selectionne or not dossier_selectionne or not dossier_clé:
        messagebox.showwarning("Erreur", "Veuillez sélectionner un fichier, un dossier et le dossier pour la clé !") 
        return

    try:
        with open(fichier_selectionne, "rb") as file:
            file.read() # Vérifie que le fichier est bien lisible
        # Chiffrement avec un thread
        future = executor.submit(encrypt_file, fichier_selectionne, dossier_selectionne, dossier_clé)
        def on_done(future):
            try:
                chemin = future.result() # chemin du fichier chiffré
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors du cryptage : {e}")
            else:
                root.after(0, lambda: messagebox.showinfo("Succès", f"Fichier crypté enregistré sous : {chemin}"))
        future.add_done_callback(on_done)

    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors du cryptage : {e}")

# --- Fonction pour le bouton de décryptage ---
def window_uncrypt():
    global fichier_selectionne, dossier_selectionne, dossier_clé

    if not fichier_selectionne or not dossier_selectionne or not dossier_clé:
        messagebox.showwarning("Erreur", "Veuillez sélectionner un fichier, un dossier et le dossier pour la clé !")
        return

# Décryptage avec un thread
    future = executor.submit(decrypt_file, fichier_selectionne, dossier_selectionne, dossier_clé)
    def on_done(future):
        try:
            chemin = future.result()  # chemin du fichier déchiffré
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du décryptage : {e}")
        else:
            root.after(0, lambda: messagebox.showinfo("Succès", f"Fichier décrypté enregistré sous : {chemin}"))
    future.add_done_callback(on_done)

# --- Fonctions pour choisir le fichier et les dossiers ---
def choisir_fichier():
    global fichier_selectionne
    fichier_selectionne = filedialog.askopenfilename(title="Sélectionnez un fichier") #ouvre explorateur de fichiers pour choisir le fichier
    if fichier_selectionne:
        lbl_fichier.config(text=f"📂 Fichier sélectionné : {fichier_selectionne}")

def choisir_dossier():
    global dossier_selectionne
    dossier_selectionne = filedialog.askdirectory(title="Sélectionnez un dossier de sauvegarde") #ouvre explorateur de fichiers pour choisir le dossier d'enregistrement
    if dossier_selectionne:
        lbl_dossier.config(text=f"Dossier sélectionné : {dossier_selectionne}")

def choisir_d_clé():
    global dossier_clé
    dossier_clé = filedialog.askdirectory(title="Sélectionnez le dossier avec la clé") # ouvre explorateur de fichiers pour choisir le dossier clé
    if dossier_clé:
        lbl_clé.config(text=f"Fichier clé : {dossier_clé}")

# Interface
root = tk.Tk()
root.title("Cryptage & Décryptage") # Titre de la fenêtre
root.geometry("700x500") # Taille de la fenêtre
# Titre
tk.Label(root, text="Sélectionnez la méthode voulue", font=("Arial", 14, "bold")).pack(pady=10)
# boutons de l'interface graphique
tk.Button(root, text="Cryptage", command=window_crypt).pack(pady=15)
tk.Button(root, text="Décryptage", command=window_uncrypt).pack(pady=15)

lbl_fichier = tk.Label(root, text="Aucun fichier sélectionné", fg="blue", wraplength=480)
lbl_fichier.pack(pady=5)
tk.Button(root, text="📂 Choisir un fichier", command=choisir_fichier).pack(pady=5)

lbl_dossier = tk.Label(root, text="Aucun dossier sélectionné", fg="blue", wraplength=350, justify="center")
lbl_dossier.pack()
tk.Button(root, text="📁 Choisir un dossier", command=choisir_dossier).pack(pady=20)

lbl_clé = tk.Label(root, text="Aucun dossier clé sélectionné", fg="blue", wraplength=220)
lbl_clé.pack()
tk.Button(root, text="📁 Choisir un dossier clé", command=choisir_d_clé).pack(pady=20)

# Lancement de l'interface
root.mainloop()
