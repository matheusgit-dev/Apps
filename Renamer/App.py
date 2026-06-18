import customtkinter as ctk
import os
import re
from tkinter import filedialog
from pypdf import PdfReader

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# =========================
# VARIÁVEIS
# =========================
total = 0
processados = 0


# =========================
# FUNÇÕES
# =========================
def escolher_pasta():
    pasta = filedialog.askdirectory()
    if pasta:
        entry.delete(0, "end")
        entry.insert(0, pasta)


def log(msg):
    log_box.insert("end", msg + "\n")
    log_box.see("end")


def atualizar_barra():
    if total == 0:
        progress.set(0)
    else:
        progress.set(processados / total)


def executar():
    global total, processados

    pasta = entry.get()

    if not pasta:
        log("Selecione uma pasta")
        return

    arquivos = [f for f in os.listdir(pasta) if f.endswith(".pdf")]

    total = len(arquivos)
    processados = 0

    log(f"\n▶ Iniciando: {total} PDFs encontrados\n")

    for file in arquivos:
        path = os.path.join(pasta, file)

        try:
            reader = PdfReader(path)

            text = ""
            for p in reader.pages:
                text += p.extract_text() or ""

            match = re.search(r"Favorecido:\s*(.+)", text, re.IGNORECASE)

            if not match:
                log(f"✖ sem favorecido: {file}")
            else:
                name = re.sub(r'[<>:"/\\|?*]', "_", match.group(1).strip())

                new_path = os.path.join(pasta, f"{name}.pdf")

                i = 1
                while os.path.exists(new_path):
                    new_path = os.path.join(pasta, f"{name} ({i}).pdf")
                    i += 1

                os.rename(path, new_path)

                log(f"✔ {file} → {os.path.basename(new_path)}")

        except Exception as e:
            log(f"erro: {file}")

        processados += 1
        atualizar_barra()
        app.update_idletasks()


# =========================
# UI
# =========================
app = ctk.CTk()
app.geometry("1000x650")
app.title("PDF Renamer Pro")


# SIDEBAR
sidebar = ctk.CTkFrame(app, width=200)
sidebar.pack(side="left", fill="y")

title = ctk.CTkLabel(sidebar, text="PDF TOOL", font=("Arial", 20, "bold"))
title.pack(pady=20)

btn1 = ctk.CTkButton(sidebar, text="Selecionar Pasta", command=escolher_pasta)
btn1.pack(pady=10)

btn2 = ctk.CTkButton(sidebar, text="Executar", command=executar, fg_color="#0066ff")
btn2.pack(pady=10)


# MAIN AREA
main = ctk.CTkFrame(app)
main.pack(side="right", expand=True, fill="both", padx=10, pady=10)


entry = ctk.CTkEntry(main, width=600, placeholder_text="Pasta dos PDFs...")
entry.pack(pady=20)


# PROGRESS BAR
progress = ctk.CTkProgressBar(main, width=600)
progress.set(0)
progress.pack(pady=10)


# LOG
log_box = ctk.CTkTextbox(main)
log_box.pack(expand=True, fill="both", pady=10)

log("Sistema pronto.")
app.mainloop()
