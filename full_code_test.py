import os #permet de manipuler les chemins de fichiers et dossiers
import math # permet de faire des calculs mathématiques
import tkinter as tk # pour l'interface graphique
from tkinter import filedialog, messagebox # pour les boîtes de dialogue
from cryptography.fernet import Fernet # pour le chiffrement et déchiffrement
from concurrent.futures import ThreadPoolExecutor, as_completed # pour le traitement parallèle des morceaux de fichiers
'''
Ce script permet de chiffrer et déchiffrer des fichiers en utilisant la bibliothèque cryptography.
Il divise les fichiers en morceaux pour un traitement plus efficace et utilise une clé de chiffrement stockée dans un fichier. L'interface graphique est réalisée avec tkinter,
permettant à l'utilisateur de sélectionner des fichiers et des dossiers pour le chiffrement et le déchiffrement.
Je me suis servi des programmes crée pour le TIPE pour ajouter le multithreading afin d'augmenter la vitesse de chiffrement et déchiffrement des fichiers.
J'ai repris les fonctions de chiffrement et déchiffrement, en les adaptant pour qu'elles fonctionnent avec des morceaux de fichiers.
J'ai tout rassemblé dans le meme fichier pour vous en rendre qu'un seul. 
Le programme decoupe donc le fcihier en plusieurs morceaux, les chiffre ou les déchiffre en parallèle, puis les assemble pour créer le fichier final.
J'ai utilisé la bibliotheque concurrent.futures pour gérer le multithreading, ce qui permet de traiter plusieurs morceaux de fichier en même temps.
C'etait de mon point de vue la mieux adaptée pour gerer le multithreading de fichier afin de recuperer le fichier de sotrtie.
Les fonctions les plus importantes pour le projet sont celle qui utilise les chunks les autres sont celle faite pour le tipe legerement modifiées pour s'adapter au projet.
'''

# --- Crypto Functions ---
# génération de la clé
def generate_key(file_name, key_dir):
    key_path = os.path.join(key_dir, "key.key")
    os.makedirs(key_dir, exist_ok=True)

    if not os.path.exists(key_path):
        open(key_path, "w").close() # Crée le fichier de clés s'il n'existe pas
        os.chmod(key_path, 0o600) # Définit les permissions strictes pour le fichier de clés
    # Vérifie si la clé existe déjà
    with open(key_path, "r", encoding="utf-8") as key_file:
        for line in key_file.readlines(): # lit chaque ligne du fichier de clés
            try:
                fichier, cle = line.strip().split("|") # Sépare le nom du fichier et la clé
                # Vérifie si le nom du fichier correspond à celui pour lequel on génère la clé
                if fichier == file_name:
                    return cle.encode() # Retourne la clé encodée si elle existe déjà
            except ValueError:
                print(f"[Erreur] Ligne incorrecte dans le fichier de clés : {line.strip()}")
    # Génération d'une nouvelle clé si aucune clé existante n'a été trouvée
    new_key = Fernet.generate_key() # génère une nouvelle clé de chiffrement
    # Ajoute la nouvelle clé au fichier de clés avec la semantic "nom_fichier|clé"
    with open(key_path, "a", encoding="utf-8") as key_file:
        key_file.write(f"{file_name}|{new_key.decode()}\n")
    print(f"[Info] Nouvelle clé générée pour {file_name}")
    return new_key

# Fonction pour chiffrer un morceau de fichier
def encrypt_chunk(file_path, chunk_index, key, chunk_size):
    chunk_name = f"{file_path}_part{chunk_index}" # nom du morceau
    with open(file_path, "rb") as f: 
        f.seek(chunk_index * chunk_size) # se déplace au début du morceau pour le lire et le crypter comme il faut
        chunk_data = f.read(chunk_size) # lit le morceau de données

     # Chiffrement du morceau
    if chunk_data:
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(chunk_data) # chiffrement des chunk_data
        with open(chunk_name, "wb") as chunk_file:
            chunk_file.write(encrypted_data) # écrit le morceau chiffré dans un fichier

    return chunk_name

# Fonction pour assembler les morceaux chiffrés
def assemble_encrypted_file(output_path, chunks):
    try:
        chunks.sort(key=lambda x: int(x.split('_part')[-1])) # trie les morceaux par leur index
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
                final_file.write(chunk_file.read()) # lit le morceau chiffré et l'écrit dans le fichier final
    print(f"[Succès] Fichier assemblé sous {output_path}")
    return True

# Fonction pour nettoyer les morceaux temporaires
def cleanup_chunks(chunks):
    for chunk in chunks:
        try:
            os.remove(chunk) # supprime le morceau temporaire un par un
        except FileNotFoundError:
            print(f"[Avertissement] Le morceau {chunk} n'existe pas ou a déjà été supprimé.")

# Fonction principale de cryptage
def encrypt_file(file_path, output_dir, key_dir, num_chunks=4):
    file_name = os.path.basename(file_path) # nom du fichier à chiffrer
    key = generate_key(file_name, key_dir) # génère ou récupère la clé de chiffrement
    file_size = os.path.getsize(file_path) # taille du fichier à chiffrer
    chunk_size = math.ceil(file_size / num_chunks) # taille de chaque morceau

    with ThreadPoolExecutor(max_workers=num_chunks) as executor: # exécute le chiffrement en parallèle
        chunks = list(executor.map( 
            lambda i: encrypt_chunk(file_path, i, key, chunk_size), # mappe chaque morceau à la fonction de chiffrement
            range(num_chunks) # itère sur le nombre de morceaux
        ))

    # Assemblage des morceaux chiffrés
    output_file = os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}_encrypted{os.path.splitext(file_name)[1]}") # nom du fichier de sortie
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
        lignes = key_file.readlines() # lit toutes les lignes du fichier de clés

    for ligne in lignes:
        ligne = ligne.strip()
        if not ligne: # Ignore les lignes vides
            continue
        try:
            fichier, cle = ligne.split("|") # Sépare le fichier et la clé
            base, ext = os.path.splitext(fichier) # Sépare le nom de base et l'extension du fichier 
            fichier = base + "_encrypted" + ext # Ajoute le suffixe "_encrypted"
            L2 = os.path.basename(doc) # Récupère le nom de base du document à déchiffrer
            if fichier == L2: # Vérifie si c'est la bonne clé
                return cle.encode() # Convertit la clé en format binaire
        except ValueError:
            continue

    raise ValueError(f"Aucune clé trouvée pour {doc}") # Lève une exception si aucune clé n'est trouvée

