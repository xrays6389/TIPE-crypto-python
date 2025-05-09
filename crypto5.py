from cryptography.fernet import Fernet 
import os
import math
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=4)

def cryptage(doc, ch_dep, ch_clé): 
    key_path = os.path.join(ch_clé, "key.key")

    # Crée le fichier key.key s’il n’existe pas
    if not os.path.exists(key_path):
        with open(key_path, "w"): 
            pass  

    # Cherche si une clé existe déjà pour ce fichier
    key = None
    with open(key_path, "r", encoding="utf-8") as key_file:
        lignes = key_file.readlines()

    for ligne in lignes:
        ligne = ligne.strip()
        if not ligne:
            continue
        try:
            fichier, cle = ligne.split("|")
            if fichier == os.path.basename(doc):
                key = cle.encode()
                break
        except ValueError:
            print(f"Erreur de format dans la ligne : {ligne}")
            continue

    # Sinon, génère une nouvelle clé
    if not key:
        key = Fernet.generate_key()
        with open(key_path, "a", encoding="utf-8") as key_file:
            key_file.write(f"{os.path.basename(doc)}|{key.decode()}\n")
        print(f"Clé générée et stockée pour {os.path.basename(doc)}")

    fernet = Fernet(key)
    nb_parts = 4
    morceaux = []

    # Étape 1 : Découpage du fichier
    taille_fichier = os.path.getsize(doc)
    taille_morceau = math.ceil(taille_fichier / nb_parts)

    with open(doc, "rb") as file:
        for i in range(nb_parts):
            morceau = file.read(taille_morceau)
            if not morceau:
                break
            nom_morceau = f"{doc}_part{i}"
            with open(nom_morceau, 'wb') as f_part:
                f_part.write( morceau)
            morceaux.append(nom_morceau)

    # Étape 2 : Chiffrement parallèle
    def chiffrer_fichier(nom_fichier):
        with open(nom_fichier, 'rb') as f:
            contenu = f.read()
        return fernet.encrypt(contenu)

    with ThreadPoolExecutor(max_workers=nb_parts) as executor:
        futures = [executor.submit(chiffrer_fichier, fichier) for fichier in morceaux]
        fichiers_chiffres = [f.result() for f in futures]

    # Étape 3 : Concaténation
    crypt = b''.join(fichiers_chiffres)

    # Étape 4 : Déterminer le nom de sortie
    base, ext = os.path.splitext(doc)
    fichier_crypte = os.path.basename(base + "_crypt" + ext)
    chemin = os.path.join(ch_dep, fichier_crypte)

    # Étape 5 : Suppression de l’original
    os.remove(doc)

    # Étape 6 : Écriture du fichier chiffré
    with open(chemin, "wb") as file:
        file.write(crypt)

    # Étape 7 : Nettoyage des morceaux
    for morceau in morceaux:
        os.remove(morceau)

    return chemin  # Chemin du fichier chiffré