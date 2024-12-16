import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

# Path to steghide executable
STEGHIDE_PATH = r"F:\\BFCAI\\lv4s1\\stegano\\project\\steghide\\steghide.exe"
OUTPUT_DIR = r"F:\\BFCAI\\lv4s1\\stegano\\project\\code"

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
if not os.path.exists(OUTPUT_DIR):
os.makedirs(OUTPUT_DIR)

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
messagebox.showinfo("Success", f"Hiding successful! File saved at:\n{carrier_path}")
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
output_file = filedialog.asksaveasfilename(title="Save Extracted File As")
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

# Reset function for hiding and extracting section
def reset_hide_fields(carrier_entry, secret_entry, password_entry):
carrier_entry.delete(0, tk.END)
secret_entry.delete(0, tk.END)
password_entry.delete(0, tk.END)

def reset_extract_fields(extract_carrier_entry, extract_password_entry):
extract_carrier_entry.delete(0, tk.END)
extract_password_entry.delete(0, tk.END)

# Main page
root = tk.Tk()
root.title("Steganography Tool")

# Center the window
window_width = 500
window_height = 650
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)

root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

# Carrier file input for Hiding
carrier_label = tk.Label(root, text="Carrier File (For Hiding):", font=("Arial", 12))
carrier_label.pack(pady=5, anchor="w", padx=10)
carrier_entry = tk.Entry(root, width=40)
carrier_entry.pack(pady=5, padx=10)
carrier_button = tk.Button(root, text="Upload Carrier", command=lambda: upload_carrier(carrier_entry))
carrier_button.pack(pady=5)

# Secret file input for Hiding
secret_label = tk.Label(root, text="Secret File:", font=("Arial", 12))
secret_label.pack(pady=5, anchor="w", padx=10)
secret_entry = tk.Entry(root, width=40)
secret_entry.pack(pady=5, padx=10)
secret_button = tk.Button(root, text="Upload Secret", command=lambda: upload_secret(secret_entry))
secret_button.pack(pady=5)

# Password input for Hiding
password_label = tk.Label(root, text="Password (For Hiding):", font=("Arial", 12))
password_label.pack(pady=5, anchor="w", padx=10)
password_entry = tk.Entry(root, show="*", width=40)
password_entry.pack(pady=5, padx=10)

# Hide button
hide_button = tk.Button(
root, text="Hide", font=("Arial", 12),
command=lambda: hide_action(carrier_entry.get(), secret_entry.get(), password_entry.get()),
width=5, # Adjust the width as needed
height=1 # Adjust the height as needed
)
hide_button.pack(pady=10)

# Reset button for Hide
reset_hide_button = tk.Button(
root, text="Reset", font=("Arial", 12),
command=lambda: reset_hide_fields(carrier_entry, secret_entry, password_entry),
width=5, # Adjust the width as needed
height=1 # Adjust the height as needed
)
reset_hide_button.pack(pady=5)

# Separator
separator = tk.Label(root, text="-----------------------------", font=("Arial", 12))
separator.pack(pady=10)

# Carrier file input for Extraction
extract_label = tk.Label(root, text="Carrier File (For Extraction):", font=("Arial", 12))
extract_label.pack(pady=5, anchor="w", padx=10)
extract_carrier_entry = tk.Entry(root, width=40)
extract_carrier_entry.pack(pady=5, padx=10)
extract_carrier_button = tk.Button(root, text="Upload Carrier", command=lambda: upload_carrier(extract_carrier_entry))
extract_carrier_button.pack(pady=5)

# Password input for Extraction
extract_password_label = tk.Label(root, text="Password (For Extraction):", font=("Arial", 12))
extract_password_label.pack(pady=5, anchor="w", padx=10)
extract_password_entry = tk.Entry(root, show="*", width=40)
extract_password_entry.pack(pady=5, padx=10)

# Extract button
extract_button = tk.Button(
root, text="Extract", font=("Arial", 12),
command=lambda: extract_action(extract_carrier_entry.get(), extract_password_entry.get())
)
extract_button.pack(pady=10)

# Reset button for Extract
reset_extract_button = tk.Button(
root, text="Reset", font=("Arial", 12),
command=lambda: reset_extract_fields(extract_carrier_entry, extract_password_entry)
)
reset_extract_button.pack(pady=5)

root.mainloop()
