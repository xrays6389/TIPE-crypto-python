from cryptography.fernet import Fernet
import os

#V1.0

# Fonction pour charger la clé depuis un fichier
def load_key():
    key_path = r"d:\Baptiste\Perso\CPE Prépa\TIPE crypto python\key.key"
    with open(key_path, "rb") as key_file:
        return key_file.read()

# Fonction de déchiffrement
def decrypto(doc_crypt, key):
    fernet = Fernet(key)

    # Lecture du fichier crypté
    chemin = os.path.join(r"d:\Baptiste\Perso\CPE Prépa\TIPE crypto python", doc_crypt) 
    with open(chemin, "rb") as enc_file:
        encrypted_data = enc_file.read()

    # Déchiffrement des données
    decrypted_data = fernet.decrypt(encrypted_data)

    # Écriture du fichier déchiffré
    fichier_sortie = "fichier_decrypte.txt"
    chemin_sortie = os.path.join(r"d:\Baptiste\Perso\CPE Prépa\TIPE crypto python", fichier_sortie)
    with open(chemin_sortie, "wb") as dec_file:
        dec_file.write(decrypted_data)

    return chemin_sortie

# Chargement de la clé
key = load_key()

# Nom du fichier crypté
fichier_crypté = "test2.txt"  

# Déchiffrement du fichier
fichier_decrypte = decrypto(fichier_crypté, key)
print(f"Fichier déchiffré sauvegardé sous : {fichier_decrypte}")
