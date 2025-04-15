from cryptography.fernet import Fernet
import os
from threading import Thread

#a faire:
"""Ajout de theadring afin d'utliser des coeurs pour charger la clé et d'autres pour decrypter 
le fichier en plusieurs morceaux afin d'optimiser le temps de traitement"""



# Fonction pour charger la clé depuis un fichier
def load_key(doc, ch_clé):
    """Charge la clé de chiffrement depuis un fichier"""
    key_path = os.path.join(ch_clé, "key.key")
    
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
            fichier = base + "_crypt" + ext
            L = doc.split("/")
            L2 = L[-1]
            if fichier == L2:  # Vérifie si c'est la bonne clé
                return cle.encode()  # Convertit la clé en format binaire
        except ValueError:
            print(f"Erreur de format dans la ligne : {ligne}. Le format attendu est 'fichier|clé'.")
            continue  # Ignore les lignes mal formatées
    
    raise ValueError(f"Aucune clé trouvée pour {doc}")

# Fonction de déchiffrement
def decrypto(doc_crypt, ch_dep, key):
    fernet = Fernet(key)

    # Lecture du fichier crypté
    chemin = os.path.join(doc_crypt) 

    if not os.path.exists(chemin):
        raise FileNotFoundError(f"Fichier crypté introuvable : {chemin}")
    
    with open(chemin, "rb") as enc_file:
        encrypted_data = enc_file.read()

    # Déchiffrement des données
    decrypted_data = fernet.decrypt(encrypted_data)

    # Ajout d'un suffixe au fichier déchiffré
    base, ext = os.path.splitext(doc_crypt)
    if base.endswith("_crypt"):  # Vérifie si le fichier a bien été crypté avec le suffixe
        fichier_sortie = base[:-6] + ext  # Supprime "_crypt" du nom
        f_s = fichier_sortie.split("/")
        fichier_sortie = f_s[-1]
        print(fichier_sortie)
    else:
        fichier_sortie = "decrypted_" + doc_crypt  # Si pas de suffixe, on renomme avec "decrypted_"
        f_s = fichier_sortie.split("/")
        fichier_sortie = f_s[-1]

    # Écriture du fichier déchiffré
    os.remove(doc_crypt) # Supprime le document crypté
    chemin_sortie = os.path.join(ch_dep, fichier_sortie)
    with open(chemin_sortie, "wb") as dec_file:
        dec_file.write(decrypted_data)

    return chemin_sortie
