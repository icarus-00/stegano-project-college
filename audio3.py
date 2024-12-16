import os
import subprocess
import hashlib
import time
import customtkinter as ctk
from tkinter import messagebox, filedialog
from threading import Thread
import pygame

# Function to find the steghide executable
def find_steghide():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    steghide_path = os.path.join(current_dir, 'steghide', 'steghide.exe')
    Encode_path = os.path.join(current_dir, 'audioTools' , 'MP3Stego', 'Encode.exe')
    decode_path = os.path.join(current_dir, 'audioTools' , 'MP3Stego', 'Decode.exe')
    if not os.path.exists(steghide_path):
        raise FileNotFoundError("steghide.exe not found in the 'steghide' directory.")
    return steghide_path

def find_encode():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    Encode_path = os.path.join(current_dir, 'audioTools' , 'MP3Stego', 'Encode.exe')
    if not os.path.exists(Encode_path):
        raise FileNotFoundError("Encode.exe not found in the 'steghide' directory.")
    return Encode_path

def find_decode():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    Decode_path = os.path.join(current_dir, 'audioTools' , 'MP3Stego', 'Decode.exe')
    if not os.path.exists(Decode_path):
        raise FileNotFoundError("Decode.exe not found in the 'steghide' directory.")
    return Decode_path

# Get the path to steghide executable
STEGHIDE_PATH = find_steghide()
ENCODE_PATH = find_encode()
DECODE_PATH = find_decode()

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'audio')
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

