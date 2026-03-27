import os
import json
import hashlib
import sys

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.exceptions import InvalidSignature


# -----------------------------
# TASK 1: Generate SHA-256 Hash
# -----------------------------
def generate_hash(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while True:
            chunk = file.read(4096)
            if not chunk:
                break
            sha256.update(chunk)

    return sha256.hexdigest()


# -----------------------------
# TASK 2: Generate Manifest
# -----------------------------
def generate_manifest(directory):
    manifest = {}

    for filename in sorted(os.listdir(directory)):
        file_path = os.path.join(directory, filename)

        if os.path.isfile(file_path):
            manifest[filename] = generate_hash(file_path)

    with open("metadata.json", "w") as f:
        json.dump(manifest, f, indent=4)

    print("metadata.json created successfully.")


# -----------------------------
# TASK 3: Check Integrity
# -----------------------------
def check_integrity(directory):
    if not os.path.exists("metadata.json"):
        print("[ERROR] metadata.json not found!")
        return

    with open("metadata.json", "r") as f:
        manifest = json.load(f)

    manifest_files = set(manifest.keys())

    for filename in sorted(manifest.keys()):
        old_hash = manifest[filename]
        file_path = os.path.join(directory, filename)

        if not os.path.exists(file_path):
            print(f"[MISSING] {filename} is missing!")
            continue

        new_hash = generate_hash(file_path)

        if new_hash != old_hash:
            print(f"[MODIFIED] {filename} has been modified!")
        else:
            print(f"[OK] {filename} is intact.")

    # 🔥 NEW FEATURE: detect added files
    current_files = {
        f for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f))
    }

    new_files = current_files - manifest_files

    for filename in sorted(new_files):
        print(f"[NEW FILE] {filename} was added and is not in metadata.json")


# -----------------------------
# TASK 4: Generate RSA Key Pair
# -----------------------------
def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    public_key = private_key.public_key()

    with open("private_key.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

    with open("public_key.pem", "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    print("RSA key pair generated successfully.")


# -----------------------------
# TASK 5: Sign metadata.json
# -----------------------------
def sign_file(file_to_sign):
    if not os.path.exists("private_key.pem"):
        print("private_key.pem not found!")
        return

    if not os.path.exists(file_to_sign):
        print(f"{file_to_sign} not found!")
        return

    with open("private_key.pem", "rb") as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None
        )

    with open(file_to_sign, "rb") as f:
        data = f.read()

    file_hash = hashlib.sha256(data).digest()

    signature = private_key.sign(
        file_hash,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    with open("signature.sig", "wb") as f:
        f.write(signature)

    print("File signed successfully. Signature saved in signature.sig")


# -----------------------------
# TASK 6: Verify Signature
# -----------------------------
def verify_signature(file_to_verify):
    if not os.path.exists("public_key.pem"):
        print("public_key.pem not found!")
        return

    if not os.path.exists("signature.sig"):
        print("signature.sig not found!")
        return

    if not os.path.exists(file_to_verify):
        print(f"{file_to_verify} not found!")
        return

    with open("public_key.pem", "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())

    with open(file_to_verify, "rb") as f:
        data = f.read()

    with open("signature.sig", "rb") as f:
        signature = f.read()

    file_hash = hashlib.sha256(data).digest()

    try:
        public_key.verify(
            signature,
            file_hash,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print("Verification SUCCESS: file is authentic and unchanged.")
    except InvalidSignature:
        print("Verification FAILED: file was changed or signature is invalid.")


# -----------------------------
# SIMPLE CLI
# -----------------------------
def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python main.py manifest <directory>")
        print("  python main.py check <directory>")
        print("  python main.py genkeys")
        print("  python main.py sign <file>")
        print("  python main.py verify <file>")
        return

    command = sys.argv[1]

    if command == "manifest":
        if len(sys.argv) != 3:
            print("Usage: python main.py manifest <directory>")
            return
        generate_manifest(sys.argv[2])

    elif command == "check":
        if len(sys.argv) != 3:
            print("Usage: python main.py check <directory>")
            return
        check_integrity(sys.argv[2])

    elif command == "genkeys":
        generate_keys()

    elif command == "sign":
        if len(sys.argv) != 3:
            print("Usage: python main.py sign <file>")
            return
        sign_file(sys.argv[2])

    elif command == "verify":
        if len(sys.argv) != 3:
            print("Usage: python main.py verify <file>")
            return
        verify_signature(sys.argv[2])

    else:
        print("Invalid command.")


if __name__ == "__main__":
    main()