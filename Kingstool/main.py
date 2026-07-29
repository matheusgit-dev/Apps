import os
import sys
import customtkinter as ctk
import modules.pdf_renamer as pdf_renamer
import modules.text_organizer as text_organizer
import modules.uppercase_converter as uppercase_converter

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
    
ctk.set_appearance_mode("dark")

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1100x700")
        self.title("Kingstool")
        self.configure(fg_color="#242424")
        icon_file = resource_path("icone.ico")
        if os.path.exists(icon_file):
            self.iconbitmap(icon_file)

        self.modules_list = [
            pdf_renamer,
            text_organizer,
            uppercase_converter
        ]

        self.views = {}

        self.create_header()
        self.create_body()
        self.create_home_view()
        self.load_modules()

        self.show_view("home")

    def create_header(self):
        self.header = ctk.CTkFrame(self, height=45, corner_radius=0, fg_color="#0A0A0A")
        self.header.pack(side="top", fill="x")

        self.header_left = ctk.CTkLabel(
            self.header, 
            text="Kingstool", 
            font=("Segoe UI", 13, "bold"), 
            text_color="#C0C0C0"
        )
        self.header_left.pack(side="left", padx=15, pady=10)

        self.settings_btn = ctk.CTkButton(
            self.header, 
            text="Configurações", 
            width=110, 
            height=30, 
            corner_radius=5,
            fg_color="transparent", 
            hover_color="#1A4D8F", 
            font=("Segoe UI", 13),
            text_color="#C0C0C0",
            command=lambda: print("Abrir Configurações")
        )
        self.settings_btn.pack(side="right", padx=15, pady=7)

    def create_body(self):
        self.body_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.body_frame.pack(expand=True, fill="both")

        self.sidebar = ctk.CTkFrame(self.body_frame, width=160, corner_radius=0, fg_color="#1C1C1C")
        self.sidebar.pack(side="left", fill="y")

        home_btn = ctk.CTkButton(
            self.sidebar, 
            text="Inicio", 
            height=38, 
            corner_radius=5,
            font=("Segoe UI", 13, "bold"),
            fg_color="#0A0A0A", 
            hover_color="#1A4D8F",
            text_color="#C0C0C0",
            command=lambda: self.show_view("home")
        )
        home_btn.pack(pady=(15, 10), padx=10, fill="x")

        divider = ctk.CTkFrame(self.sidebar, height=2, fg_color="#29292E")
        divider.pack(fill="x", padx=10, pady=5)

        self.main_content = ctk.CTkFrame(self.body_frame, fg_color="transparent")
        self.main_content.pack(side="right", expand=True, fill="both", padx=25, pady=25)

    def create_home_view(self):
        home_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")

        welcome_title = ctk.CTkLabel(
            home_frame, 
            text="Bem-vindo ao Dashboard!", 
            font=("Segoe UI", 22, "bold"), 
            text_color="#C0C0C0"
        )
        welcome_title.pack(anchor="w", pady=(0, 5))

        welcome_sub = ctk.CTkLabel(
            home_frame, 
            text="Selecione um dos aplicativos abaixo ou navegue pelo menu lateral para começar.", 
            font=("Segoe UI", 13), 
            text_color="#9E9E9E"
        )
        welcome_sub.pack(anchor="w", pady=(0, 25))

        self.cards_container = ctk.CTkScrollableFrame(home_frame, fg_color="transparent")
        self.cards_container.pack(expand=True, fill="both")

        self.views["home"] = home_frame

    def load_modules(self):
        for mod in self.modules_list:
            info = mod.APP_INFO
            app_id = info["id"]

            view_instance = mod.AppView(self.main_content)
            self.views[app_id] = view_instance

            side_btn = ctk.CTkButton(
                self.sidebar, 
                text=info["title"], 
                height=38, 
                corner_radius=5,
                font=("Segoe UI", 13),
                anchor="w",
                fg_color="transparent", 
                hover_color="#1A4D8F",
                text_color="#C0C0C0",
                command=lambda id_=app_id: self.show_view(id_)
            )
            side_btn.pack(pady=4, padx=10, fill="x")

            self.create_card(info)

    def create_card(self, info):
        card = ctk.CTkFrame(self.cards_container, fg_color="#1C1C1C", corner_radius=5)
        card.pack(fill="x", pady=8, padx=5)

        top_row = ctk.CTkFrame(card, fg_color="transparent")
        top_row.pack(fill="x", padx=15, pady=(15, 5))

        card_title = ctk.CTkLabel(
            top_row, 
            text=info['title'], 
            font=("Segoe UI", 15, "bold"), 
            text_color="#C0C0C0"
        )
        card_title.pack(side="left")

        open_btn = ctk.CTkButton(
            top_row, 
            text="Abrir App", 
            width=90, 
            height=32, 
            corner_radius=5,
            fg_color="#0A0A0A", 
            hover_color="#1A4D8F", 
            font=("Segoe UI", 12, "bold"),
            text_color="#C0C0C0",
            command=lambda id_=info["id"]: self.show_view(id_)
        )
        open_btn.pack(side="right")

        card_desc = ctk.CTkLabel(
            card, 
            text=info["description"], 
            font=("Segoe UI", 12), 
            text_color="#9E9E9E", 
            wraplength=700, 
            justify="left"
        )
        card_desc.pack(anchor="w", padx=15, pady=(0, 15))

    def show_view(self, view_id):
        for view in self.views.values():
            view.pack_forget()

        if view_id in self.views:
            self.views[view_id].pack(expand=True, fill="both")

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()