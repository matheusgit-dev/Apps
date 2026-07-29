import os
import re
import uuid
from tkinter import filedialog
from pypdf import PdfReader
import customtkinter as ctk

APP_INFO = {
    "id": "pdf_renamer",
    "title": "Renomeador de PDF",
    "description": "Extrai o nome do favorecido de comprovantes PDF e renomeia os arquivos automaticamente.",
    "icon": ""
}

class AppView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self.total_files = 0
        self.processed_files = 0

        self.path_entry = ctk.CTkEntry(
            self, 
            placeholder_text="Caminho da pasta selecionada...", 
            font=("Segoe UI", 13), 
            height=45, 
            corner_radius=5,
            border_color="#0A0A0A",
            fg_color="#0A0A0A",
            text_color="#C0C0C0",
            placeholder_text_color="#9E9E9E"
        )
        self.path_entry.pack(fill="x", pady=(0, 20))

        self.actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.actions_frame.pack(fill="x", pady=(0, 15))

        self.select_btn = ctk.CTkButton(
            self.actions_frame, 
            text="Selecionar Pasta", 
            font=("Segoe UI", 13, "bold"), 
            height=40, 
            corner_radius=8,
            fg_color="#0A0A0A", 
            hover_color="#1A4D8F", 
            text_color="#C0C0C0",
            command=self.select_directory
        )
        self.select_btn.pack(side="left", padx=(0, 10))

        self.execute_btn = ctk.CTkButton(
            self.actions_frame, 
            text="Executar", 
            font=("Segoe UI", 13, "bold"), 
            height=40, 
            corner_radius=8,
            fg_color="#0A0A0A", 
            hover_color="#1A4D8F", 
            text_color="#C0C0C0",
            command=self.execute_renaming
        )
        self.execute_btn.pack(side="left")

        self.progress_bar = ctk.CTkProgressBar(
            self, 
            height=6, 
            corner_radius=3,
            fg_color="#0A0A0A",
            progress_color="#1A4D8F"
        )
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", pady=(0, 20))

        self.log_box = ctk.CTkTextbox(
            self, 
            font=("Segoe UI", 11), 
            corner_radius=5, 
            fg_color="#0A0A0A",
            text_color="#C0C0C0"
        )
        self.log_box.pack(expand=True, fill="both")

        self.append_log("Sistema de renomeação pronto para uso.")

    def select_directory(self):
        selected_dir = filedialog.askdirectory()
        if selected_dir:
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, selected_dir)

    def append_log(self, message):
        self.log_box.insert("end", message + "\n")
        self.log_box.see("end")

    def update_progress_bar(self):
        if self.total_files == 0:
            self.progress_bar.set(0)
        else:
            self.progress_bar.set(self.processed_files / self.total_files)

    def execute_renaming(self):
        root_dir = self.path_entry.get()
        if not root_dir or not os.path.exists(root_dir):
            self.append_log("Por favor, selecione uma pasta válida.")
            return

        raw_pdf_files = []
        for current_root, _, files in os.walk(root_dir):
            for file in files:
                if file.lower().endswith(".pdf"):
                    raw_pdf_files.append((current_root, file))

        self.total_files = len(raw_pdf_files)
        self.processed_files = 0

        if self.total_files == 0:
            self.append_log("Nenhum arquivo PDF encontrado na pasta selecionada.")
            return

        self.append_log(f"\nIniciando processamento: {self.total_files} PDFs encontrados\n")

        temp_pdf_tasks = []
        for current_root, file in raw_pdf_files:
            old_path = os.path.join(current_root, file)
            temp_filename = f"temp_{uuid.uuid4().hex[:8]}.pdf"
            temp_path = os.path.join(current_root, temp_filename)
            
            try:
                os.rename(old_path, temp_path)
                temp_pdf_tasks.append((current_root, temp_filename, file))
            except Exception:
                self.append_log(f"[ERRO] Falha ao preparar arquivo: {file}")

        for current_root, temp_filename, original_filename in temp_pdf_tasks:
            temp_path = os.path.join(current_root, temp_filename)
            try:
                reader = PdfReader(temp_path)
                extracted_text = ""
                for page in reader.pages:
                    extracted_text += page.extract_text() or ""

                match = re.search(r"Favorecido:\s*(.+)", extracted_text, re.IGNORECASE)
                if not match:
                    self.append_log(f"[PULADO] (Favorecido não encontrado): {original_filename}")
                    new_filename = original_filename
                else:
                    beneficiary_name = re.sub(r'[<>:"/\\|?*]', "_", match.group(1).strip())
                    new_filename = f"{beneficiary_name}.pdf"

                new_path = os.path.join(current_root, new_filename)

                counter = 1
                while os.path.exists(new_path) and new_path != temp_path:
                    new_filename = f"{beneficiary_name} ({counter}).pdf"
                    new_path = os.path.join(current_root, new_filename)
                    counter += 1

                os.rename(temp_path, new_path)
                self.append_log(f"[SUCESSO] {original_filename} -> {new_filename}")
            except Exception:
                try:
                    restored_path = os.path.join(current_root, original_filename)
                    os.rename(temp_path, restored_path)
                except Exception:
                    pass
                self.append_log(f"[ERRO] Erro ao processar o arquivo: {original_filename}")

            self.processed_files += 1
            self.update_progress_bar()
            self.update_idletasks()

        self.append_log("\nProcesso concluído com sucesso!")