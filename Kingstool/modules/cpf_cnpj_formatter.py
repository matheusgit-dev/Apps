import re
import customtkinter as ctk

APP_INFO = {
    "id": "cpf_cnpj_formatter",
    "title": "Formatador de CPF / CNPJ",
    "description": "Adiciona ou remove a pontuação padrão de listas de CPFs e CNPJs automaticamente.",
    "icon": ""
}

class AppView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self.label_title = ctk.CTkLabel(
            self, text="Formatador de CPF / CNPJ", font=("Segoe UI", 18, "bold"), text_color="#C0C0C0"
        )
        self.label_title.pack(anchor="w", pady=(0, 5))

        self.label_desc = ctk.CTkLabel(
            self, text="Cole a lista de documentos abaixo para formatar tudo de uma vez.", 
            font=("Segoe UI", 13), text_color="#9E9E9E"
        )
        self.label_desc.pack(anchor="w", pady=(0, 15))

        self.entrada = ctk.CTkTextbox(
            self, font=("Segoe UI", 13), height=180, fg_color="#0C0C0C", 
            text_color="#C0C0C0", border_color="#242424", corner_radius=5
        )
        self.entrada.pack(fill="x", pady=(0, 15))

        self.options_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.options_frame.pack(fill="x", pady=(0, 15))

        self.btn_formatar = ctk.CTkButton(
            self.options_frame, text="Pontuar (Formatar)", font=("Segoe UI", 13, "bold"), height=40,
            fg_color="#0C0C0C", hover_color="#242424", text_color="#C0C0C0",
            command=self.formatar_documentos
        )
        self.btn_formatar.pack(side="left", padx=(0, 10))

        self.btn_limpar = ctk.CTkButton(
            self.options_frame, text="Remover Pontuação (Só Números)", font=("Segoe UI", 13, "bold"), height=40,
            fg_color="#0C0C0C", hover_color="#242424", text_color="#C0C0C0",
            command=self.remover_pontuacao
        )
        self.btn_limpar.pack(side="left")

        self.label_res = ctk.CTkLabel(
            self, text="Resultado", font=("Segoe UI", 15, "bold"), text_color="#C0C0C0"
        )
        self.label_res.pack(anchor="w", pady=(0, 5))

        self.resultado = ctk.CTkTextbox(
            self, font=("Segoe UI", 13), height=180, fg_color="#0C0C0C", 
            text_color="#C0C0C0", border_color="#242424", corner_radius=5
        )
        self.resultado.pack(fill="x")

    def formatar_doc(self, doc):
        numeros = re.sub(r"\D", "", doc)
        
        if len(numeros) == 11:
            return f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:9]}-{numeros[9:]}"
        elif len(numeros) == 14:
            return f"{numeros[:2]}.{numeros[2:5]}.{numeros[5:8]}/{numeros[8:12]}-{numeros[12:]}"
        else:
            return f"{doc} (Tamanho inválido)" if doc else ""

    def formatar_documentos(self):
        texto = self.entrada.get("1.0", "end-1c")
        linhas = [linha.strip() for linha in texto.split("\n") if linha.strip() != ""]
        
        resultados = []
        for linha in linhas:
            resultados.append(self.formatar_doc(linha))

        self.resultado.delete("1.0", "end")
        self.resultado.insert("1.0", "\n".join(resultados))

    def remover_pontuacao(self):
        texto = self.entrada.get("1.0", "end-1c")
        linhas = [linha.strip() for linha in texto.split("\n") if linha.strip() != ""]
        
        resultados = []
        for linha in linhas:
            numeros = re.sub(r"\D", "", linha)
            if numeros:
                resultados.append(numeros)

        self.resultado.delete("1.0", "end")
        self.resultado.insert("1.0", "\n".join(resultados))