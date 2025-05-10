from cryptography.fernet import Fernet
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Fonction pour charger la clé depuis un fichier
def load_key(doc, ch_clé):
    """Charge la clé de chiffrement depuis un fichier"""
    key_path = os.path.join(ch_clé, "key.key")
    
    if not os.path.exists(key_path):
        raise FileNotFoundError(f"Clé introuvable : {key_path}")

    # On s'assure que le nom du fichier à vérifier est une chaîne de caractères
    doc = os.path.basename(doc)  # Récupère uniquement le nom du fichier sans le chemin
    if isinstance(doc, bytes):
        doc = doc.decode("utf-8")

    with open(key_path, "r", encoding="utf-8") as key_file:
        for ligne in key_file:
            ligne = ligne.strip()
            if not ligne:  # Ignore les lignes vides
                continue
            
            try:
                fichier, cle = ligne.split("|")
                # Vérifie si le fichier correspond
                if fichier == doc:
                    # Retourne la clé encodée en bytes
                    return cle.strip().encode("utf-8")
            except ValueError:
                print(f"Erreur de format dans la ligne : {ligne}. Le format attendu est 'fichier|clé'.")
    
    raise ValueError(f"Aucune clé trouvée pour {doc}")

# Fonction pour déchiffrer un morceau spécifique
def decrypt_chunk(chunk, fernet):
    with open(chunk, "rb") as chunk_file:
        encrypted_data = chunk_file.read()
        decrypted_data = fernet.decrypt(encrypted_data)
    return decrypted_data, chunk

# Fonction de déchiffrement avec exécution parallèle
def decrypt_file(doc_crypt, output_dir, key_dir, num_threads=4):
    # Vérifie et convertit les chemins en chaînes de caractères
    doc_crypt = str(doc_crypt)
    output_dir = str(output_dir)
    key_dir = str(key_dir)

    # Charge la clé
    key = load_key(doc_crypt, key_dir)
    fernet = Fernet(key)

    # Détection des morceaux à déchiffrer
    base_name, ext = os.path.splitext(doc_crypt)
    chunks = sorted(
        [f for f in os.listdir() if f.startswith(base_name) and "_part" in f],
        key=lambda x: int(x.split('_part')[-1].split('.')[0])  # Sécuriser l'extraction du numéro de partie
    )

    if not chunks:
        raise FileNotFoundError(f"Aucun morceau trouvé pour {doc_crypt}")

    # Vérification de type explicite pour output_dir
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # Crée le répertoire s'il n'existe pas

    # Construction du fichier de sortie
    output_file = os.path.join(output_dir, f"{base_name[:-10] + ext}")

    # Ouverture du fichier de sortie en mode binaire
    with open(output_file, "wb") as final_file:
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            future_to_chunk = {executor.submit(decrypt_chunk, chunk, fernet): chunk for chunk in chunks}
            for future in as_completed(future_to_chunk):
                decrypted_data, chunk = future.result()  # Récupère les données déchiffrées et le morceau
                final_file.write(decrypted_data)
                os.remove(chunk)  # Supprimer le morceau après l'avoir traité

    print(f"[Succès] Fichier déchiffré sauvegardé sous {output_file}")
    return output_file