# Fonction pour déchiffrer un morceau spécifique
def decrypt_chunk(chunk, fernet):
    with open(chunk, "rb") as chunk_file: # Ouvre le morceau en mode binaire
        encrypted_data = chunk_file.read() # lit les données chiffrées du morceau
        decrypted_data = fernet.decrypt(encrypted_data) # déchiffre les données
    return decrypted_data, chunk

# Fonction principale de déchiffrement
def decrypt_file(doc_crypt, output_dir, key_dir, num_threads=4):
    doc_crypt = str(doc_crypt) # Convertit le chemin du document chiffré en chaîne de caractères
    output_dir = str(output_dir) # Convertit le chemin du dossier de sortie en chaîne de caractères
    key_dir = str(key_dir) # Convertit le chemin du dossier de clés en chaîne de caractères
    # Récupération de la clé
    key = load_key(doc_crypt, key_dir)
    fernet = Fernet(key)

    # Determine taille des chunks (meme logique que pour le cryptage)
    file_size = os.path.getsize(doc_crypt) # taille du fichier chiffré
    num_chunks = num_threads  # nombre de morceaux à créer (par défaut, le même que le nombre de threads)
    chunk_size = math.ceil(file_size / num_chunks) # taille de chaque morceau

    # Prepare output file
    base_name = os.path.basename(doc_crypt) # Reécupère le nom de base du fichier chiffré
    name, ext = os.path.splitext(base_name) # Sépare le nom et l'extension du fichier
    output_file = os.path.join(output_dir, f"{name.replace('_encrypted', '')}{ext}") # Nom du fichier de sortie sans le suffixe "_encrypted"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir) # Crée le dossier de sortie s'il n'existe pas

    # Diviser le fichier en morceaux
    # Crée une liste pour stocker les noms des morceaux
    chunk_files = []
    with open(doc_crypt, "rb") as infile:
        for i in range(num_chunks):
            chunk_data = infile.read(chunk_size) # lit un morceau de données du fichier chiffré
            # Si le morceau est vide, on arrête la boucle
            if not chunk_data:
                break
            chunk_name = f"{doc_crypt}_part{i}" # Nom du morceau
            # Écrit le morceau dans un fichier
            with open(chunk_name, "wb") as chunk_file:
                chunk_file.write(chunk_data) # écrit les données du morceau dans le fichier
            chunk_files.append(chunk_name) # ajoute le nom du morceau à la liste

    # Décryptage ckunk en parralelle
    decrypted_chunks = [None] * len(chunk_files) # Liste pour stocker les données déchiffrées meme taille que chunk_files
    # Utilise ThreadPoolExecutor pour déchiffrer les morceaux en parallèle
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = {executor.submit(decrypt_chunk, chunk, fernet): idx for idx, chunk in enumerate(chunk_files)} # soumet chaque morceau à la fonction de déchiffrement
        # Utilise as_completed pour traiter les résultats au fur et à mesure qu'ils sont disponibles
        for future in as_completed(futures):
            decrypted_data, chunk = future.result() # déchiffre les données du morceau
            idx = futures[future] # Récupère l'index du morceau
            decrypted_chunks[idx] = decrypted_data # stocke les données déchiffrées dans la liste
            os.remove(chunk) # Supprime le morceau après déchiffrement

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
executor = ThreadPoolExecutor(max_workers=4) # pour exécuter les tâches de chiffrement et déchiffrement en parallèle
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
    future = executor.submit(decrypt_file, fichier_selectionne, dossier_selectionne, dossier_clé) # déchiffre le fichier sélectionné
    def on_done(future):
        try:
            chemin = future.result()  # chemin du fichier déchiffré
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du décryptage : {e}")
        else:
            root.after(0, lambda: messagebox.showinfo("Succès", f"Fichier décrypté enregistré sous : {chemin}")) # Affiche un message de succès
    future.add_done_callback(on_done) # Ajoute un callback pour gérer le résultat du futur

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

lbl_fichier = tk.Label(root, text="Aucun fichier sélectionné", fg="blue", wraplength=480) # Label pour afficher le fichier sélectionné
lbl_fichier.pack(pady=5) 
tk.Button(root, text="📂 Choisir un fichier", command=choisir_fichier).pack(pady=5) # Bouton de choix de fichier

lbl_dossier = tk.Label(root, text="Aucun dossier sélectionné", fg="blue", wraplength=350, justify="center")
lbl_dossier.pack()
tk.Button(root, text="📁 Choisir un dossier", command=choisir_dossier).pack(pady=20) #Bouton choix dossier

lbl_clé = tk.Label(root, text="Aucun dossier clé sélectionné", fg="blue", wraplength=220)
lbl_clé.pack()
tk.Button(root, text="📁 Choisir un dossier clé", command=choisir_d_clé).pack(pady=20) #Bouton choix dossier

# Lancement de l'interface
root.mainloop()
