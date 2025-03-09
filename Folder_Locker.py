import os
import tkinter as tk
from tkinter import filedialog, messagebox, Text, END
from cryptography.fernet import Fernet
import base64
import platform

# Generate a key from the password
def generate_key(password):
    key = base64.urlsafe_b64encode(password.encode().ljust(32)[:32])
    return key

# Check if folder is encrypted
def is_folder_encrypted(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".enc"):
                return True
    return False

# Encrypt a folder
def encrypt_folder(folder_path, password):
    try:
        key = generate_key(password)
        fernet = Fernet(key)
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                encrypted_file_path = file_path + ".enc"
                
                with open(file_path, "rb") as f:
                    data = f.read()
                encrypted_data = fernet.encrypt(data)
                
                with open(encrypted_file_path, "wb") as f:
                    f.write(encrypted_data)
                
                os.remove(file_path)
        update_dashboard()
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Encryption failed: {str(e)}")
        return False

# Decrypt a folder
def decrypt_folder(folder_path, password):
    try:
        key = generate_key(password)
        fernet = Fernet(key)
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".enc"):
                    file_path = os.path.join(root, file)
                    decrypted_file_path = file_path[:-4]
                    
                    with open(file_path, "rb") as f:
                        encrypted_data = f.read()
                    decrypted_data = fernet.decrypt(encrypted_data)
                    
                    with open(decrypted_file_path, "wb") as f:
                        f.write(decrypted_data)
                    
                    os.remove(file_path)
        update_dashboard()
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Decryption failed: {str(e)}")
        return False

# Select folder and update dashboard
def select_folder():
    folder_path = filedialog.askdirectory()
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder_path)
    update_dashboard()

# Update dashboard information and warnings
def update_dashboard():
    folder_path = folder_entry.get()
    if folder_path:
        path_value.config(text=folder_path)
        status = "Locked" if is_folder_encrypted(folder_path) else "Unlocked"
        status_value.config(text=status)
        
        warning_text.delete(1.0, END)  # Clear previous text
        
        if status == "Unlocked":
            warning_text.insert(END, "Warning: Your folder is living its best unlocked life! If you want to slap a password on it and ruin its carefree vibes, go ahead and add one, then hit ")
            warning_text.insert(END, "'Apply Password'", "red")
            warning_text.insert(END, " Button —but don’t say we didn’t warn you when it starts sulking!")
            warning_text.tag_configure("red", foreground="#ff4444")  # Red for 'Apply Password'
            warning_text.config(fg="#00ff00")  # Green for the rest of the text
        else:
            warning_text.insert(END, "Alert: Your folder’s been chilling behind a password, locked up like it’s in folder jail! To bust it out and let it live its wild, unlocked dreams, type in the password and hit ")
            warning_text.insert(END, "'Remove Password'", "green")
            warning_text.insert(END, " Button —but watch out, it might throw a freedom party you weren’t invited to!")
            warning_text.tag_configure("green", foreground="#00ff00")  # Green for 'Remove Password'
            warning_text.config(fg="#ff4444")  # Red for the rest of the text
    else:
        path_value.config(text="None")
        status_value.config(text="N/A")
        warning_text.delete(1.0, END)
        warning_text.insert(END, "Please select a folder to see its status.")
        warning_text.config(fg=style["fg"])

# Apply encryption
def apply_password():
    folder_path = folder_entry.get()
    password = password_entry.get()
    if not folder_path or not password:
        messagebox.showwarning("Error", "Please select a folder and enter a password.")
        return
    if encrypt_folder(folder_path, password):
        messagebox.showinfo("Success", "Folder encrypted successfully!")

# Remove encryption
def remove_password():
    folder_path = folder_entry.get()
    password = password_entry.get()
    if not folder_path or not password:
        messagebox.showwarning("Error", "Please select a folder and enter a password.")
        return
    if decrypt_folder(folder_path, password):
        messagebox.showinfo("Success", "Folder decrypted successfully!")

# GUI Setup with Dark Theme
root = tk.Tk()
root.title("Folder Password Protector (Cross-Platform)")
root.geometry("800x600")
root.configure(bg="#2d2d2d")

# Theme settings
style = {
    "bg": "#2d2d2d",
    "fg": "#ffffff",
    "entry_bg": "#404040",
    "button_bg": "#555555",
    "button_fg": "#ffffff",
    "highlight": "#00b7eb"
}

