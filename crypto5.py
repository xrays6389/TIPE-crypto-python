from cryptography.fernet import Fernet 
import os

#V1.4
#potentiel probleme lors de generation de clé ou de cryptage reglé ainsi qu'ajout d'un suffixe au fichier


def cryptage(doc,ch_dep,ch_clé): 

    key_path = os.path.join(ch_clé, "key.key")

    # Vérifie si le fichier key.key existe, sinon le crée
    if not os.path.exists(key_path):
        with open(key_path, "w") as key_file: 
            pass  
        
    # Vérifie si le fichier key.key contient déjà une clé pour ce fichier
    with open(key_path, "r", encoding="utf-8") as key_file:
        lignes = key_file.readlines()  # Lire toutes les lignes du fichier de clés

    for ligne in lignes:
        ligne = ligne.strip()

        if not ligne:  # Ignore les lignes vides
            continue
        
        try:
            fichier, cle = ligne.split("|")  # Sépare le nom du fichier et la clé
            if fichier == os.path.basename(doc):  # Si le fichier à crypter a déjà une clé
                key = cle.encode()  # Récupère la clé existante au lieu d'en créer une nouvelle
                break
        except ValueError:
            print(f"Erreur de format dans la ligne : {ligne}. Le format attendu est 'fichier|clé'.")
            continue  # Ignore les lignes mal formatées

    else:
        # Si aucune clé n'a été trouvée, on génère une nouvelle clé et on l'ajoute au fichier de clés
        try:
            key = Fernet.generate_key()
            L2 = os.path.basename(doc)  # Récupère directement le nom du fichier
    
            with open(key_path, "a", encoding="utf-8") as key_file:
                key_file.write(f"{L2}|{key.decode()}\n")

            print(f"Clé générée et stockée pour {L2}")

        except Exception as e:
            print(f"Erreur : {e}")

    # Lire le fichier et le convertir en bytes
    with open(doc, "rb") as file:
        contenu = file.read()

    # Cryptage du document
    fernet = Fernet(key)
    crypt=Fernet(key).encrypt(contenu) #crypte seulement des bytes

    base, ext = os.path.splitext(doc)
    fichier_crypte = base + "_crypt" + ext
    print(fichier_crypte)
    chemin = os.path.join(ch_dep, fichier_crypte)

    # Écriture du fichier crypté
    os.remove(doc) # Supprime le document original
    with open(chemin, "wb") as file:
        file.write(crypt)

    return fichier_crypte

# test le programme
"""
ch = r"d:\Baptiste\Perso\CPE Prépa\TIPE crypto python"
doc = r"d:\Baptiste\Perso\CPE Prépa\TIPE crypto python\antho.txt"
doc = doc.strip()
doc = cryptage(doc,ch)
print (doc)
"""