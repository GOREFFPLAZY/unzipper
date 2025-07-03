import customtkinter as ctk
from tkinter import filedialog, messagebox
import zipfile
import os
import threading


class WinRARCloneApp(ctk.CTk):
    """A minimalist ZIP extractor/creator rebuilt with CustomTkinter for a modern look."""

    def __init__(self):
        super().__init__()

        #Window config
        self.title("Biggies unzipper")
        self.geometry("520x380")
        self.resizable(False, False)

        # Optional appearance settings
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # --- Tabs -
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(expand=True, fill="both", padx=10, pady=10)

        self.extract_tab = self.tabview.add("Extract ZIP")
        self.zip_tab = self.tabview.add("Create ZIP")

        # Build UI for each tab
        self._setup_extract_tab()
        self._setup_zip_tab()

    # === Extract TAB ===
    def _setup_extract_tab(self):
        self.zip_path = ctk.StringVar()
        self.extract_path = ctk.StringVar()

        # Select ZIP file
        ctk.CTkLabel(self.extract_tab, text="Select ZIP File:").pack(anchor="w", pady=(8, 0))
        zip_frame = ctk.CTkFrame(self.extract_tab, fg_color="transparent")
        zip_frame.pack(fill="x")
        ctk.CTkEntry(zip_frame, textvariable=self.zip_path).pack(side="left", expand=True, fill="x", padx=(0, 6))
        ctk.CTkButton(zip_frame, text="Browse", command=self._browse_zip).pack(side="right")

        #Select destination folder
        ctk.CTkLabel(self.extract_tab, text="Select Destination Folder:").pack(anchor="w", pady=(10, 0))
        dest_frame = ctk.CTkFrame(self.extract_tab, fg_color="transparent")
        dest_frame.pack(fill="x")
        ctk.CTkEntry(dest_frame, textvariable=self.extract_path).pack(side="left", expand=True, fill="x", padx=(0, 6))
        ctk.CTkButton(dest_frame, text="Browse", command=self._browse_folder).pack(side="right")

        #Action button & progress
        ctk.CTkButton(self.extract_tab, text="Extract", command=self._start_extraction, height=32).pack(pady=15)
        self.progress_extract = ctk.CTkProgressBar(self.extract_tab, width=400)
        self.progress_extract.pack(pady=6)
        self.progress_extract.set(0)
        self.status_extract = ctk.CTkLabel(self.extract_tab, text="")
        self.status_extract.pack()

    def _browse_zip(self):
        path = filedialog.askopenfilename(filetypes=[("ZIP files", "*.zip")])
        if path:
            self.zip_path.set(path)

    def _browse_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.extract_path.set(path)

    def _start_extraction(self):
        zip_file = self.zip_path.get()
        dest = self.extract_path.get()
        if not zip_file or not dest:
            messagebox.showwarning("Missing Info", "Please select both a ZIP file and a destination folder.")
            return
        self.status_extract.configure(text="Starting extraction…")
        self.progress_extract.set(0)
        threading.Thread(target=self._extract_zip, args=(zip_file, dest), daemon=True).start()

    def _extract_zip(self, zip_file: str, dest: str):
        try:
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                files = zip_ref.namelist()
                total = len(files)
                for i, file in enumerate(files, 1):
                    zip_ref.extract(file, dest)
                    percent = i / total
                    self.progress_extract.set(percent)
                    self.status_extract.configure(text=f"Extracting… {int(percent * 100)}%")
                    self.update_idletasks()

            self.status_extract.configure(text="Extraction complete ✅")
            messagebox.showinfo("Success", f"Files extracted to:\n{dest}")
        except Exception as err:
            messagebox.showerror("Error", f"An error occurred:\n{err}")

    # == ZIP TAB ==
    def _setup_zip_tab(self):
        self.folder_to_zip = ctk.StringVar()
        self.zip_output_path = ctk.StringVar()

        # Select folder
        ctk.CTkLabel(self.zip_tab, text="Select Folder to ZIP:").pack(anchor="w", pady=(8, 0))
        folder_frame = ctk.CTkFrame(self.zip_tab, fg_color="transparent")
        folder_frame.pack(fill="x")
        ctk.CTkEntry(folder_frame, textvariable=self.folder_to_zip).pack(side="left", expand=True, fill="x", padx=(0, 6))
        ctk.CTkButton(folder_frame, text="Browse", command=self._browse_folder_to_zip).pack(side="right")

        #Save location
        ctk.CTkLabel(self.zip_tab, text="Save ZIP As:").pack(anchor="w", pady=(10, 0))
        save_frame = ctk.CTkFrame(self.zip_tab, fg_color="transparent")
        save_frame.pack(fill="x")
        ctk.CTkEntry(save_frame, textvariable=self.zip_output_path).pack(side="left", expand=True, fill="x", padx=(0, 6))
        ctk.CTkButton(save_frame, text="Choose", command=self._choose_zip_save_location).pack(side="right")

        #Action button & progress
        ctk.CTkButton(self.zip_tab, text="Create ZIP", command=self._start_zipping, height=32).pack(pady=15)
        self.progress_zip = ctk.CTkProgressBar(self.zip_tab, width=400)
        self.progress_zip.pack(pady=6)
        self.progress_zip.set(0)
        self.status_zip = ctk.CTkLabel(self.zip_tab, text="")
        self.status_zip.pack()

    def _browse_folder_to_zip(self):
        path = filedialog.askdirectory()
        if path:
            self.folder_to_zip.set(path)

    def _choose_zip_save_location(self):
        path = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=[("ZIP files", "*.zip")])
        if path:
            self.zip_output_path.set(path)

    def _start_zipping(self):
        folder = self.folder_to_zip.get()
        zip_path = self.zip_output_path.get()
        if not folder or not zip_path:
            messagebox.showwarning("Missing Info", "Please select both a folder and a save location.")
            return
        self.status_zip.configure(text="Starting compression…")
        self.progress_zip.set(0)
        threading.Thread(target=self._create_zip, args=(folder, zip_path), daemon=True).start()

    def _create_zip(self, folder_path: str, zip_path: str):
        try:
            file_list = [
                os.path.join(root, file)
                for root, _, files in os.walk(folder_path)
                for file in files
            ]
            total = len(file_list) or 1

            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for i, file in enumerate(file_list, 1):
                    zipf.write(file, os.path.relpath(file, folder_path))
                    percent = i / total
                    self.progress_zip.set(percent)
                    self.status_zip.configure(text=f"Compressing… {int(percent * 100)}%")
                    self.update_idletasks()

            self.status_zip.configure(text="Compression complete ✅")
            messagebox.showinfo("Success", f"Folder zipped to:\n{zip_path}")
        except Exception as err:
            messagebox.showerror("Error", f"An error occurred:\n{err}")


# === Entry Point ===

def main():
    app = WinRARCloneApp()
    app.mainloop()


if __name__ == "__main__":
    main()
