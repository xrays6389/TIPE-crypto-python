import os
import threading
from cryptography.fernet import Fernet

class KeyManager:
    """Gestion des clés de cryptage et décryptage."""
    
    def __init__(self, ch_dep):
        self.key_file = os.path.join(ch_dep, "key.key")
        if not os.path.exists(self.key_file):
            with open(self.key_file, "w", encoding="utf-8") as f:
                pass  # Crée un fichier vide si inexistant

    def get_key(self, fichier):
        """Récupère la clé associée à un fichier donné."""
        with open(self.key_file, "r", encoding="utf-8") as file:
            lignes = file.readlines()
        
        for ligne in lignes:
            nom_fichier, cle = ligne.strip().split("|")
            if nom_fichier == fichier:
                return cle.encode()  # Retourne la clé en bytes
        
        raise ValueError(f"Aucune clé trouvée pour {fichier}")

    def generate_key(self, fichier):
        """Génère une nouvelle clé et l'associe à un fichier."""
        key = Fernet.generate_key().decode()  # Convertit en string pour stockage
        with open(self.key_file, "a", encoding="utf-8") as file:
            file.write(f"{fichier}|{key}\n")  # Stocke la clé
        
        return key.encode()  # Retourne la clé en bytes


class CryptoManager:
    """Effectue les opérations de cryptage et décryptage avec threading."""

    def __init__(self, key_manager):
        self.key_manager = key_manager

    def cryptage(self, doc, ch_dep, callback=None):
        """Lance le cryptage dans un thread."""
        thread = threading.Thread(target=self._cryptage_worker, args=(doc, ch_dep, callback))
        thread.start()

    def _cryptage_worker(self, doc, ch_dep, callback):
        """Crypte le fichier et exécute le callback à la fin."""
        base, ext = os.path.splitext(doc)
        fichier_crypte = base + "_crypt" + ext
        chemin_sortie = os.path.join(ch_dep, fichier_crypte)

        # Vérifie si une clé existe déjà, sinon en génère une nouvelle
        try:
            key = self.key_manager.get_key(fichier_crypte)
        except ValueError:
            key = self.key_manager.generate_key(fichier_crypte)

        fernet = Fernet(key)

        # Lire et crypter le fichier
        with open(doc, "rb") as file:
            contenu = file.read()

        crypted_data = fernet.encrypt(contenu)

        # Sauvegarde du fichier crypté
        with open(chemin_sortie, "wb") as file:
            file.write(crypted_data)

        if callback:
            callback(f"Fichier crypté : {fichier_crypte}")

    def decrypto(self, doc_crypt, ch_dep, callback=None):
        """Lance le décryptage dans un thread."""
        thread = threading.Thread(target=self._decrypto_worker, args=(doc_crypt, ch_dep, callback))
        thread.start()

    def _decrypto_worker(self, doc_crypt, ch_dep, callback):
        """Déchiffre le fichier et exécute le callback à la fin."""
        base, ext = os.path.splitext(doc_crypt)
        
        # Vérifier si le fichier a bien le suffixe "_crypt"
        if not base.endswith("_crypt"):
            if callback:
                callback("Erreur : Le fichier ne semble pas être chiffré")
            return

        fichier_original = base[:-6] + ext  # Retire "_crypt"
        chemin_sortie = os.path.join(ch_dep, fichier_original)

        # Récupération de la clé associée
        try:
            key = self.key_manager.get_key(doc_crypt)
            fernet = Fernet(key)

            # Lire et décrypter le fichier
            with open(os.path.join(ch_dep, doc_crypt), "rb") as file:
                encrypted_data = file.read()

            decrypted_data = fernet.decrypt(encrypted_data)

            # Sauvegarde du fichier déchiffré
            with open(chemin_sortie, "wb") as file:
                file.write(decrypted_data)

            if callback:
                callback(f"Fichier déchiffré : {fichier_original}")

        except ValueError:
            if callback:
                callback(f"Erreur : Aucune clé trouvée pour {doc_crypt}")


# --- Utilisation avec Threading ---
def afficher_resultat(message):
    """Callback qui affiche le résultat dans la console."""
    print(message)

# Initialisation des classes avec le chemin du dossier
ch_dep = choisir_dossier()  # Sélection du dossier
key_manager = KeyManager(ch_dep)
crypto_manager = CryptoManager(key_manager)

# Sélection du fichier
doc = choisir_fichier()

# Cryptage du fichier
crypto_manager.cryptage(doc, ch_dep, callback=afficher_resultat)

# Décryptage du fichier après cryptage
crypto_manager.decrypto(doc + "_crypt", ch_dep, callback=afficher_resultat)
