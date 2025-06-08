import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import zipfile
import os
import threading

class ModernWinRARClone:
    def __init__(self, master):
        self.master = master
        self.master.title("unzipper")
        self.master.geometry("520x330")
        self.master.resizable(False, False)

        self.style = ttk.Style()
        self.master.tk.call("source", "azure.tcl")  # Optional: use a theme file
        self.style.theme_use("clam")  # Looks more modern than default "vista"

        # Customize style
        self.style.configure("TNotebook.Tab", padding=[12, 6], font=("Segoe UI", 10))
        self.style.configure("TButton", font=("Segoe UI", 10), padding=6)
        self.style.configure("TProgressbar", thickness=20)

        self.tab_control = ttk.Notebook(master)

        self.extract_tab = ttk.Frame(self.tab_control)
        self.zip_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.extract_tab, text='📂 Extract ZIP')
        self.tab_control.add(self.zip_tab, text='🗜 Create ZIP')
        self.tab_control.pack(expand=1, fill="both", padx=10, pady=10)

        self.setup_extract_tab()
        self.setup_zip_tab()

    # ==== Extract Tab ====
    def setup_extract_tab(self):
        self.zip_path = tk.StringVar()
        self.extract_path = tk.StringVar()

        self.build_entry_row(self.extract_tab, "ZIP File:", self.zip_path, self.browse_zip)
        self.build_entry_row(self.extract_tab, "Extract To:", self.extract_path, self.browse_extract_folder)

        ttk.Button(self.extract_tab, text="Extract", command=self.start_extraction).pack(pady=10)

        self.progress_bar_extract = ttk.Progressbar(self.extract_tab, length=400, mode='determinate')
        self.progress_bar_extract.pack(pady=(10, 0))
        self.status_label_extract = tk.Label(self.extract_tab, text="", fg="blue")
        self.status_label_extract.pack()

    def browse_zip(self):
        path = filedialog.askopenfilename(filetypes=[("ZIP files", "*.zip")])
        if path:
            self.zip_path.set(path)

    def browse_extract_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.extract_path.set(path)

    def start_extraction(self):
        zip_file = self.zip_path.get()
        extract_to = self.extract_path.get()
        if not zip_file or not extract_to:
            messagebox.showwarning("Missing Info", "Please select both a ZIP file and destination folder.")
            return

        self.progress_bar_extract['value'] = 0
        self.status_label_extract.config(text="Starting extraction...")
        threading.Thread(target=self.extract_zip, args=(zip_file, extract_to), daemon=True).start()

    def extract_zip(self, zip_path, extract_path):
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                file_list = zip_ref.namelist()
                total = len(file_list)
                for i, file in enumerate(file_list, 1):
                    zip_ref.extract(file, extract_path)
                    percent = int((i / total) * 100)
                    self.progress_bar_extract['value'] = percent
                    self.status_label_extract.config(text=f"Extracting... {percent}%")
                    self.master.update_idletasks()
            self.status_label_extract.config(text="Extraction complete!")
            messagebox.showinfo("Success", f"Extracted to:\n{extract_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Extraction failed:\n{e}")

    # ==== ZIP Tab ====
    def setup_zip_tab(self):
        self.folder_to_zip = tk.StringVar()
        self.zip_output_path = tk.StringVar()

        self.build_entry_row(self.zip_tab, "Folder to ZIP:", self.folder_to_zip, self.browse_folder_to_zip)
        self.build_entry_row(self.zip_tab, "Save ZIP As:", self.zip_output_path, self.choose_zip_save_location)

        ttk.Button(self.zip_tab, text="Create ZIP", command=self.start_zipping).pack(pady=10)

        self.progress_bar_zip = ttk.Progressbar(self.zip_tab, length=400, mode='determinate')
        self.progress_bar_zip.pack(pady=(10, 0))
        self.status_label_zip = tk.Label(self.zip_tab, text="", fg="blue")
        self.status_label_zip.pack()

    def browse_folder_to_zip(self):
        path = filedialog.askdirectory()
        if path:
            self.folder_to_zip.set(path)

    def choose_zip_save_location(self):
        path = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=[("ZIP files", "*.zip")])
        if path:
            self.zip_output_path.set(path)

    def start_zipping(self):
        folder = self.folder_to_zip.get()
        zip_path = self.zip_output_path.get()
        if not folder or not zip_path:
            messagebox.showwarning("Missing Info", "Please select both a folder and save location.")
            return

        self.progress_bar_zip['value'] = 0
        self.status_label_zip.config(text="Starting compression...")
        threading.Thread(target=self.create_zip, args=(folder, zip_path), daemon=True).start()

    def create_zip(self, folder_path, zip_path):
        try:
            file_list = []
            for root, _, files in os.walk(folder_path):
                for file in files:
                    file_list.append(os.path.join(root, file))
            total = len(file_list)

            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for i, file in enumerate(file_list, 1):
                    arcname = os.path.relpath(file, folder_path)
                    zipf.write(file, arcname)
                    percent = int((i / total) * 100)
                    self.progress_bar_zip['value'] = percent
                    self.status_label_zip.config(text=f"Compressing... {percent}%")
                    self.master.update_idletasks()
            self.status_label_zip.config(text="Compression complete!")
            messagebox.showinfo("Success", f"ZIP created:\n{zip_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Compression failed:\n{e}")

    # ==== Helper ====
    def build_entry_row(self, parent, label_text, variable, browse_command):
        frame = tk.Frame(parent)
        frame.pack(fill='x', padx=10, pady=6)
        tk.Label(frame, text=label_text, width=14, anchor='w').pack(side='left')
        tk.Entry(frame, textvariable=variable, width=40).pack(side='left', padx=5, fill='x', expand=True)
        ttk.Button(frame, text="Browse", command=browse_command).pack(side='right')

def main():
    root = tk.Tk()
    app = ModernWinRARClone(root)
    root.mainloop()

if __name__ == "__main__":
    main()