class AudioSteganography3(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_tabs()
        self.audio = None
        self.play_thread = None
        self.paused = False
        self.playing = False
        pygame.mixer.init()

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
        layout.pack(pady=20, padx=20, fill="both", expand=True)

        self.carrier_entry = ctk.CTkEntry(layout, placeholder_text="Carrier File Path", width=300)
        self.carrier_entry.grid(row=0, column=0, pady=10, padx=10, sticky="ew")

        carrier_button = ctk.CTkButton(layout, text="Upload Carrier", command=self.upload_carrier, width=150)
        carrier_button.grid(row=0, column=1, pady=10, padx=10, sticky="ew")

        self.audio_player_frame = ctk.CTkFrame(layout)
        self.audio_player_frame.grid(row=1, column=0, columnspan=2, pady=10, padx=10, sticky="ew")
        self.audio_player_frame.grid_remove()  # Hide the audio player initially

        self.secret_entry = ctk.CTkEntry(layout, placeholder_text="Secret File Path", width=300)
        self.secret_entry.grid(row=2, column=0, pady=10, padx=10, sticky="ew")

        secret_button = ctk.CTkButton(layout, text="Upload Secret", command=self.upload_secret, width=150)
        secret_button.grid(row=2, column=1, pady=10, padx=10, sticky="ew")

        self.password_entry = ctk.CTkEntry(layout, placeholder_text="Password", show='*', width=300)
        self.password_entry.grid(row=3, column=0, pady=10, padx=10, sticky="ew")

        hide_button = ctk.CTkButton(layout, text="Hide", command=self.hide_action, width=150)
        hide_button.grid(row=3, column=1, pady=10, padx=10, sticky="ew")

        reset_hide_button = ctk.CTkButton(layout, text="Reset", command=self.reset_hide_fields, width=150)
        reset_hide_button.grid(row=4, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

        layout.grid_columnconfigure(0, weight=1)
        layout.grid_columnconfigure(1, weight=1)

    def setup_decode_tab(self):
        layout = ctk.CTkFrame(self.decode_tab)
        layout.pack(pady=20, padx=20, fill="both", expand=True)

        ctk.CTkLabel(layout, text="Audio MP3Stegano", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=20)

        self.extract_carrier_entry = ctk.CTkEntry(layout, placeholder_text="Carrier File Path", width=300)
        self.extract_carrier_entry.grid(row=1, column=0, pady=10, padx=10, sticky="ew")

        extract_carrier_button = ctk.CTkButton(layout, text="Upload Carrier", command=self.upload_carrier_extract, width=150)
        extract_carrier_button.grid(row=1, column=1, pady=10, padx=10, sticky="ew")

        self.audio_player_frame_decode = ctk.CTkFrame(layout)
        self.audio_player_frame_decode.grid(row=2, column=0, columnspan=2, pady=10, padx=10, sticky="ew")
        self.audio_player_frame_decode.grid_remove()  # Hide the audio player initially

        self.extract_password_entry = ctk.CTkEntry(layout, placeholder_text="Password", show='*', width=300)
        self.extract_password_entry.grid(row=3, column=0, pady=10, padx=10, sticky="ew")

        extract_button = ctk.CTkButton(layout, text="Extract", command=self.extract_action, width=150)
        extract_button.grid(row=3, column=1, pady=10, padx=10, sticky="ew")

        reset_extract_button = ctk.CTkButton(layout, text="Reset", command=self.reset_extract_fields, width=150)
        reset_extract_button.grid(row=4, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

        layout.grid_columnconfigure(0, weight=1)
        layout.grid_columnconfigure(1, weight=1)

    def upload_carrier(self):
        carrier_path = filedialog.askopenfilename(filetypes=[("Audio files", ".wav")])
        if carrier_path:
            self.carrier_entry.delete(0, ctk.END)
            self.carrier_entry.insert(0, carrier_path)
            self.show_audio_player(carrier_path, self.audio_player_frame)

    def upload_secret(self):
        secret_path = filedialog.askopenfilename()
        if secret_path:
            self.secret_entry.delete(0, ctk.END)
            self.secret_entry.insert(0, secret_path)

    def upload_carrier_extract(self):
        carrier_path = filedialog.askopenfilename()
        if carrier_path:
            self.extract_carrier_entry.delete(0, ctk.END)
            self.extract_carrier_entry.insert(0, carrier_path)
            self.show_audio_player(carrier_path, self.audio_player_frame_decode)

    def show_audio_player(self, carrier_path, audio_player_frame):
        audio_player_frame.grid()  # Show the audio player frame

        self.play_button = ctk.CTkButton(audio_player_frame, text="Play", command=lambda: self.play_audio(carrier_path))
        self.play_button.grid(row=0, column=0, padx=5, pady=5)

        self.pause_button = ctk.CTkButton(audio_player_frame, text="Pause", command=self.pause_audio)
        self.pause_button.grid(row=0, column=1, padx=5, pady=5)

        self.stop_button = ctk.CTkButton(audio_player_frame, text="Stop", command=self.stop_audio)
        self.stop_button.grid(row=0, column=2, padx=5, pady=5)

        self.volume_scale = ctk.CTkSlider(audio_player_frame, from_=0, to=1, command=self.set_volume)
        self.volume_scale.set(1)  # Set default volume to maximum
        self.volume_scale.grid(row=0, column=3, padx=5, pady=5)

        self.progress_bar = ctk.CTkProgressBar(audio_player_frame, mode="determinate")
        self.progress_bar.grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky="ew")
        self.progress_bar.set(0)

        audio_player_frame.grid_columnconfigure(0, weight=1)
        audio_player_frame.grid_columnconfigure(1, weight=1)
        audio_player_frame.grid_columnconfigure(2, weight=1)
        audio_player_frame.grid_columnconfigure(3, weight=1)

    def play_audio(self, carrier_path):
        if not self.playing:
            pygame.mixer.music.load(carrier_path)
            pygame.mixer.music.play()
            self.playing = True
            self.total_length = pygame.mixer.Sound(carrier_path).get_length() * 1000  # Get total length in milliseconds
            self.update_progress_bar()
        elif self.paused:
            pygame.mixer.music.unpause()
            self.paused = False

    def pause_audio(self):
        if self.playing and not self.paused:
            pygame.mixer.music.pause()
            self.paused = True

    def stop_audio(self):
        pygame.mixer.music.stop()
        self.playing = False
        self.paused = False
        self.progress_bar.set(0)

    def set_volume(self, value):
        pygame.mixer.music.set_volume(value)

    def update_progress_bar(self):
        if self.playing and not self.paused:
            current_time = pygame.mixer.music.get_pos() / 1000  # Get current position in seconds
            total_time = self.total_length / 1000  # Get total length in seconds
            progress = (current_time / total_time) * 10
            self.progress_bar.set(progress)
            if self.playing and not self.paused:
                self.after(1000, self.update_progress_bar)  # Update every second

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

        output_filename = generate_unique_filename(os.path.basename(carrier_path)) + ".mp3"
        output_file_path = os.path.join(ENCODE_DIR, output_filename)

        command = [
            ENCODE_PATH,
            "-E", secret_path,
            "-P", password,
            carrier_path, output_file_path  # Use -sf to specify output file directly.
        ]

        try:
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode == 0:
                messagebox.showinfo("Success", f"Hiding successful! File saved at:\n{output_file_path}")
            else:
                messagebox.showerror("Error", f"Steghide failed:\n{result.stderr}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run Steghide: {e}")

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

        # Extract the directory from the DECODE_PATH
        decode_dir = os.path.dirname(DECODE_PATH)

        # Set the command to run Decode.exe
        command = [
            DECODE_PATH,
            "-P", password, "-X", carrier_path, output_file_path
        ]

        try:
            # Change working directory to where Decode.exe is located
            os.chdir(decode_dir)

            # Run the command to execute Decode.exe
            result = subprocess.run(command, capture_output=True, text=True)
            print(command)

            # Check if the extraction was successful
            if result.returncode == 0:
                messagebox.showinfo("Success", f"Extraction successful! File saved at:\n{output_file_path}")
            else:
                messagebox.showerror("Error", f"{result.stderr}")

        except Exception as e:
            messagebox.showerror("Error", f"{e}")

    def reset_hide_fields(self):
        self.carrier_entry.delete(0, ctk.END)
        self.secret_entry.delete(0, ctk.END)
        self.password_entry.delete(0, ctk.END)
        self.audio_player_frame.grid_remove()  # Hide the audio player frame
        self.stop_audio()

    def reset_extract_fields(self):
        self.extract_carrier_entry.delete(0, ctk.END)
        self.extract_password_entry.delete(0, ctk.END)
        self.audio_player_frame_decode.grid_remove()  # Hide the audio player frame
        self.stop_audio()

if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Audio Steganography")
    app.geometry("800x600")
    app.resizable(False, False)
    ctk.set_appearance_mode("dark")  # Set the theme to dark mode
    ctk.set_default_color_theme("blue")  # Set the color theme to blue
    audio_steganography = AudioSteganography3(app)
    audio_steganography.pack(expand=True, fill="both")
    app.mainloop()
