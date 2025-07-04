import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import zipfile
import os
import threading

class WinRARCloneApp:
    def __init__(self, master):
        self.master = master
        self.master.title("unzipper")
        self.master.geometry("500x320")
        self.master.resizable(False, False)

        self.tab_control = ttk.Notebook(master)

        self.extract_tab = ttk.Frame(self.tab_control)
        self.zip_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.extract_tab, text='Extract ZIP')
        self.tab_control.add(self.zip_tab, text='Create ZIP')
        self.tab_control.pack(expand=1, fill="both")

        self.setup_extract_tab()
        self.setup_zip_tab()

    # ======== Extract Tab ========
    def setup_extract_tab(self):
        self.zip_path = tk.StringVar()
        self.extract_path = tk.StringVar()

        tk.Label(self.extract_tab, text="Select ZIP File:").pack(anchor='w', padx=10, pady=(15, 0))
        file_frame = tk.Frame(self.extract_tab)
        file_frame.pack(fill='x', padx=10)
        tk.Entry(file_frame, textvariable=self.zip_path, width=50).pack(side='left', fill='x', expand=True)
        tk.Button(file_frame, text="Browse", command=self.browse_zip).pack(side='right')

        tk.Label(self.extract_tab, text="Select Destination Folder:").pack(anchor='w', padx=10, pady=(15, 0))
        folder_frame = tk.Frame(self.extract_tab)
        folder_frame.pack(fill='x', padx=10)
        tk.Entry(folder_frame, textvariable=self.extract_path, width=50).pack(side='left', fill='x', expand=True)
        tk.Button(folder_frame, text="Browse", command=self.browse_folder).pack(side='right')

        tk.Button(self.extract_tab, text="Extract", command=self.start_extraction, height=2, bg="#4CAF50", fg="white").pack(pady=15)

        self.progress_bar_extract = ttk.Progressbar(self.extract_tab, length=400, mode='determinate')
        self.progress_bar_extract.pack(pady=5)
        self.status_label_extract = tk.Label(self.extract_tab, text="", fg="blue")
        self.status_label_extract.pack()

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

        self.status_label_extract.config(text="Starting extraction...")
        self.progress_bar_extract['value'] = 0
        threading.Thread(target=self.extract_zip, args=(zip_file, extract_to), daemon=True).start()

    def extract_zip(self, zip_path, extract_path):
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                file_list = zip_ref.namelist()
                total_files = len(file_list)

                for i, file in enumerate(file_list, 1):
                    zip_ref.extract(file, extract_path)
                    percent = int((i / total_files) * 100)
                    self.progress_bar_extract['value'] = percent
                    self.status_label_extract.config(text=f"Extracting... {percent}%")
                    self.master.update_idletasks()

            self.status_label_extract.config(text="Extraction complete.")
            messagebox.showinfo("Success", f"Files extracted to:\n{extract_path}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")

    # ======== Zip Tab ========
    def setup_zip_tab(self):
        self.folder_to_zip = tk.StringVar()
        self.zip_output_path = tk.StringVar()

        tk.Label(self.zip_tab, text="Select Folder to ZIP:").pack(anchor='w', padx=10, pady=(15, 0))
        folder_frame = tk.Frame(self.zip_tab)
        folder_frame.pack(fill='x', padx=10)
        tk.Entry(folder_frame, textvariable=self.folder_to_zip, width=50).pack(side='left', fill='x', expand=True)
        tk.Button(folder_frame, text="Browse", command=self.browse_folder_to_zip).pack(side='right')

        tk.Label(self.zip_tab, text="Save ZIP As:").pack(anchor='w', padx=10, pady=(15, 0))
        save_frame = tk.Frame(self.zip_tab)
        save_frame.pack(fill='x', padx=10)
        tk.Entry(save_frame, textvariable=self.zip_output_path, width=50).pack(side='left', fill='x', expand=True)
        tk.Button(save_frame, text="Choose", command=self.choose_zip_save_location).pack(side='right')

        tk.Button(self.zip_tab, text="Create ZIP", command=self.start_zipping, height=2, bg="#2196F3", fg="white").pack(pady=15)

        self.progress_bar_zip = ttk.Progressbar(self.zip_tab, length=400, mode='determinate')
        self.progress_bar_zip.pack(pady=5)
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
            messagebox.showwarning("Missing Info", "Please select both a folder and ZIP save location.")
            return

        self.status_label_zip.config(text="Starting compression...")
        self.progress_bar_zip['value'] = 0
        threading.Thread(target=self.create_zip, args=(folder, zip_path), daemon=True).start()

    def create_zip(self, folder_path, zip_path):
        try:
            file_list = []
            for root, _, files in os.walk(folder_path):
                for file in files:
                    file_list.append(os.path.join(root, file))

            total_files = len(file_list)

            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for i, file in enumerate(file_list, 1):
                    arcname = os.path.relpath(file, folder_path)
                    zipf.write(file, arcname)
                    percent = int((i / total_files) * 100)
                    self.progress_bar_zip['value'] = percent
                    self.status_label_zip.config(text=f"Compressing... {percent}%")
                    self.master.update_idletasks()

            self.status_label_zip.config(text="Compression complete.")
            messagebox.showinfo("Success", f"Folder zipped to:\n{zip_path}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")

def main():
    root = tk.Tk()
    app = WinRARCloneApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