# Heading
heading_label = tk.Label(root, text="Cyber Gyan Lock", font=("Helvetica", 20, "bold"),
                        bg=style["bg"], fg=style["highlight"])
heading_label.grid(row=0, column=0, columnspan=3, padx=20, pady=20)

# Folder Path
tk.Label(root, text="Folder Path:", bg=style["bg"], fg=style["fg"], 
         font=("Helvetica", 12)).grid(row=1, column=0, padx=20, pady=15, sticky="e")
folder_entry = tk.Entry(root, width=60, bg=style["entry_bg"], fg=style["fg"], 
                       insertbackground=style["fg"], font=("Helvetica", 12))
folder_entry.grid(row=1, column=1, padx=20, pady=15)
tk.Button(root, text="Browse", command=select_folder, bg=style["button_bg"], 
         fg=style["button_fg"], font=("Helvetica", 10)).grid(row=1, column=2, padx=20, pady=15)

# Password Entry
tk.Label(root, text="Password:", bg=style["bg"], fg=style["fg"], 
         font=("Helvetica", 12)).grid(row=2, column=0, padx=20, pady=15, sticky="e")
password_entry = tk.Entry(root, show="*", width=60, bg=style["entry_bg"], 
                         fg=style["fg"], insertbackground=style["fg"], font=("Helvetica", 12))
password_entry.grid(row=2, column=1, padx=20, pady=15)

# Dashboard in Table Form
dashboard_frame = tk.Frame(root, bg=style["bg"], bd=2, relief="groove")
dashboard_frame.grid(row=3, column=0, columnspan=3, padx=20, pady=20, sticky="ew")

# Table headers
tk.Label(dashboard_frame, text="Property", bg=style["bg"], fg=style["highlight"],
         font=("Helvetica", 12, "bold"), width=20).grid(row=0, column=0, padx=5, pady=5)
tk.Label(dashboard_frame, text="Value", bg=style["bg"], fg=style["highlight"],
         font=("Helvetica", 12, "bold"), width=50).grid(row=0, column=1, padx=5, pady=5)

# Table content
tk.Label(dashboard_frame, text="Selected Path:", bg=style["bg"], fg=style["fg"],
         font=("Helvetica", 11)).grid(row=1, column=0, padx=5, pady=5)
path_value = tk.Label(dashboard_frame, text="None", bg=style["bg"], fg=style["fg"],
                     font=("Helvetica", 11), anchor="w")
path_value.grid(row=1, column=1, padx=5, pady=5, sticky="w")

tk.Label(dashboard_frame, text="Status:", bg=style["bg"], fg=style["fg"],
         font=("Helvetica", 11)).grid(row=2, column=0, padx=5, pady=5)
status_value = tk.Label(dashboard_frame, text="N/A", bg=style["bg"], fg=style["fg"],
                       font=("Helvetica", 11), anchor="w")
status_value.grid(row=2, column=1, padx=5, pady=5, sticky="w")

# Warning Text (replacing warning_label with Text widget)
warning_text = tk.Text(root, height=4, wrap="word", bg=style["bg"], fg=style["fg"], 
                      borderwidth=0, font=("Helvetica", 11))
warning_text.grid(row=4, column=0, columnspan=3, padx=20, pady=10)

# Action Buttons (in one line)
button_frame = tk.Frame(root, bg=style["bg"])
button_frame.grid(row=5, column=0, columnspan=3, pady=15)

tk.Button(button_frame, text="Apply Password", command=apply_password, 
         bg=style["button_bg"], fg=style["button_fg"], 
         font=("Helvetica", 12), width=15).pack(side=tk.LEFT, padx=20)
tk.Button(button_frame, text="Remove Password", command=remove_password, 
         bg=style["button_bg"], fg=style["button_fg"], 
         font=("Helvetica", 12), width=15).pack(side=tk.LEFT, padx=20)

# Footer with OS info
footer_label = tk.Label(root, text=f"Created by Yash Makwana | Running on {platform.system()}", 
                       font=("Helvetica", 12), bg=style["bg"], fg=style["fg"])
footer_label.grid(row=6, column=0, columnspan=3, padx=20, pady=20)

root.mainloop()