import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

# Path to steghide executable
STEGHIDE_PATH = os.path.join(os.path.dirname(__file__), 'steghide', 'steghide.exe')
ENCODE_DIR = os.path.join(os.path.dirname(__file__), 'encodefolder')
DECODE_DIR = os.path.join(os.path.dirname(__file__), 'decodefolder')

# Function to handle upload carrier button
def upload_carrier(carrier_entry):
    carrier_path = filedialog.askopenfilename()
    carrier_entry.delete(0, tk.END)
    carrier_entry.insert(0, carrier_path)

# Function to handle upload secret button
def upload_secret(secret_entry):
    secret_path = filedialog.askopenfilename()
    secret_entry.delete(0, tk.END)
    secret_entry.insert(0, secret_path)

# Function for hide button
def hide_action(carrier_path, secret_path, password):
    if not (carrier_path and secret_path):
        messagebox.showerror("Error", "Both files must be selected!")
        return

    if not password:
        messagebox.showerror("Error", "Password is required!")
        return

    # Ensure the output directory exists
    os.makedirs(ENCODE_DIR, exist_ok=True)

    # Run steghide embed command
    command = [
        STEGHIDE_PATH, "embed",
        "-cf", carrier_path,
        "-ef", secret_path,
        "-p", password
    ]
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            output_file = os.path.join(ENCODE_DIR, os.path.basename(carrier_path))
            messagebox.showinfo("Success", f"Hiding successful! File saved at:\n{output_file}")
        else:
            messagebox.showerror("Error", f"Steghide failed:\n{result.stderr}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run Steghide: {e}")

# Function for extract button
def extract_action(carrier_path, password):
    if not carrier_path:
        messagebox.showerror("Error", "Carrier file must be selected!")
        return

    if not password:
        messagebox.showerror("Error", "Password is required!")
        return

    # Ask for output directory for the extracted file
    output_file = filedialog.asksaveasfilename(
        title="Save Extracted File As",
        initialdir=DECODE_DIR
    )
    if not output_file:
        messagebox.showinfo("Info", "Extraction cancelled.")
        return

    # Run steghide extract command
    command = [
        STEGHIDE_PATH, "extract",
        "-sf", carrier_path,
        "-xf", output_file,
        "-p", password
    ]
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            messagebox.showinfo("Success", f"Extraction successful! File saved at:\n{output_file}")
        else:
            messagebox.showerror("Error", f"Steghide failed:\n{result.stderr}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run Steghide: {e}")

# Main page
root = tk.Tk()
root.title("Steganography Tool")

# Center the window
window_width = 400
window_height = 450
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)

root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

# Configure grid to make the window responsive
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

# Carrier file input for Hiding
carrier_label = tk.Label(root, text="Carrier File (For Hiding):", font=("Arial", 12))
carrier_label.grid(row=0, column=0, pady=5, sticky="w", padx=10)

carrier_entry = tk.Entry(root, width=40)
carrier_entry.grid(row=1, column=0, pady=5, padx=10)

carrier_button = tk.Button(root, text="Upload Carrier", command=lambda: upload_carrier(carrier_entry))
carrier_button.grid(row=2, column=0, pady=5, padx=10, sticky="ew")

# Secret file input for Hiding
secret_label = tk.Label(root, text="Secret File:", font=("Arial", 12))
secret_label.grid(row=3, column=0, pady=5, sticky="w", padx=10)

secret_entry = tk.Entry(root, width=40)
secret_entry.grid(row=4, column=0, pady=5, padx=10)

secret_button = tk.Button(root, text="Upload Secret", command=lambda: upload_secret(secret_entry))
secret_button.grid(row=5, column=0, pady=5, padx=10, sticky="ew")

# Password input for Hiding
password_label = tk.Label(root, text="Password (For Hiding):", font=("Arial", 12))
password_label.grid(row=6, column=0, pady=5, sticky="w", padx=10)

password_entry = tk.Entry(root, show="*", width=40)
password_entry.grid(row=7, column=0, pady=5, padx=10)

# Hide button
hide_button = tk.Button(
    root, text="Hide", font=("Arial", 12),
    command=lambda: hide_action(carrier_entry.get(), secret_entry.get(), password_entry.get())
)
hide_button.grid(row=8, column=0, pady=10, padx=10, sticky="ew")

# Separator
separator = tk.Label(root, text="-----------------------------", font=("Arial", 12))
separator.grid(row=9, column=0, pady=10)

# Carrier file input for Extraction
extract_label = tk.Label(root, text="Carrier File (For Extraction):", font=("Arial", 12))
extract_label.grid(row=10, column=0, pady=5, sticky="w", padx=10)

extract_carrier_entry = tk.Entry(root, width=40)
extract_carrier_entry.grid(row=11, column=0, pady=5, padx=10)

extract_carrier_button = tk.Button(root, text="Upload Carrier", command=lambda: upload_carrier(extract_carrier_entry))
extract_carrier_button.grid(row=12, column=0, pady=5, padx=10, sticky="ew")

# Password input for Extraction
extract_password_label = tk.Label(root, text="Password (For Extraction):", font=("Arial", 12))
extract_password_label.grid(row=13, column=0, pady=5, sticky="w", padx=10)

extract_password_entry = tk.Entry(root, show="*", width=40)
extract_password_entry.grid(row=14, column=0, pady=5, padx=10)

# Extract button
extract_button = tk.Button(
    root, text="Extract", font=("Arial", 12),
    command=lambda: extract_action(extract_carrier_entry.get(), extract_password_entry.get())
)
extract_button.grid(row=15, column=0, pady=10, padx=10, sticky="ew")

root.mainloop()
