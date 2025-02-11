import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# Define common ransomware extensions and signatures
ransomware_extensions = ['.locked', '.encrypted', '.crypt']

def analyze_ransomware(file_path):
    """
    Analyzes the encrypted file and attempts to determine the ransomware used
    based on known extensions or patterns.
    """
    if os.path.exists(file_path):
        _, file_extension = os.path.splitext(file_path)
        if file_extension.lower() in ransomware_extensions:
            return True, "Potential Ransomware detected: Extension match"
        else:
            return False, "No known ransomware signature detected"
    else:
        return False, "File does not exist"

def decrypt_file(encrypted_file_path, key):
    """
    Decrypts an AES-encrypted file using the provided key.
    """
    try:
        with open(encrypted_file_path, 'rb') as file:
            encrypted_data = file.read()
        
        # Extract the IV (first 16 bytes) and the actual encrypted data
        iv = encrypted_data[:AES.block_size]
        encrypted_data = encrypted_data[AES.block_size:]
        
        # Ensure the encrypted data is padded to 16 byte boundary
        if len(encrypted_data) % AES.block_size != 0:
            raise ValueError("Data must be padded to 16 byte boundary in CBC mode")
        
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
        
        decrypted_file_path = encrypted_file_path.replace(".locked", ".decrypted")
        with open(decrypted_file_path, 'wb') as decrypted_file:
            decrypted_file.write(decrypted_data)
        
        return decrypted_file_path, "Decryption successful."
    except Exception as e:
        return None, f"Error during decryption: {str(e)}"

class RansomwareDecryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ransomware Decryption Tool")
        self.root.geometry("600x400")
        self.root.configure(bg="#1F2A34")  # Dark background for cybersecurity theme
        
        # Custom fonts and colors for a modern look
        self.font_style = ("Helvetica", 14)
        self.button_style = {'font': ("Helvetica", 12, "bold"), 'bg': "#1ABC9C", 'fg': "#ECF0F1", 'relief': "flat", 'width': 20, 'height': 2}
        self.button_hover_style = {'bg': "#16A085", 'fg': "#FFFFFF"}

        self.label = tk.Label(root, text="Select an encrypted file to decrypt", font=("Helvetica", 16, "bold"), fg="#ECF0F1", bg="#1F2A34")
        self.label.pack(pady=30)
        
        self.select_button = tk.Button(root, text="Select File", **self.button_style, command=self.select_file)
        self.select_button.pack(pady=10)
        
        self.decrypt_button = tk.Button(root, text="Decrypt File", **self.button_style, state=tk.DISABLED, command=self.decrypt_file)
        self.decrypt_button.pack(pady=10)
        
        self.selected_file = None
        
        # Hover effect for buttons
        self.select_button.bind("<Enter>", lambda e: self.on_hover(self.select_button))
        self.select_button.bind("<Leave>", lambda e: self.on_leave(self.select_button))
        self.decrypt_button.bind("<Enter>", lambda e: self.on_hover(self.decrypt_button))
        self.decrypt_button.bind("<Leave>", lambda e: self.on_leave(self.decrypt_button))
    
    def on_hover(self, button):
        button.config(**self.button_hover_style)
    
    def on_leave(self, button):
        button.config(**self.button_style)
    
    def select_file(self):
        self.selected_file = filedialog.askopenfilename(title="Select Encrypted File", filetypes=[("All Files", "*.*")])
        if self.selected_file:
            is_ransomware, message = analyze_ransomware(self.selected_file)
            if is_ransomware:
                messagebox.showinfo("Analysis Result", message)
                self.decrypt_button.config(state=tk.NORMAL)
            else:
                messagebox.showwarning("Analysis Result", message)
                self.decrypt_button.config(state=tk.DISABLED)
    
    def decrypt_file(self):
        if self.selected_file:
            # Prompt the user to enter the decryption key
            key = simpledialog.askstring("Decryption Key", "Enter the 16-byte decryption key:", parent=self.root)
            if key:
                # Convert the key to bytes and ensure it is 16 bytes long
                key = key.encode('utf-8')
                if len(key) < 16:
                    # Pad the key with null bytes if it is too short
                    key += b'\x00' * (16 - len(key))
                elif len(key) > 16:
                    # Truncate the key if it is too long
                    key = key[:16]
                
                decrypted_file, message = decrypt_file(self.selected_file, key)
                if decrypted_file:
                    messagebox.showinfo("Decryption Success", f"File decrypted successfully! Saved as: {decrypted_file}")
                else:
                    messagebox.showerror("Decryption Error", message)

# Run the GUI application
if __name__ == "__main__":
    root = tk.Tk()
    app = RansomwareDecryptionApp(root)
    root.mainloop()
