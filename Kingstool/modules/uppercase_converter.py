import customtkinter as ctk

APP_INFO = {
    "id": "uppercase_converter",
    "title": "Conversor Caixa Alta",
    "description": "Converte rapidamente qualquer bloco de texto para letras maiúsculas.",
    "icon": ""
}

class AppView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self.label_title = ctk.CTkLabel(
            self, text="Conversor para Caixa Alta", font=("Segoe UI", 18, "bold"), text_color="#C0C0C0"
        )
        self.label_title.pack(anchor="w", pady=(0, 5))

        self.label_desc = ctk.CTkLabel(
            self, text="Digite ou cole o texto para converter tudo para MAIÚSCULAS.", 
            font=("Segoe UI", 13), text_color="#9E9E9E"
        )
        self.label_desc.pack(anchor="w", pady=(0, 20))

        self.texto_io = ctk.CTkTextbox(
            self, font=("Segoe UI", 13), height=350, fg_color="#0A0A0A", 
            text_color="#C0C0C0", border_color="#0A0A0A", corner_radius=5
        )
        self.texto_io.pack(fill="x", pady=(0, 15))

        self.btn_converter = ctk.CTkButton(
            self, text="Converter para MAIÚSCULAS", font=("Segoe UI", 13, "bold"), height=40,
            fg_color="#0A0A0A", hover_color="#1A4D8F", text_color="#C0C0C0",
            command=self.converter
        )
        self.btn_converter.pack(anchor="w")

    def converter(self):
        conteudo = self.texto_io.get("1.0", "end-1c")
        self.texto_io.delete("1.0", "end")
        self.texto_io.insert("1.0", conteudo.upper())