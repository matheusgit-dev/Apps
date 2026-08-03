import customtkinter as ctk

APP_INFO = {
    "id": "settings",
    "title": "Configurações",
    "description": "Personalize a cor de destaque do aplicativo.",
    "icon": ""
}

class AppView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        self.app = self.winfo_toplevel()

        self.title_lbl = ctk.CTkLabel(
            self, text="Configurações", font=("Segoe UI", 22, "bold"), text_color="#C0C0C0"
        )
        self.title_lbl.pack(anchor="w", pady=(0, 25))

        self.color_frame = ctk.CTkFrame(self, fg_color="#1C1C1C", corner_radius=8)
        self.color_frame.pack(fill="x", pady=(0, 15), ipadx=15, ipady=15)

        self.color_info = ctk.CTkFrame(self.color_frame, fg_color="transparent")
        self.color_info.pack(side="left", fill="x", expand=True)
        
        self.color_title = ctk.CTkLabel(
            self.color_info, text="Cor de Destaque", font=("Segoe UI", 16, "bold"), text_color="#C0C0C0"
        )
        self.color_title.pack(anchor="w")
        
        self.color_desc = ctk.CTkLabel(
            self.color_info, text="Escolha a cor principal para detalhes, seleções e hovers.", font=("Segoe UI", 13), text_color="#9E9E9E"
        )
        self.color_desc.pack(anchor="w")

        self.color_btns = ctk.CTkFrame(self.color_frame, fg_color="transparent")
        self.color_btns.pack(side="right")

        colors = [
            ("#1A4D8F", "Azul Padrão"), 
            ("#007ACC", "Azul Celeste"),
            ("#009688", "Verde Água"),
            ("#1A8F35", "Verde"), 
            ("#D4AC0D", "Amarelo"),
            ("#E67E22", "Laranja"),
            ("#C42B1C", "Vermelho"), 
            ("#D11582", "Rosa"),
            ("#8E44AD", "Violeta"),
            ("#6B1A8F", "Roxo")
        ]
        
        row1 = ctk.CTkFrame(self.color_btns, fg_color="transparent")
        row1.pack(pady=3)
        row2 = ctk.CTkFrame(self.color_btns, fg_color="transparent")
        row2.pack(pady=3)

        for i, (hex_code, name) in enumerate(colors):
            parent_row = row1 if i < 5 else row2
            btn = ctk.CTkButton(
                parent_row, text="", width=28, height=28, corner_radius=14, 
                fg_color=hex_code, hover_color=hex_code, 
                command=lambda h=hex_code: self.app.set_accent(h)
            )
            btn._is_static_color = True
            btn.pack(side="left", padx=4)