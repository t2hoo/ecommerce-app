import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet
import os

# Key Management (Ensure the same key is used for encryption and decryption)
KEY_FILE = "secret.key"

def generate_key():
    """Generate and save the key."""
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)

def load_key():
    """Load the encryption key."""
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as key_file:
            return key_file.read()
    else:
        messagebox.showerror("Error", "Key file not found!")
        return None

# Encryption and Decryption Functions
def encrypt_password(password):
    key = load_key()
    if key:
        fernet = Fernet(key)
        return fernet.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password):
    key = load_key()
    if key:
        fernet = Fernet(key)
        try:
            return fernet.decrypt(encrypted_password.encode()).decode()
        except Exception as e:
            messagebox.showerror("Error", "Decryption failed!")
            return None

# GUI Functions
def handle_encrypt():
    password = password_entry.get()
    if password:
        encrypted = encrypt_password(password)
        if encrypted:
            result_entry.delete(0, tk.END)
            result_entry.insert(0, encrypted)
    else:
        messagebox.showwarning("Warning", "Please enter a password to encrypt.")

def handle_decrypt():
    encrypted_password = result_entry.get()
    if encrypted_password:
        decrypted = decrypt_password(encrypted_password)
        if decrypted:
            password_entry.delete(0, tk.END)
            password_entry.insert(0, decrypted)
    else:
        messagebox.showwarning("Warning", "Please enter an encrypted password to decrypt.")

# Generate key on startup
generate_key()

# GUI Setup
root = tk.Tk()
root.title("Django Oracle Password Encryption/Decryption")

# Input Fields
tk.Label(root, text="Password:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
password_entry = tk.Entry(root, width=30)
password_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Result:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
result_entry = tk.Entry(root, width=30)
result_entry.grid(row=1, column=1, padx=10, pady=10)

# Buttons
encrypt_button = tk.Button(root, text="Encrypt", command=handle_encrypt)
encrypt_button.grid(row=2, column=0, padx=10, pady=10)

decrypt_button = tk.Button(root, text="Decrypt", command=handle_decrypt)
decrypt_button.grid(row=2, column=1, padx=10, pady=10)

# Start GUI
root.mainloop()
