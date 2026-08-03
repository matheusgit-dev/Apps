import os
import sys
import ctypes
from ctypes import wintypes
import customtkinter as ctk
import modules.pdf_renamer as pdf_renamer
import modules.text_organizer as text_organizer
import modules.uppercase_converter as uppercase_converter
import modules.settings as settings
import modules.cpf_cnpj_formatter as cpf_cnpj_formatter

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
        self.configure(fg_color="#111111")

        self.overrideredirect(True)

        self._offset_x = 0
        self._offset_y = 0
        self.is_maximized = False
        self.normal_geometry = "1100x700+100+100"
        
        self.accent_color = "#242424"

        icon_file = resource_path("icone.ico")
        if os.path.exists(icon_file):
            self.iconbitmap(icon_file)

        self.modules_list = [
            pdf_renamer,
            text_organizer,
            uppercase_converter,
            cpf_cnpj_formatter
        ]

        self.views = {}

        self.create_header()
        self.create_body()
        self.create_home_view()
        self.load_modules()
        
        self.views["settings"] = settings.AppView(self.main_content)

        self.after(10, self.setup_taskbar_icon)
        self.show_view("home")

    def setup_taskbar_icon(self):
        GWL_EXSTYLE = -20
        WS_EX_APPWINDOW = 0x00040000
        WS_EX_TOOLWINDOW = 0x00000080

        hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
        style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        style = (style & ~WS_EX_TOOLWINDOW) | WS_EX_APPWINDOW
        ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)

    def set_accent(self, new_color):
        old_color = self.accent_color
        self.accent_color = new_color
        
        def update_widget(w):
            try:
                if getattr(w, "_is_static_color", False):
                    return

                if hasattr(w, "cget"):
                    if isinstance(w, ctk.CTkButton):
                        if w.cget("hover_color") == old_color:
                            w.configure(hover_color=new_color)
                        if w.cget("fg_color") == old_color:
                            w.configure(fg_color=new_color)
                    elif isinstance(w, ctk.CTkProgressBar):
                        if w.cget("progress_color") == old_color:
                            w.configure(progress_color=new_color)
            except Exception:
                pass
            for child in w.winfo_children():
                update_widget(child)
                
        update_widget(self)

    def create_header(self):
        self.header = ctk.CTkFrame(self, height=45, corner_radius=0, fg_color="#0C0C0C")
        self.header.pack(side="top", fill="x")

        self.header.bind("<ButtonPress-1>", self.start_move)
        self.header.bind("<B1-Motion>", self.do_move)
        self.header.bind("<Double-Button-1>", self.toggle_maximize)

        self.header_left = ctk.CTkLabel(
            self.header, 
            text="Kingstool", 
            font=("Segoe UI", 13, "bold"), 
            text_color="#C0C0C0"
        )
        self.header_left.pack(side="left", padx=15, pady=10)
        self.header_left.bind("<ButtonPress-1>", self.start_move)
        self.header_left.bind("<B1-Motion>", self.do_move)
        self.header_left.bind("<Double-Button-1>", self.toggle_maximize)

        self.close_btn = ctk.CTkButton(
            self.header, 
            text="✕", 
            width=45, 
            height=45, 
            corner_radius=0,
            fg_color="transparent", 
            hover_color="#242424", 
            text_color="#C0C0C0",
            command=self.destroy
        )
        self.close_btn._is_static_color = True
        self.close_btn.pack(side="right")

        self.maximize_btn = ctk.CTkButton(
            self.header, 
            text="□", 
            width=45, 
            height=45, 
            corner_radius=0,
            fg_color="transparent", 
            hover_color=self.accent_color, 
            text_color="#C0C0C0",
            command=self.toggle_maximize
        )
        self.maximize_btn.pack(side="right")

        self.minimize_btn = ctk.CTkButton(
            self.header, 
            text="─", 
            width=45, 
            height=45, 
            corner_radius=0,
            fg_color="transparent", 
            hover_color=self.accent_color, 
            text_color="#C0C0C0",
            command=self.minimize_window
        )
        self.minimize_btn.pack(side="right")

        self.settings_btn = ctk.CTkButton(
            self.header, 
            text="Configurações", 
            width=110, 
            height=30, 
            corner_radius=5,
            fg_color="transparent", 
            hover_color=self.accent_color, 
            font=("Segoe UI", 13),
            text_color="#C0C0C0",
            command=lambda: self.show_view("settings")
        )
        self.settings_btn.pack(side="right", padx=10, pady=7)

    def start_move(self, event):
        if self.is_maximized:
            self.toggle_maximize()
            self._offset_x = event.x + (self.winfo_width() // 2)
        else:
            self._offset_x = event.x
        self._offset_y = event.y

    def do_move(self, event):
        if not self.is_maximized:
            x = self.winfo_pointerx() - self._offset_x
            y = self.winfo_pointery() - self._offset_y
            self.geometry(f"+{x}+{y}")

    def toggle_maximize(self, event=None):
        if not self.is_maximized:
            self.normal_geometry = self.geometry()
            SPI_GETWORKAREA = 48
            rect = wintypes.RECT()
            ctypes.windll.user32.SystemParametersInfoW(SPI_GETWORKAREA, 0, ctypes.byref(rect), 0)
            width = rect.right - rect.left
            height = rect.bottom - rect.top
            self.geometry(f"{width}x{height}+{rect.left}+{rect.top}")
            self.maximize_btn.configure(text="❐")
            self.is_maximized = True
        else:
            self.geometry(self.normal_geometry)
            self.maximize_btn.configure(text="□")
            self.is_maximized = False

    def minimize_window(self):
        self.attributes("-alpha", 0.0)
        self.overrideredirect(False)
        self.iconify()
        self.bind("<Map>", self.on_restore)

    def on_restore(self, event=None):
        if self.state() == "normal":
            self.unbind("<Map>")
            self.overrideredirect(True)
            self.attributes("-alpha", 1.0)

    def create_body(self):
        self.body_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.body_frame.pack(expand=True, fill="both")

        self.sidebar = ctk.CTkFrame(self.body_frame, width=160, corner_radius=0, fg_color="#111111")
        self.sidebar.pack(side="left", fill="y")

        home_btn = ctk.CTkButton(
            self.sidebar, 
            text="Inicio", 
            height=38, 
            corner_radius=5,
            border_width=1,
            border_color="#242424",
            font=("Segoe UI", 13, "bold"),
            fg_color="#0C0C0C", 
            hover_color=self.accent_color,
            text_color="#C0C0C0",
            command=lambda: self.show_view("home")
        )
        home_btn.pack(pady=(15, 10), padx=10, fill="x")

        divider = ctk.CTkFrame(self.sidebar, height=2, fg_color="#242424")
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
                hover_color=self.accent_color,
                text_color="#C0C0C0",
                command=lambda id_=app_id: self.show_view(id_)
            )
            side_btn.pack(pady=4, padx=10, fill="x")

            self.create_card(info)

    def create_card(self, info):
        card = ctk.CTkFrame(self.cards_container, fg_color="#0C0C0C", corner_radius=5)
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
            fg_color="#171717", 
            hover_color=self.accent_color, 
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