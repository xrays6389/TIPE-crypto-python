from cryptography.fernet import Fernet
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Fonction pour charger la clé depuis un fichier
def load_key(doc, ch_clé):
    """Charge la clé de chiffrement depuis un fichier"""
    print(ch_clé)
    key_path = os.path.join(str(ch_clé) , "key.key")
    print (key_path)
    
    if not os.path.exists(key_path):
        raise FileNotFoundError(f"Clé introuvable : {key_path}")

  
    with open(key_path, "r", encoding="utf-8") as key_file:
        lignes = key_file.readlines()  # Lit toutes les lignes du fichier

    for ligne in lignes:
        ligne = ligne.strip()
        print (ligne)
        if not ligne:  # Ignore les lignes vides
            continue   
        
        try:
            fichier, cle = ligne.split("|")  # Sépare le fichier et la clé
            base, ext = os.path.splitext(fichier)
            fichier = base + "_encrypted" + ext
            L = doc.split("/")
            L2 = L[-1]
            print (L2)
            if fichier == L2:  # Vérifie si c'est la bonne clé
                return cle.encode()

        except ValueError:
            print(f"Erreur de format dans la ligne : {ligne}. Le format attendu est 'fichier|clé'.")
            continue  # Ignore les lignes mal formatées

    raise ValueError(f"Aucune clé trouvée pour {doc}")

# Fonction pour déchiffrer un morceau spécifique
def decrypt_chunk(chunk_path, fernet):
    with open(chunk_path, "rb") as f:
        encrypted_data = f.read()
    decrypted_data = fernet.decrypt(encrypted_data)
    return chunk_path, decrypted_data


# Fonction principale de déchiffrement
def decrypt_file(doc_crypt, output_dir, key_dir, num_threads=4):
    doc_crypt = str(doc_crypt)
    output_dir = str(output_dir)
    key_dir = str(key_dir)

    key = load_key(doc_crypt, key_dir)
    fernet = Fernet(key)

    base_name, ext = os.path.splitext(doc_crypt)
    prefix = base_name  # ex: document_encrypted

    # Liste des morceaux
    chunks = sorted(
        [f for f in os.listdir() if f.startswith(prefix) and "_part" in f],
        key=lambda x: int(x.split('_part')[-1].split('.')[0])
    )

    if not chunks:
        raise FileNotFoundError(f"Aucun morceau trouvé pour {doc_crypt}")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file = os.path.join(output_dir, base_name.replace("_encrypted", "") + ext)

    decrypted_chunks = {}

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = {executor.submit(decrypt_chunk, chunk, fernet): chunk for chunk in chunks}
        for future in futures:
            chunk_name, data = future.result()
            decrypted_chunks[chunk_name] = data

    with open(output_file, "wb") as f_out:
        for chunk in sorted(decrypted_chunks, key=lambda x: int(x.split('_part')[-1].split('.')[0])):
            f_out.write(decrypted_chunks[chunk])
            os.remove(chunk)

    print(f"[Succès] Fichier déchiffré sauvegardé sous {output_file}")
    return output_file