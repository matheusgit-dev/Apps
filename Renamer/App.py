import os
import re
from tkinter import filedialog
from pypdf import PdfReader
import customtkinter as ctk

ctk.set_appearance_mode("dark")

total_files = 0
processed_files = 0

def select_directory():
    selected_dir = filedialog.askdirectory()
    if selected_dir:
        path_entry.delete(0, "end")
        path_entry.insert(0, selected_dir)

def append_log(message):
    log_box.insert("end", message + "\n")
    log_box.see("end")

def update_progress_bar():
    if total_files == 0:
        progress_bar.set(0)
    else:
        progress_bar.set(processed_files / total_files)

def execute_renaming():
    global total_files, processed_files
    root_dir = path_entry.get()
    
    if not root_dir or not os.path.exists(root_dir):
        append_log("Por favor, selecione uma pasta válida.")
        return

    pdf_tasks = []
    for current_root, _, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(".pdf"):
                pdf_tasks.append((current_root, file))

    total_files = len(pdf_tasks)
    processed_files = 0
    
    if total_files == 0:
        append_log("Nenhum arquivo PDF encontrado na pasta selecionada.")
        return

    append_log(f"\n▶ Iniciando processamento: {total_files} PDFs encontrados\n")

    for current_root, file in pdf_tasks:
        old_path = os.path.join(current_root, file)
        try:
            reader = PdfReader(old_path)
            extracted_text = ""
            for page in reader.pages:
                extracted_text += page.extract_text() or ""

            match = re.search(r"Favorecido:\s*(.+)", extracted_text, re.IGNORECASE)
            if not match:
                append_log(f"⚠ Pulado (Favorecido não encontrado): {file}")
            else:
                beneficiary_name = re.sub(r'[<>:"/\\|?*]', "_", match.group(1).strip())
                new_filename = f"{beneficiary_name}.pdf"
                new_path = os.path.join(current_root, new_filename)

                counter = 1
                while os.path.exists(new_path):
                    new_filename = f"{beneficiary_name} ({counter}).pdf"
                    new_path = os.path.join(current_root, new_filename)
                    counter += 1

                os.rename(old_path, new_path)
                append_log(f"✔ Sucesso: {file} → {new_filename}")

        except Exception:
            append_log(f"✖ Erro ao processar o arquivo: {file}")

        processed_files += 1
        update_progress_bar()
        app.update_idletasks()

    append_log("\n🏁 Processo concluído com sucesso!")

app = ctk.CTk()
app.geometry("1000x660")
app.title("Renamer")
app.resizable(False, False)
app.configure(fg_color="#121214")

sidebar = ctk.CTkFrame(app, width=260, corner_radius=0, fg_color="#18181C")
sidebar.pack(side="left", fill="y")

title_label = ctk.CTkLabel(sidebar, text="Renamer", font=("Segoe UI", 18, "bold"), text_color="#E1E1E6")
title_label.pack(pady=(45, 35), padx=20)

select_btn = ctk.CTkButton(
    sidebar, 
    text="Selecionar Pasta", 
    font=("Segoe UI", 13, "bold"), 
    height=42, 
    corner_radius=8,
    fg_color="#29292E", 
    hover_color="#323238", 
    text_color="#E1E1E6"
)
select_btn.configure(command=select_directory)
select_btn.pack(pady=10, padx=25, fill="x")

execute_btn = ctk.CTkButton(
    sidebar, 
    text="Executar", 
    font=("Segoe UI", 13, "bold"), 
    height=42, 
    corner_radius=8,
    fg_color="#384F66", 
    hover_color="#2A3B4D", 
    text_color="#E1E1E6"
)
execute_btn.configure(command=execute_renaming)
execute_btn.pack(pady=10, padx=25, fill="x")

version_label = ctk.CTkLabel(sidebar, text="v2.1.0", font=("Segoe UI", 11), text_color="#7C7C8A")
version_label.pack(side="bottom", pady=25)

main_content = ctk.CTkFrame(app, fg_color="transparent")
main_content.pack(side="right", expand=True, fill="both", padx=35, pady=35)

path_entry = ctk.CTkEntry(
    main_content, 
    placeholder_text="Caminho da pasta selecionada...", 
    font=("Segoe UI", 13), 
    height=45, 
    corner_radius=8,
    fg_color="#18181C",
    border_color="#29292E",
    text_color="#E1E1E6",
    placeholder_text_color="#7C7C8A"
)
path_entry.pack(fill="x", pady=(0, 20))

progress_bar = ctk.CTkProgressBar(
    main_content, 
    height=6, 
    corner_radius=3,
    fg_color="#18181C",
    progress_color="#4C6785"
)
progress_bar.set(0)
progress_bar.pack(fill="x", pady=(0, 20))

log_box = ctk.CTkTextbox(
    main_content, 
    font=("Consolas", 11), 
    corner_radius=8, 
    border_width=1, 
    border_color="#29292E",
    fg_color="#18181C",
    text_color="#C4C4CC"
)
log_box.pack(expand=True, fill="both")

append_log("Sistema inicializado e pronto para uso.")
app.mainloop()
