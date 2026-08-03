import customtkinter as ctk

APP_INFO = {
    "id": "text_organizer",
    "title": "Organizador de Texto",
    "description": "Transforma várias linhas de texto em uma única sequência com um separador customizável.",
    "icon": ""
}

class AppView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self.label_title = ctk.CTkLabel(
            self, text="Organizador de Texto", font=("Segoe UI", 18, "bold"), text_color="#C0C0C0"
        )
        self.label_title.pack(anchor="w", pady=(0, 5))

        self.label_desc = ctk.CTkLabel(
            self, text="Cole as linhas abaixo para agrupar tudo em uma sequência única.", 
            font=("Segoe UI", 13), text_color="#9E9E9E"
        )
        self.label_desc.pack(anchor="w", pady=(0, 20))

        self.entrada = ctk.CTkTextbox(
            self, font=("Segoe UI", 13), height=200, fg_color="#0C0C0C", 
            text_color="#C0C0C0", border_color="#242424", corner_radius=5
        )
        self.entrada.pack(fill="x", pady=(0, 15))

        self.options_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.options_frame.pack(fill="x", pady=(0, 20))

        self.label_sep = ctk.CTkLabel(
            self.options_frame, text="Separador:", font=("Segoe UI", 13, "bold"), text_color="#C0C0C0"
        )
        self.label_sep.pack(side="left", padx=(0, 10))

        self.sep_entry = ctk.CTkEntry(
            self.options_frame, font=("Segoe UI", 13), width=80, height=40,
            fg_color="#0C0C0C", border_color="#242424", text_color="#C0C0C0", corner_radius=5
        )
        self.sep_entry.insert(0, ", ")
        self.sep_entry.pack(side="left", padx=(0, 20))

        self.btn_organizar = ctk.CTkButton(
            self.options_frame, text="Arrumar Texto", font=("Segoe UI", 13, "bold"), height=40,
            fg_color="#0C0C0C", hover_color="#242424", text_color="#C0C0C0",
            command=self.organizar
        )
        self.btn_organizar.pack(side="left")

        self.label_res = ctk.CTkLabel(
            self, text="Resultado", font=("Segoe UI", 15, "bold"), text_color="#C0C0C0"
        )
        self.label_res.pack(anchor="w", pady=(0, 5))

        self.resultado = ctk.CTkTextbox(
            self, font=("Segoe UI", 13), height=150, fg_color="#0C0C0C", 
            text_color="#C0C0C0", border_color="#242424", corner_radius=5
        )
        self.resultado.pack(fill="x")

    def organizar(self):
        texto = self.entrada.get("1.0", "end-1c")
        
        separador = self.sep_entry.get() 
        
        linhas = [linha.strip() for linha in texto.split("\n") if linha.strip() != ""]
        
        texto_final = separador.join(linhas)
        
        self.resultado.delete("1.0", "end")
        self.resultado.insert("1.0", texto_final)