# main.py
import customtkinter as ctk
from images import ImageSteganography
from audio2 import AudioSteganography
from audio3 import AudioSteganography3

class SteganographyTool(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Steganography Tool")
        self.geometry("800x600")
        self.resizable(False, False)

        # Add drawer for navigation
        self.drawer = ctk.CTkFrame(self, width=200)
        self.drawer.pack(side="left", fill="y")

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(side="right", expand=True, fill="both")

        self.add_drawer_items()
        self.setup_pane()

    def add_drawer_items(self):
        ctk.CTkLabel(self.drawer, text="Menu", font=("Arial", 16, "bold")).pack(pady=20)
        ctk.CTkButton(self.drawer, text="Images", command=self.load_image_tab).pack(pady=10)
        ctk.CTkButton(self.drawer, text="Audio", command=self.load_audio_tab).pack(pady=10)
        ctk.CTkButton(self.drawer, text="Audio3", command=self.load_audio_tab3).pack(pady=10)

    def setup_pane(self):
        self.image_tab = ImageSteganography(self.main_frame)
        self.audio_tab = AudioSteganography(self.main_frame)
        self.audio_tab3 = AudioSteganography3(self.main_frame)
        self.load_image_tab()  # Default to image tab

    def load_image_tab(self):
        self.hide_all_tabs()
        self.image_tab.pack(expand=True, fill="both")

    def load_audio_tab(self):
        self.hide_all_tabs()
        self.audio_tab.pack(expand=True, fill="both")
        
    def load_audio_tab3(self):
        self.hide_all_tabs()
        self.audio_tab3.pack(expand=True, fill="both")

    def hide_all_tabs(self):
        for tab in [self.image_tab, self.audio_tab]:
            tab.pack_forget()

if __name__ == "__main__":
    app = SteganographyTool()
    app.mainloop()
