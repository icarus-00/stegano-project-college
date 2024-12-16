import customtkinter as ctk
import os
import subprocess
import hashlib
import time
from tkinter import messagebox

# Function to find the steghide executable
def find_snow():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    snow_path = os.path.join(current_dir, 'SNOW', 'SNOW.EXE')
    if not os.path.exists(snow_path):
        raise FileNotFoundError("SNOW.EXE not found in the 'SNOW' directory.")
    return snow_path

# Get the path to steghide executable
SNOW_PATH = find_snow()
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'textfiles')
ENCODE_DIR = os.path.join(OUTPUT_DIR, 'encode')
DECODE_DIR = os.path.join(OUTPUT_DIR, 'decode')

# Ensure output directories exist
os.makedirs(ENCODE_DIR, exist_ok=True)
os.makedirs(DECODE_DIR, exist_ok=True)

# Function to generate a unique filename based on hash and timestamp
def generate_unique_filename(base_name):
    timestamp = int(time.time())
    hash_object = hashlib.md5(base_name.encode())
    unique_hash = hash_object.hexdigest()
    return f"{unique_hash}_{timestamp}"

class ImageSteganography(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_tabs()

    def setup_tabs(self):
        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(expand=True, fill="both")

        # Image tabs
        self.encode_tab = self.tabs.add("Encode")
        self.decode_tab = self.tabs.add("Decode")

        # Setup image tabs
        self.setup_encode_tab()
        self.setup_decode_tab()

    def setup_encode_tab(self):
        layout = ctk.CTkFrame(self.encode_tab)
        layout.pack(pady=20)

        self.carrier_entry = ctk.CTkEntry(layout, placeholder_text="Carrier File Path")
        self.carrier_entry.pack(pady=10)

        carrier_button = ctk.CTkButton(layout, text="Upload Carrier", command=self.upload_carrier)
        carrier_button.pack(pady=10)

        self.secret_entry = ctk.CTkEntry(layout, placeholder_text="Secret File Path")
        self.secret_entry.pack(pady=10)

        secret_button = ctk.CTkButton(layout, text="Upload Secret", command=self.upload_secret)
        secret_button.pack(pady=10)

        self.password_entry = ctk.CTkEntry(layout, placeholder_text="Password", show='*')
        self.password_entry.pack(pady=10)

        hide_button = ctk.CTkButton(layout, text="Hide", command=self.hide_action)
        hide_button.pack(pady=10)

        reset_hide_button = ctk.CTkButton(layout, text="Reset", command=self.reset_hide_fields)
        reset_hide_button.pack(pady=10)

    def setup_decode_tab(self):
        layout = ctk.CTkFrame(self.decode_tab)
        layout.pack(pady=20)
        ctk.CTkLabel(layout, text="Images", font=("Arial", 16, "bold")).pack(pady=20)

        self.extract_carrier_entry = ctk.CTkEntry(layout, placeholder_text="Carrier File Path")
        self.extract_carrier_entry.pack(pady=10)

        extract_carrier_button = ctk.CTkButton(layout, text="Upload Carrier", command=self.upload_carrier_extract)
        extract_carrier_button.pack(pady=10)

        self.extract_password_entry = ctk.CTkEntry(layout, placeholder_text="Password", show='*')
        self.extract_password_entry.pack(pady=10)

        extract_button = ctk.CTkButton(layout, text="Extract", command=self.extract_action)
        extract_button.pack(pady=10)

        reset_extract_button = ctk.CTkButton(layout, text="Reset", command=self.reset_extract_fields)
        reset_extract_button.pack(pady=10)

    def upload_carrier(self):
        carrier_path = ctk.filedialog.askopenfilename()
        if carrier_path:
            self.carrier_entry.delete(0, ctk.END)
            self.carrier_entry.insert(0, carrier_path)

    def upload_secret(self):
        secret_path = ctk.filedialog.askopenfilename()
        if secret_path:
            self.secret_entry.delete(0, ctk.END)
            self.secret_entry.insert(0, secret_path)

    def upload_carrier_extract(self):
        carrier_path = ctk.filedialog.askopenfilename()
        if carrier_path:
            self.extract_carrier_entry.delete(0, ctk.END)
            self.extract_carrier_entry.insert(0, carrier_path)

    def hide_action(self):
        carrier_path = self.carrier_entry.get()
        secret_path = self.secret_entry.get()

        if not (carrier_path and secret_path):
            messagebox.showerror("Error", "Both files must be selected!")
            return

        password = self.password_entry.get()
        if not password:
            messagebox.showerror("Error", "Password is required!")
            return

        output_filename = generate_unique_filename(os.path.basename(carrier_path)) + ".txt"
        output_file_path = os.path.join(ENCODE_DIR, output_filename)

        command = [
            SNOW_PATH,
            "-C",
            "-p", password,
            "-f", secret_path,
            carrier_path,
            output_file_path  
        ]

        try:
            
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode == 0:
                messagebox.showinfo("Success", f"Hiding successful! File saved at:\n{output_file_path}")
            else:
                messagebox.showerror("Error", f"Snowfailed:\n{result.stderr}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run Snow: {e}")

    def extract_action(self):
            carrier_path = self.extract_carrier_entry.get()

            if not carrier_path:
                messagebox.showerror("Error", "Carrier file must be selected!")
                return

            password = self.extract_password_entry.get()
            if not password:
                messagebox.showerror("Error", "Password is required!")
                return

            output_filename = generate_unique_filename(os.path.basename(carrier_path)) + ".txt"
            output_file_path = os.path.join(DECODE_DIR, output_filename)

            result =subprocess.run([
                SNOW_PATH,
                "-C",
                "-p", password,
                carrier_path,
                
                output_file_path  
            ])

            try:
                
                if result.returncode == 0:
                    messagebox.showinfo("Success", f"Extraction successful! File saved at:\n{output_file_path}")
                else:
                    messagebox.showerror("Error", f"Snow failed:\n{result.stderr}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to run SNOW: {e}")

    def reset_hide_fields(self):
        self.carrier_entry.delete(0, ctk.END)
        self.secret_entry.delete(0, ctk.END)
        self.password_entry.delete(0, ctk.END)

    def reset_extract_fields(self):
        self.extract_carrier_entry.delete(0, ctk.END)
        self.extract_password_entry.delete(0, ctk.END)


# Main function to run the application
if __name__ == "__main__":
    root = ctk.CTk()  # Create the main CTk window
    root.title("Text Steganography Tool")
    root.geometry("800x600")  # Set the window size

    app = ImageSteganography(root)  # Create the ImageSteganography app inside the window
    app.pack(expand=True, fill="both")  # Pack the app into the root window

    root.mainloop()  # Run the main event loop
