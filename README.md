# TrustVerify 🔐

TrustVerify is a Python-based Command Line Interface (CLI) tool designed to ensure file integrity and authenticity using SHA-256 hashing and RSA digital signatures.

---

## 🎓 Course Information

* **Course:** SENG 473 – Information Security
* **Instructor:** Lect. Muhammet Mustafa Ölmez

---

## 👥 Group Members

* Maimuna Aminu Suleiman
* Zakariyya Zakariyya Suleiman
* Sidi Lamine Abdourahmane

---

## 🚀 Features

* Generate SHA-256 hashes for files
* Create a manifest (`metadata.json`)
* Detect file tampering (modified, missing, or new files)
* Generate RSA public/private key pairs
* Digitally sign files
* Verify authenticity using digital signatures

---

## 📁 Project Structure

```text
TrustVerify/
│
├── main.py
├── test_files/
│   └── example.txt
├── README.md
├── .gitignore
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/Mymunah30/TrustVerify.git
cd TrustVerify
```

Install dependencies:

```bash
pip install cryptography
```

---

## 🧪 Usage

Generate manifest:

```bash
python main.py manifest test_files
```

Check integrity:

```bash
python main.py check test_files
```

Generate RSA keys:

```bash
python main.py genkeys
```

Sign manifest:

```bash
python main.py sign metadata.json
```

Verify signature:

```bash
python main.py verify metadata.json
```

---

## 🔐 How It Works

* **Hashing (SHA-256)** ensures file integrity by detecting any changes in files
* **Digital Signatures (RSA)** ensure authenticity by verifying the identity of the sender
* Any modification in files or metadata results in verification failure

---

## 📌 Conclusion

TrustVerify demonstrates how combining hashing and digital signatures provides a secure system for verifying both the integrity and origin of files.

---

## 🔒 Security Note

The private key is excluded from the repository and should always be kept secret.
