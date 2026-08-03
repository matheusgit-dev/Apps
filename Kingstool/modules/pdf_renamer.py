import os
import re
import uuid
import threading
from tkinter import filedialog
from pypdf import PdfReader
import customtkinter as ctk

APP_INFO = {
    "id": "pdf_renamer",
    "title": "Renomeador de PDF",
    "description": "Extrai nomes de favorecidos/beneficiários de comprovantes PDF em todas as pastas e subpastas, renomeando-os automaticamente.",
    "icon": ""
}

TERMOS_BUSCA = [
    "Favorecido",
    "Beneficiário",
    "Beneficiario",
]

class AppView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self.total_files = 0
        self.processed_files = 0

        self.label_title = ctk.CTkLabel(
            self, text="Renomeador de PDF", font=("Segoe UI", 18, "bold"), text_color="#C0C0C0"
        )
        self.label_title.pack(anchor="w", pady=(0, 5))

        self.label_desc = ctk.CTkLabel(
            self, text="Selecione uma pasta para buscar e renomear comprovantes em PDF (incluindo subpastas).", 
            font=("Segoe UI", 13), text_color="#9E9E9E"
        )
        self.label_desc.pack(anchor="w", pady=(0, 15))

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
        self.path_entry.pack(fill="x", pady=(0, 15))

        self.actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.actions_frame.pack(fill="x", pady=(0, 15))

        self.select_btn = ctk.CTkButton(
            self.actions_frame, 
            text="Selecionar Pasta", 
            font=("Segoe UI", 13, "bold"),
            height=40,
            fg_color="#0A0A0A", 
            hover_color="#1A4D8F", 
            text_color="#C0C0C0",
            command=self.select_folder
        )
        self.select_btn.pack(side="left", padx=(0, 10))

        self.start_btn = ctk.CTkButton(
            self.actions_frame, 
            text="Iniciar Processamento", 
            font=("Segoe UI", 13, "bold"),
            height=40,
            fg_color="#0A0A0A", 
            hover_color="#1A4D8F", 
            text_color="#C0C0C0",
            command=self.start_processing_thread
        )
        self.start_btn.pack(side="left")

        self.progress_bar = ctk.CTkProgressBar(self, height=12, corner_radius=6, fg_color="#0A0A0A", progress_color="#1A4D8F")
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", pady=(0, 15))

        self.log_box = ctk.CTkTextbox(
            self, font=("Segoe UI", 12), height=250, fg_color="#0A0A0A", 
            text_color="#C0C0C0", border_color="#0A0A0A", corner_radius=5
        )
        self.log_box.pack(fill="x", expand=True)

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, folder)

    def append_log(self, message):
        self.log_box.insert("end", message + "\n")
        self.log_box.see("end")

    def start_processing_thread(self):
        threading.Thread(target=self.process_pdfs, daemon=True).start()

    def process_pdfs(self):
        folder_path = self.path_entry.get().strip()

        if not folder_path or not os.path.exists(folder_path):
            self.append_log("[ERRO] Por favor, selecione uma pasta válida.")
            return

        pdf_tasks = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(".pdf"):
                    pdf_tasks.append((root, file))

        self.total_files = len(pdf_tasks)

        if self.total_files == 0:
            self.append_log("[AVISO] Nenhum arquivo PDF encontrado na pasta selecionada ou subpastas.")
            return

        self.processed_files = 0
        self.progress_bar.set(0)
        self.append_log(f"--- Iniciando processamento de {self.total_files} arquivo(s) ---")

        padrao_regex = r"(?:" + "|".join(re.escape(term) for term in TERMOS_BUSCA) + r"):\s*(.+)"

        for current_root, filename in pdf_tasks:
            filepath = os.path.join(current_root, filename)
            temp_name = f"temp_{uuid.uuid4().hex}.pdf"
            temp_path = os.path.join(current_root, temp_name)

            try:
                os.rename(filepath, temp_path)
                reader = PdfReader(temp_path)
                extracted_text = ""

                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        extracted_text += text + "\n"

                match = re.search(padrao_regex, extracted_text, re.IGNORECASE)

                if not match:
                    self.append_log(f"[PULADO] (Termo de busca não encontrado): {filename}")
                    restored_path = os.path.join(current_root, filename)
                    os.rename(temp_path, restored_path)
                else:
                    raw_name = match.group(1).strip().split("\n")[0]
                    beneficiary_name = re.sub(r'[<>:"/\\|?*]', "_", raw_name)
                    
                    if not beneficiary_name:
                        new_filename = filename
                    else:
                        new_filename = f"{beneficiary_name}.pdf"

                    new_path = os.path.join(current_root, new_filename)

                    counter = 1
                    while os.path.exists(new_path) and new_path != temp_path:
                        new_filename = f"{beneficiary_name} ({counter}).pdf"
                        new_path = os.path.join(current_root, new_filename)
                        counter += 1

                    os.rename(temp_path, new_path)
                    self.append_log(f"[SUCESSO] {filename} -> {new_filename}")

            except Exception as e:
                try:
                    if os.path.exists(temp_path):
                        restored_path = os.path.join(current_root, filename)
                        os.rename(temp_path, restored_path)
                except Exception:
                    pass
                self.append_log(f"[ERRO] Falha ao processar {filename}: {str(e)}")

            self.processed_files += 1
            self.progress_bar.set(self.processed_files / self.total_files)

        self.append_log("--- Processamento concluído! ---")