import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import os
import threading

class SteghideApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Steghide Steganography Tool")
        self.root.geometry("600x700")
        self.root.configure(bg='#f0f4f8')

        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()

        # Create main notebook (tabbed interface)
        self.notebook = ttk.Notebook(root, style='Custom.TNotebook')
        self.notebook.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Create tabs
        self.create_embed_tab()
        self.create_extract_tab()

    def configure_styles(self):
        # Custom styles for a modern look
        self.style.configure('Custom.TNotebook', background='#f0f4f8')
        self.style.configure('Custom.TNotebook.Tab', 
                             background='#e2e8f0', 
                             foreground='#2d3748', 
                             padding=[10, 5])
        self.style.map('Custom.TNotebook.Tab', 
                       background=[('selected', '#4a5568')],
                       foreground=[('selected', 'white')])
        
        self.style.configure('TLabel', 
                              background='#f0f4f8', 
                              foreground='#2d3748', 
                              font=('Segoe UI', 10))
        
        self.style.configure('TButton', 
                              background='#4299e1', 
                              foreground='white', 
                              font=('Segoe UI', 10, 'bold'))
        
        self.style.configure('TEntry', 
                              background='white', 
                              foreground='#2d3748')

    def create_embed_tab(self):
        # Embed Tab
        embed_frame = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(embed_frame, text="Embed Message")

        # Carrier File
        ttk.Label(embed_frame, text="Carrier File", style='TLabel').pack(pady=(20,5), anchor='w', padx=20)
        self.carrier_entry = ttk.Entry(embed_frame, width=70, style='TEntry')
        self.carrier_entry.pack(pady=5, padx=20, fill='x')
        ttk.Button(embed_frame, text="Browse", command=self.browse_carrier_file, style='TButton').pack(pady=5)

        # Output File
        ttk.Label(embed_frame, text="Output Steganographic File", style='TLabel').pack(pady=(10,5), anchor='w', padx=20)
        self.output_entry = ttk.Entry(embed_frame, width=70, style='TEntry')
        self.output_entry.pack(pady=5, padx=20, fill='x')
        ttk.Button(embed_frame, text="Browse", command=self.browse_output_file, style='TButton').pack(pady=5)

        # Message
        ttk.Label(embed_frame, text="Message to Embed", style='TLabel').pack(pady=(10,5), anchor='w', padx=20)
        self.message_text = tk.Text(embed_frame, height=4, width=70)
        self.message_text.pack(pady=5, padx=20)

        # Password
        ttk.Label(embed_frame, text="Password (Optional)", style='TLabel').pack(pady=(10,5), anchor='w', padx=20)
        self.embed_password_entry = ttk.Entry(embed_frame, show='*', width=70, style='TEntry')
        self.embed_password_entry.pack(pady=5, padx=20, fill='x')

        # Embed Button
        ttk.Button(embed_frame, text="Embed Message", command=self.embed_message, style='TButton').pack(pady=20)

    def create_extract_tab(self):
        # Extract Tab
        extract_frame = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(extract_frame, text="Extract Message")

        # Steganographic File
        ttk.Label(extract_frame, text="Steganographic File", style='TLabel').pack(pady=(20,5), anchor='w', padx=20)
        self.stego_entry = ttk.Entry(extract_frame, width=70, style='TEntry')
        self.stego_entry.pack(pady=5, padx=20, fill='x')
        ttk.Button(extract_frame, text="Browse", command=self.browse_stego_file, style='TButton').pack(pady=5)

        # Output File
        ttk.Label(extract_frame, text="Output Message File", style='TLabel').pack(pady=(10,5), anchor='w', padx=20)
        self.extract_output_entry = ttk.Entry(extract_frame, width=70, style='TEntry')
        self.extract_output_entry.pack(pady=5, padx=20, fill='x')
        ttk.Button(extract_frame, text="Browse", command=self.browse_extract_output_file, style='TButton').pack(pady=5)

        # Password
        ttk.Label(extract_frame, text="Password (Optional)", style='TLabel').pack(pady=(10,5), anchor='w', padx=20)
        self.extract_password_entry = ttk.Entry(extract_frame, show='*', width=70, style='TEntry')
        self.extract_password_entry.pack(pady=5, padx=20, fill='x')

        # Extract Button
        ttk.Button(extract_frame, text="Extract Message", command=self.extract_message, style='TButton').pack(pady=20)

    def browse_carrier_file(self):
        filename = filedialog.askopenfilename(title="Select Carrier File")
        self.carrier_entry.delete(0, tk.END)
        self.carrier_entry.insert(0, filename)

    def browse_output_file(self):
        filename = filedialog.asksaveasfilename(title="Save Steganographic File")
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, filename)

    def browse_stego_file(self):
        filename = filedialog.askopenfilename(title="Select Steganographic File")
        self.stego_entry.delete(0, tk.END)
        self.stego_entry.insert(0, filename)

    def browse_extract_output_file(self):
        filename = filedialog.asksaveasfilename(title="Save Extracted Message")
        self.extract_output_entry.delete(0, tk.END)
        self.extract_output_entry.insert(0, filename)

    def embed_message(self):
        # Validate inputs
        carrier_file = self.carrier_entry.get()
        output_file = self.output_entry.get()
        message = self.message_text.get("1.0", tk.END).strip()
        password = self.embed_password_entry.get()

        if not carrier_file or not output_file or not message:
            messagebox.showerror("Error", "Please fill in all required fields")
            return

        # Create temporary message file
        try:
            with open('temp_message.txt', 'w') as f:
                f.write(message)

            # Construct command
            cmd = ['steghide', 'embed', '-cf', carrier_file, '-ef', 'temp_message.txt', '-sf', output_file]
            if password:
                cmd.extend(['-p', password])

            # Run in a separate thread to prevent GUI freezing
            threading.Thread(target=self.run_steghide_command, args=(cmd,), daemon=True).start()

        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            # Clean up temporary file
            if os.path.exists('temp_message.txt'):
                os.remove('temp_message.txt')

    def extract_message(self):
        # Validate inputs
        stego_file = self.stego_entry.get()
        output_file = self.extract_output_entry.get()
        password = self.extract_password_entry.get()

        if not stego_file or not output_file:
            messagebox.showerror("Error", "Please fill in all required fields")
            return

        # Construct command
        cmd = ['steghide', 'extract', '-sf', stego_file, '-xf', output_file]
        if password:
            cmd.extend(['-p', password])

        # Run in a separate thread to prevent GUI freezing
        threading.Thread(target=self.run_steghide_command, args=(cmd,), daemon=True).start()

    def run_steghide_command(self, cmd):
        try:
            # Run the steghide command
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # Show success message
            tk.messagebox.showinfo("Success", "Operation completed successfully!")
        except subprocess.CalledProcessError as e:
            # Show error message
            tk.messagebox.showerror("Error", f"Operation failed:\n{e.stderr}")

def main():
    root = tk.Tk()
    app = SteghideApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
