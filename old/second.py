import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from shadcn.ui.alert import Alert, AlertDescription, AlertTitle, AlertDialog, AlertDialogAction
from shadcn.ui.button import Button
from shadcn.ui.card import Card, CardContent, CardHeader, CardTitle
from shadcn.ui.input import Input

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
        Alert(
            title=AlertTitle("Error"),
            description=AlertDescription("Both files must be selected!"),
            variant="destructive"
        ).show()
        return

    if not password:
        Alert(
            title=AlertTitle("Error"),
            description=AlertDescription("Password is required!"),
            variant="destructive"
        ).show()
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
            Alert(
                title=AlertTitle("Success"),
                description=AlertDescription(f"Hiding successful! File saved at:\n{output_file}"),
                variant="default"
            ).show()
        else:
            Alert(
                title=AlertTitle("Error"),
                description=AlertDescription(f"Steghide failed:\n{result.stderr}"),
                variant="destructive"
            ).show()
    except Exception as e:
        Alert(
            title=AlertTitle("Error"),
            description=AlertDescription(f"Failed to run Steghide: {e}"),
            variant="destructive"
        ).show()

# Function for extract button
def extract_action(carrier_path, password):
    if not carrier_path:
        Alert(
            title=AlertTitle("Error"),
            description=AlertDescription("Carrier file must be selected!"),
            variant="destructive"
        ).show()
        return

    if not password:
        Alert(
            title=AlertTitle("Error"),
            description=AlertDescription("Password is required!"),
            variant="destructive"
        ).show()
        return

    # Ask for output directory for the extracted file
    output_file = filedialog.asksaveasfilename(
        title="Save Extracted File As",
        initialdir=DECODE_DIR
    )
    if not output_file:
        Alert(
            title=AlertTitle("Info"),
            description=AlertDescription("Extraction cancelled."),
            variant="default"
        ).show()
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
            Alert(
                title=AlertTitle("Success"),
                description=AlertDescription(f"Extraction successful! File saved at:\n{output_file}"),
                variant="default"
            ).show()
        else:
            Alert(
                title=AlertTitle("Error"),
                description=AlertDescription(f"Steghide failed:\n{result.stderr}"),
                variant="destructive"
            ).show()
    except Exception as e:
        Alert(
            title=AlertTitle("Error"),
            description=AlertDescription(f"Failed to run Steghide: {e}"),
            variant="destructive"
        ).show()

# Main page
root = tk.Tk()
root.title("Steganography Tool")

# Center the window
window_width = 600
window_height = 550
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
carrier_label.grid(row=0, column=0, pady=10, sticky="w", padx=20)

carrier_entry = Input(root, width=40)
carrier_entry.grid(row=1, column=0, pady=10, padx=20)

carrier_button = Button(root, text="Upload Carrier", on_click=lambda: upload_carrier(carrier_entry))
carrier_button.grid(row=2, column=0, pady=10, padx=20, sticky="ew")

# Secret file input for Hiding
secret_label = tk.Label(root, text="Secret File:", font=("Arial", 12))
secret_label.grid(row=3, column=0, pady=10, sticky="w", padx=20)

secret_entry = Input(root, width=40)
secret_entry.grid(row=4, column=0, pady=10, padx=20)

secret_button = Button(root, text="Upload Secret", on_click=lambda: upload_secret(secret_entry))
secret_button.grid(row=5, column=0, pady=10, padx=20, sticky="ew")

# Password input for Hiding
password_label = tk.Label(root, text="Password (For Hiding):", font=("Arial", 12))
password_label.grid(row=6, column=0, pady=10, sticky="w", padx=20)

password_entry = Input(root, show="*", width=40)
password_entry.grid(row=7, column=0, pady=10, padx=20)

# Hide button
hide_button = Button(
    root, text="Hide", font=("Arial", 12),
    on_click=lambda: hide_action(carrier_entry.get(), secret_entry.get(), password_entry.get())
)
hide_button.grid(row=8, column=0, pady=20, padx=20, sticky="ew")

# Separator
separator = tk.Label(root, text="-----------------------------", font=("Arial", 12))
separator.grid(row=9, column=0, pady=20)

# Carrier file input for Extraction
extract_label = tk.Label(root, text="Carrier File (For Extraction):", font=("Arial", 12))
extract_label.grid(row=10, column=0, pady=10, sticky="w", padx=20)

extract_carrier_entry = Input(root, width=40)
extract_carrier_entry.grid(row=11, column=0, pady=10, padx=20)

extract_carrier_button = Button(root, text="Upload Carrier", on_click=lambda: upload_carrier(extract_carrier_entry))
extract_carrier_button.grid(row=12, column=0, pady=10, padx=20, sticky="ew")

# Password input for Extraction
extract_password_label = tk.Label(root, text="Password (For Extraction):", font=("Arial", 12))
extract_password_label.grid(row=13, column=0, pady=10, sticky="w", padx=20)

extract_password_entry = Input(root, show="*", width=40)
extract_password_entry.grid(row=14, column=0, pady=10, padx=20)

# Extract button
extract_button = Button(
    root, text="Extract", font=("Arial", 12),
    on_click=lambda: extract_action(extract_carrier_entry.get(), extract_password_entry.get())
)
extract_button.grid(row=15, column=0, pady=20, padx=20, sticky="ew")

root.mainloop()
