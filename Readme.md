# 📁 Password Manager (Encryption)
**CodTech IT Solutions — Python Programming Internship**  
Task name : Password Manager (Encryption)   
Intern : SHRIRAM K N  
Intern ID  : CITS8258  
Domain : Python Programming  
Duration : 4 Weeks  
Internship Period : 22 June 2026 - 20 July 2026

## 📌 Project Overview🖥️ GUI Interface

The **Password Manager (Encryption)**, this project focuses on securely storing user credentials by encrypting sensitive data before saving it to a local file. It aims to prevent unauthorized access to personal accounts by ensuring that even if the storage file is intercepted, the passwords remain encrypted and unreadable without the Master Password.

## ✨ Features
| Feature | Description |
|---------|-------------|
| 🔒 Strong Encryption | Secures stored passwords using robust encryption (e.g., AES/Fernet) so data is unreadable at rest. |
| 🔑 Master Password | Protects your entire password vault with a single, secure master key. |
| ➕ Add Credentials | Easily save website, email/username, and password combinations. |
| 👁️ Retrieve & Search | Instantly search for saved websites to decrypt and view or copy your passwords. |
| 🛡️ Local Storage | Data is saved locally on your machine, ensuring you have full control over your vault. |
| 🖥️ GUI Interface | A user-friendly graphical interface built with Tkinter for seamless interaction. |


## 🛠️ Technologies Used

- **Language** : Python 3.x
- **Core Libraries** :  cryptography (or base64 / hashlib) - For encrypting and decrypting data
```

```
##  Project Scope
This project focuses on securely storing user credentials by encrypting sensitive data before saving it to a local file. It aims to prevent unauthorized access to personal accounts by ensuring that even if the storage file is intercepted, the passwords remain encrypted and unreadable without the Master Password.
```

```
##  Technologies Used
1.Python  
2.OS Module  
3.cryptography Module  
```

```
##  Features
1.Keeps stored passwords secure and unreadable. 
2.One key unlocks your entire vault. 
3.Quickly add, search, and retrieve logins.
4.Data stays completely private on your own device.
5.Easy-to-use graphical design (GUI).
```

```
## Project Structure
password-manager/  
│  
├── main.py               ← Main Python script (GUI and encryption logic)  
├── data.json             ← Local storage file for encrypted data (Auto-generated)  
└── README.md             ← Project documentation 
```

```
## How It Works (Step-by-Step)
Step 1 → User launches the app and sets/enters the Master Password  
         ↓  
Step 2 → Script authenticates the Master Password  
         ↓  
Step 3 → User inputs new account details (Website, Username, Password)  
         ↓  
Step 4 → Script encrypts the password using a cryptographic key  
         ↓  
Step 5 → Encrypted data is saved securely into a local file (e.g., JSON or TXT)  
         ↓  
Step 6 → When searching, the user enters the website name  
         ↓  
Step 7 → Script locates the entry, decrypts the password using the Master Key, and displays it
```

```
## Conclusion
This Password Manager efficiently secures digital identities, reducing the risk of compromised accounts and eliminating the need to memorize multiple complex passwords. The project demonstrates proficiency in Python programming, applied cryptography, secure file handling, and GUI development using Tkinter.
