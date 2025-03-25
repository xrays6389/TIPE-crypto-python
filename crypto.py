from cryptography.fernet import Fernet
import os

#V1.0
#Version qui genere un nouveau fichier avec le contenu crypté

def cryptage(doc): 
     # Génération et sauvegarde de la clé
    key = Fernet.generate_key()
    with open(r"d:\Baptiste\Perso\CPE Prépa\TIPE crypto python\key.key", "wb") as key_file: #w ecrase l'ancien contenu du fichier (pas possible de crypter deux documents)
        key_file.write(key)

    #recupere le fichier a crypter et l'encode en bytes
    with open(doc, "r", encoding="utf-8") as file:
        contenu = file.read().encode()  # Encodage en bytes ('.encode'=>transforme les caracteres en bytes)

    #cryptage du document
    fernet = Fernet(key)
    crypt=Fernet(key).encrypt(contenu) #crypte seulement des bytes

    # Écriture dans un nouveau fichier
    fichier_out = "fichier_crypte.txt"
    chemin = os.path.join(r"d:\\Baptiste\\Perso\\CPE Prépa\\TIPE crypto python", fichier_out) #permet d'enregistrer le fichier à l'emplacement voulu
    with open(chemin, "wb") as file:
        file.write(crypt)

    return fichier_out


doc = r"d:\Baptiste\Perso\CPE Prépa\TIPE crypto python\test.txt"

#permet de verifier que le fichier est bien trouvé par le programme
with open(doc, "r", encoding="utf-8") as file:
    contenu = file.read()
    print("Fichier trouvé et ouvert avec succès !")

#doc = input("Nom_fichier.txt :")
doc = doc.strip()
doc = cryptage(doc)
print (doc)



"""
#creer un fichier 
with open("fichier.txt", "w", encoding="utf-8") as fichier: pass 

#ecrire dans un fichier 
with open ("fichier.txt", "a", encoding="utf-8") as file : file.write("text")
"""

