import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import zipfile
import os
import threading

class WinRARCloneApp:
    def __init__(self, master):
        self.master = master
        self.master.title("WinRAR Clone")
        self.master.geometry("500x250")
        self.master.resizable(False, False)

        # File and folder paths
        self.zip_path = tk.StringVar()
        self.extract_path = tk.StringVar()

        # --- UI Layout ---
        tk.Label(master, text="Select ZIP File:").pack(anchor='w', padx=10, pady=(15, 0))
        file_frame = tk.Frame(master)
        file_frame.pack(fill='x', padx=10)
        tk.Entry(file_frame, textvariable=self.zip_path, width=50).pack(side='left', fill='x', expand=True)
        tk.Button(file_frame, text="Browse", command=self.browse_zip).pack(side='right')

        tk.Label(master, text="Select Destination Folder:").pack(anchor='w', padx=10, pady=(15, 0))
        folder_frame = tk.Frame(master)
        folder_frame.pack(fill='x', padx=10)
        tk.Entry(folder_frame, textvariable=self.extract_path, width=50).pack(side='left', fill='x', expand=True)
        tk.Button(folder_frame, text="Browse", command=self.browse_folder).pack(side='right')

        tk.Button(master, text="Extract", command=self.start_extraction, height=2, bg="#4CAF50", fg="white").pack(pady=15)

        self.progress_bar = ttk.Progressbar(master, length=400, mode='determinate')
        self.progress_bar.pack(pady=5)

        self.status_label = tk.Label(master, text="", fg="blue")
        self.status_label.pack()

    def browse_zip(self):
        path = filedialog.askopenfilename(filetypes=[("ZIP files", "*.zip")])
        if path:
            self.zip_path.set(path)

    def browse_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.extract_path.set(path)

    def start_extraction(self):
        zip_file = self.zip_path.get()
        extract_to = self.extract_path.get()

        if not zip_file or not extract_to:
            messagebox.showwarning("Missing Info", "Please select both a ZIP file and destination folder.")
            return

        self.status_label.config(text="Starting extraction...")
        self.progress_bar['value'] = 0
        threading.Thread(target=self.extract_zip, args=(zip_file, extract_to), daemon=True).start()

    def extract_zip(self, zip_path, extract_path):
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                file_list = zip_ref.namelist()
                total_files = len(file_list)

                for i, file in enumerate(file_list, 1):
                    zip_ref.extract(file, extract_path)
                    percent = int((i / total_files) * 100)
                    self.progress_bar['value'] = percent
                    self.status_label.config(text=f"Extracting... {percent}%")
                    self.master.update_idletasks()

            self.status_label.config(text="Extraction complete.")
            messagebox.showinfo("Success", f"Files extracted to:\n{extract_path}")

        except zipfile.BadZipFile:
            messagebox.showerror("Error", "Invalid ZIP file.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")

def main():
    root = tk.Tk()
    app = WinRARCloneApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
