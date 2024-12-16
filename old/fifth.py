import os
import subprocess
import customtkinter as ctk
from tkinter import filedialog, messagebox

# Set the appearance mode and color theme
ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

class SteganographyApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Steganography Tool")
        self.geometry("500x700")

        # Ensure necessary directories exist
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.encode_dir = os.path.join(self.base_dir, 'encoded')
        self.decode_dir = os.path.join(self.base_dir, 'decoded')
        os.makedirs(self.encode_dir, exist_ok=True)
        os.makedirs(self.decode_dir, exist_ok=True)

        # Path to steghide executable (now relative to script)
        self.steghide_path = os.path.join(self.base_dir, 'steghide', 'steghide.exe')

        # Create tabview
        self.tabview = ctk.CTkTabview(self, width=450)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)

        # Encode Tab
        self.encode_tab = self.tabview.add("Encode")
        self.create_encode_tab()

        # Decode Tab
        self.decode_tab = self.tabview.add("Decode")
        self.create_decode_tab()

    def create_encode_tab(self):
        # Carrier File
        self.carrier_label = ctk.CTkLabel(self.encode_tab, text="Carrier File:", font=("Arial", 14))
        self.carrier_label.pack(pady=(10, 5), anchor="w", padx=20)
        
        self.carrier_frame = ctk.CTkFrame(self.encode_tab)
        self.carrier_frame.pack(pady=5, padx=20, fill="x")
        
        self.carrier_entry = ctk.CTkEntry(self.carrier_frame, width=350)
        self.carrier_entry.pack(side="left", expand=True, fill="x", padx=(0, 10))
        
        self.carrier_button = ctk.CTkButton(
            self.carrier_frame, 
            text="Browse", 
            width=100, 
            command=self.upload_carrier_encode
        )
        self.carrier_button.pack(side="right")

        # Secret File
        self.secret_label = ctk.CTkLabel(self.encode_tab, text="Secret File:", font=("Arial", 14))
        self.secret_label.pack(pady=(10, 5), anchor="w", padx=20)
        
        self.secret_frame = ctk.CTkFrame(self.encode_tab)
        self.secret_frame.pack(pady=5, padx=20, fill="x")
        
        self.secret_entry = ctk.CTkEntry(self.secret_frame, width=350)
        self.secret_entry.pack(side="left", expand=True, fill="x", padx=(0, 10))
        
        self.secret_button = ctk.CTkButton(
            self.secret_frame, 
            text="Browse", 
            width=100, 
            command=self.upload_secret_encode
        )
        self.secret_button.pack(side="right")

        # Password
        self.password_label = ctk.CTkLabel(self.encode_tab, text="Password:", font=("Arial", 14))
        self.password_label.pack(pady=(10, 5), anchor="w", padx=20)
        
        self.password_entry = ctk.CTkEntry(self.encode_tab, show="*", width=450)
        self.password_entry.pack(pady=5, padx=20)

        # Encode Button
        self.encode_button = ctk.CTkButton(
            self.encode_tab, 
            text="Encode", 
            font=("Arial", 16), 
            command=self.encode_action
        )
        self.encode_button.pack(pady=20)

    def create_decode_tab(self):
        # Carrier File
        self.decode_carrier_label = ctk.CTkLabel(self.decode_tab, text="Carrier File:", font=("Arial", 14))
        self.decode_carrier_label.pack(pady=(10, 5), anchor="w", padx=20)
        
        self.decode_carrier_frame = ctk.CTkFrame(self.decode_tab)
        self.decode_carrier_frame.pack(pady=5, padx=20, fill="x")
        
        self.decode_carrier_entry = ctk.CTkEntry(self.decode_carrier_frame, width=350)
        self.decode_carrier_entry.pack(side="left", expand=True, fill="x", padx=(0, 10))
        
        self.decode_carrier_button = ctk.CTkButton(
            self.decode_carrier_frame, 
            text="Browse", 
            width=100, 
            command=self.upload_carrier_decode
        )
        self.decode_carrier_button.pack(side="right")

        # Password
        self.decode_password_label = ctk.CTkLabel(self.decode_tab, text="Password:", font=("Arial", 14))
        self.decode_password_label.pack(pady=(10, 5), anchor="w", padx=20)
        
        self.decode_password_entry = ctk.CTkEntry(self.decode_tab, show="*", width=450)
        self.decode_password_entry.pack(pady=5, padx=20)

        # Decode Button
        self.decode_button = ctk.CTkButton(
            self.decode_tab, 
            text="Decode", 
            font=("Arial", 16), 
            command=self.decode_action
        )
        self.decode_button.pack(pady=20)

    def upload_carrier_encode(self):
        carrier_path = filedialog.askopenfilename()
        if carrier_path:
            self.carrier_entry.delete(0, 'end')
            self.carrier_entry.insert(0, carrier_path)

    def upload_secret_encode(self):
        secret_path = filedialog.askopenfilename()
        if secret_path:
            self.secret_entry.delete(0, 'end')
            self.secret_entry.insert(0, secret_path)

    def upload_carrier_decode(self):
        carrier_path = filedialog.askopenfilename()
        if carrier_path:
            self.decode_carrier_entry.delete(0, 'end')
            self.decode_carrier_entry.insert(0, carrier_path)

    def encode_action(self):
        carrier_path = self.carrier_entry.get()
        secret_path = self.secret_entry.get()
        password = self.password_entry.get()

        if not (carrier_path and secret_path):
            messagebox.showerror("Error", "Both carrier and secret files must be selected!")
            return

        if not password:
            messagebox.showerror("Error", "Password is required!")
            return

        # Generate output filename
        carrier_filename = os.path.basename(carrier_path)
        output_path = os.path.join(self.encode_dir, f"encoded_{carrier_filename}")

        # Run steghide embed command
        command = [
            self.steghide_path, "embed",
            "-cf", carrier_path,
            "-ef", secret_path,
            "-p", password,
            "-sf", output_path
        ]
        
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode == 0:
                messagebox.showinfo("Success", f"Encoding successful! File saved at:\n{output_path}")
            else:
                messagebox.showerror("Error", f"Steghide failed:\n{result.stderr}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run Steghide: {e}")

    def decode_action(self):
        carrier_path = self.decode_carrier_entry.get()
        password = self.decode_password_entry.get()

        if not carrier_path:
            messagebox.showerror("Error", "Carrier file must be selected!")
            return

        if not password:
            messagebox.showerror("Error", "Password is required!")
            return

        # Ask for output directory for the extracted file
        output_file = os.path.join(
            self.decode_dir, 
            f"decoded_{os.path.basename(carrier_path)}"
        )

        # Run steghide extract command
        command = [
            self.steghide_path, "extract",
            "-sf", carrier_path,
            "-xf", output_file,
            "-p", password
        ]
        
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode == 0:
                messagebox.showinfo("Success", f"Decoding successful! File saved at:\n{output_file}")
            else:
                messagebox.showerror("Error", f"Steghide failed:\n{result.stderr}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run Steghide: {e}")

def main():
    app = SteganographyApp()
    app.mainloop()

if __name__ == "__main__":
    main()
