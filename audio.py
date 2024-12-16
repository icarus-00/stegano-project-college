import os
import wave
import struct
import hashlib
import time
import numpy as np
import customtkinter as ctk
from tkinter import messagebox

# Output directories
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'audio')
ENCODE_DIR = os.path.join(OUTPUT_DIR, 'encode')
DECODE_DIR = os.path.join(OUTPUT_DIR, 'decode')

# Ensure directories exist
os.makedirs(ENCODE_DIR, exist_ok=True)
os.makedirs(DECODE_DIR, exist_ok=True)

def generate_hashed_filename():
    timestamp = str(time.time()).encode()
    return hashlib.sha256(timestamp).hexdigest()[:10]

def encode_message(audio_file, message_file, passphrase, output_dir):
    # Read message from file
    with open(message_file, 'r') as file:
        message = file.read()

    message += f"\n{passphrase}"  # Append passphrase to message

    with wave.open(audio_file, 'rb') as wav:
        params = wav.getparams()
        frames = wav.readframes(params.nframes)
        
        frame_array = np.frombuffer(frames, dtype=np.int16)
        message_bits = ''.join(format(ord(c), '08b') for c in message)

        if len(message_bits) > len(frame_array):
            raise ValueError("Message is too large for the audio file.")

        # Embed message
        for i, bit in enumerate(message_bits):
            frame_array[i] = (frame_array[i] & ~1) | int(bit)

        # Save encoded audio
        output_file = os.path.join(output_dir, f"{generate_hashed_filename()}.wav")
        with wave.open(output_file, 'wb') as out_wav:
            out_wav.setparams(params)
            out_wav.writeframes(frame_array.tobytes())

        return output_file

def decode_message(audio_file, passphrase):
    with wave.open(audio_file, 'rb') as wav:
        frames = wav.readframes(wav.getnframes())
        
        frame_array = np.frombuffer(frames, dtype=np.int16)
        bits = [str(frame_array[i] & 1) for i in range(len(frame_array))]
        
        message = ''.join([chr(int(''.join(bits[i:i+8]), 2)) for i in range(0, len(bits), 8)])
        
        decoded_message, _, decoded_passphrase = message.partition('\n')

        if decoded_passphrase != passphrase:
            raise ValueError("Incorrect passphrase.")

        return decoded_message

class AudioSteganography(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        ctk.CTkLabel(self, text="Audio Steganography", font=("Arial", 20, "bold")).pack(pady=20)

        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(expand=True, fill="both")

        self.encode_tab = self.tabs.add("Encode")
        self.decode_tab = self.tabs.add("Decode")

        self.setup_encode_tab()
        self.setup_decode_tab()

    def setup_encode_tab(self):
        layout = ctk.CTkFrame(self.encode_tab)
        layout.pack(pady=20)

        self.audio_entry = ctk.CTkEntry(layout, placeholder_text="Audio File Path")
        self.audio_entry.pack(pady=10)

        audio_button = ctk.CTkButton(layout, text="Upload Audio", command=self.upload_audio)
        audio_button.pack(pady=10)

        self.message_entry = ctk.CTkEntry(layout, placeholder_text="Message File Path")
        self.message_entry.pack(pady=10)

        message_button = ctk.CTkButton(layout, text="Upload Message", command=self.upload_message)
        message_button.pack(pady=10)

        self.passphrase_entry = ctk.CTkEntry(layout, placeholder_text="Passphrase")
        self.passphrase_entry.pack(pady=10)

        encode_button = ctk.CTkButton(layout, text="Encode", command=self.encode_action)
        encode_button.pack(pady=10)

    def setup_decode_tab(self):
        layout = ctk.CTkFrame(self.decode_tab)
        layout.pack(pady=20)

        self.decode_audio_entry = ctk.CTkEntry(layout, placeholder_text="Audio File Path")
        self.decode_audio_entry.pack(pady=10)

        decode_audio_button = ctk.CTkButton(layout, text="Upload Audio", command=self.upload_decode_audio)
        decode_audio_button.pack(pady=10)

        self.decode_passphrase_entry = ctk.CTkEntry(layout, placeholder_text="Passphrase")
        self.decode_passphrase_entry.pack(pady=10)

        decode_button = ctk.CTkButton(layout, text="Decode", command=self.decode_action)
        decode_button.pack(pady=10)

    def upload_audio(self):
        audio_path = ctk.filedialog.askopenfilename(filetypes=[("WAV Files", "*.wav")])
        if audio_path:
            self.audio_entry.delete(0, ctk.END)
            self.audio_entry.insert(0, audio_path)

    def upload_message(self):
        message_path = ctk.filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if message_path:
            self.message_entry.delete(0, ctk.END)
            self.message_entry.insert(0, message_path)

    def upload_decode_audio(self):
        audio_path = ctk.filedialog.askopenfilename(filetypes=[("WAV Files", "*.wav")])
        if audio_path:
            self.decode_audio_entry.delete(0, ctk.END)
            self.decode_audio_entry.insert(0, audio_path)

    def encode_action(self):
        audio_file = self.audio_entry.get()
        message_file = self.message_entry.get()
        passphrase = self.passphrase_entry.get()

        if not audio_file or not message_file or not passphrase:
            messagebox.showerror("Error", "Please provide an audio file, a message file, and a passphrase.")
            return

        try:
            output_file = encode_message(audio_file, message_file, passphrase, ENCODE_DIR)
            messagebox.showinfo("Success", f"Message encoded successfully! Output: {output_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to encode message: {e}")

    def decode_action(self):
        audio_file = self.decode_audio_entry.get()
        passphrase = self.decode_passphrase_entry.get()

        if not audio_file or not passphrase:
            messagebox.showerror("Error", "Please provide an audio file and a passphrase.")
            return

        try:
            message = decode_message(audio_file, passphrase)
            output_file = os.path.join(DECODE_DIR, f"{generate_hashed_filename()}.txt")
            with open(output_file, 'w') as file:
                file.write(message)

            messagebox.showinfo("Decoded Message", f"Message saved to: {output_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to decode message: {e}")
