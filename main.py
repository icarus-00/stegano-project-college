# main.py

from images import ImageSteganography
from audio2 import AudioSteganography
from audio3 import AudioSteganography3
from video import VideoSteganographyFFmpeg
from Snow import TextSteganography
import customtkinter as ctk

class SteganographyTool(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("")
        self.geometry("800x600")
        
        self.resizable(False, False)
        self.configure(fg_color="#212121")

        # Custom Title Bar
        # Custom Title Bar
        # self.title_bar = ctk.CTkFrame(self, corner_radius=0, height=35, fg_color="#000000")
        # self.title_bar.pack(side="top", fill="x")

        # self.app_name_label = ctk.CTkLabel(self.title_bar, text="Steganography Tool", font=ctk.CTkFont("Arial", 16, "bold"), text_color="white")
        # self.app_name_label.place(x=10, y=5)

        # self.close_button = ctk.CTkButton(self.title_bar, text="x ", command=self.destroy, width=30, height=30, corner_radius=0, fg_color="#000000", hover_color="#3e8e41")
        # self.close_button.place(relx=1, rely=0.5, anchor="center", x=-5, y=0)

        # self.hide_button = ctk.CTkButton(self.title_bar, text="-", command=self.iconify, width=30, height=30, corner_radius=0, fg_color="#000000", hover_color="#3e8e41")
        # self.hide_button.place(relx=1, rely=0.5, anchor="center", x=-35, y=0)
        # Drawer
        self.drawer = ctk.CTkFrame(self, width=200, height=600, corner_radius=0, fg_color="#1a1a1a")
        self.drawer.pack(side="left", fill="y")

        self.drawer_button = ctk.CTkButton(self.drawer, text="", command=self.toggle_drawer, width=30, height=30, corner_radius=0, fg_color="#1a1a1a", hover_color="#323232")
        self.drawer_button.pack(pady=10)

        self.drawer_items = ["Images", "Audio", "Audio3", "Video", "Snow"]
        for i, item in enumerate(self.drawer_items):
            button = ctk.CTkButton(self.drawer, text=item, font=ctk.CTkFont("Arial", 14), width=180, height=40, corner_radius=0,  command=lambda x=item: self.load_tab(x))
            button.pack(pady=2)

        # Main Panel
        self.main_panel = ctk.CTkFrame(self, corner_radius=0, fg_color="#212121")
        self.main_panel.pack(side="right", expand=True, fill="both")

        self.tabs = {
            "Images": ImageSteganography(self.main_panel),
            "Audio": AudioSteganography(self.main_panel),
            "Audio3": AudioSteganography3(self.main_panel),
            "Video": VideoSteganographyFFmpeg(self.main_panel),
            "Snow": TextSteganography(self.main_panel)
        }

        self.current_tab = None
        self.load_tab("Images")

    def load_tab(self, tab_name):
        if self.current_tab:
            self.current_tab.pack_forget()
        self.current_tab = self.tabs[tab_name]
        self.current_tab.pack(expand=True, fill="both")

    def toggle_drawer(self):
        if self.drawer.winfo_ismapped():
            self.drawer.pack_forget()
        else:
            self.drawer.pack(side="left", fill="y")

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("green")
    app = SteganographyTool()
    app.mainloop()

