from cryptography.fernet import Fernet
import os

#V1.2
#modification afin d'utiliser les fonctiuons a partir d'un autre programme

# Fonction pour charger la clé depuis un fichier
def load_key(ch_dep):
    key_path = os.path.join(ch_dep,"key.key")
    with open(key_path, "rb") as key_file:
        return key_file.read()

# Fonction de déchiffrement
def decrypto(doc_crypt, ch_dep, key):
    fernet = Fernet(key)

    # Lecture du fichier crypté
    chemin = os.path.join(ch_dep, doc_crypt) 
    with open(chemin, "rb") as enc_file:
        encrypted_data = enc_file.read()

    # Déchiffrement des données
    decrypted_data = fernet.decrypt(encrypted_data)

    # Écriture du fichier déchiffré
    fichier_sortie = doc_crypt
    chemin_sortie = os.path.join(os.path.join(ch_dep, fichier_sortie))
    with open(chemin_sortie, "wb") as dec_file:
        dec_file.write(decrypted_data)

    return chemin_sortie


