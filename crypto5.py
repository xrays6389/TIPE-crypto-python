import os
import math
from cryptography.fernet import Fernet
from concurrent.futures import ThreadPoolExecutor


def generate_key(file_name, key_dir):
    key_path = os.path.join(key_dir, "key.key")
    os.makedirs(key_dir, exist_ok=True)

    if not os.path.exists(key_path):
        open(key_path, "w").close()
        os.chmod(key_path, 0o600)  # Permissions strictes pour la sécurité

    with open(key_path, "r", encoding="utf-8") as key_file:
        for line in key_file.readlines():
            try:
                fichier, cle = line.strip().split("|")
                if fichier == file_name:
                    return cle.encode()
            except ValueError:
                print(f"[Erreur] Ligne incorrecte dans le fichier de clés : {line.strip()}")

    # Génération d'une nouvelle clé si aucune clé existante n'a été trouvée
    new_key = Fernet.generate_key()
    with open(key_path, "a", encoding="utf-8") as key_file:
        key_file.write(f"{file_name}|{new_key.decode()}\n")
    print(f"[Info] Nouvelle clé générée pour {file_name}")
    return new_key


def encrypt_chunk(file_path, chunk_index, key, chunk_size):
    chunk_name = f"{file_path}_part{chunk_index}"
    with open(file_path, "rb") as f:
        f.seek(chunk_index * chunk_size)
        chunk_data = f.read(chunk_size)

    if chunk_data:
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(chunk_data)
        with open(chunk_name, "wb") as chunk_file:
            chunk_file.write(encrypted_data)

    return chunk_name


def assemble_encrypted_file(output_path, chunks):
    with open(output_path, "wb") as final_file:
        for chunk in chunks:
            with open(chunk, "rb") as chunk_file:
                final_file.write(chunk_file.read())


def cleanup_chunks(chunks):
    for chunk in chunks:
        try:
            os.remove(chunk)
        except FileNotFoundError:
            print(f"[Avertissement] Le morceau {chunk} n'existe pas ou a déjà été supprimé.")


def encrypt_file(file_path, output_dir, key_dir, num_chunks=4):
    file_name = os.path.basename(file_path)
    key = generate_key(file_name, key_dir)
    file_size = os.path.getsize(file_path)
    chunk_size = math.ceil(file_size / num_chunks)

    with ThreadPoolExecutor(max_workers=num_chunks) as executor:
        chunks = list(executor.map(
            lambda i: encrypt_chunk(file_path, i, key, chunk_size),
            range(num_chunks)
        ))

    output_file = os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}_encrypted{os.path.splitext(file_name)[1]}")
    assemble_encrypted_file(output_file, chunks)
    cleanup_chunks(chunks)

    os.remove(file_path)  # Suppression du fichier original
    print(f"[Succès] Fichier chiffré sauvegardé sous {output_file}")
    return output_file
