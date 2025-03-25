import tkinter as tk
from tkinter import ttk, messagebox
import bcrypt
from datetime import datetime
import calendar
from utils import (
    center_window, is_valid_phone, is_valid_email, validate_numeric_input,
    create_scrollable_frame, setup_treeview, create_combobox_with_label,
    create_entry_with_label, get_current_date, get_month_name
)
from database import (
    create_connection, get_all_uyeler, get_apartman_bilgileri,
    get_all_banka_hesaplari, get_aidat_for_year
)

class FormBase:
    """Tüm formlar için temel sınıf"""
    def __init__(self, parent, title, width=600, height=400):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title(title)
        self.window.geometry(f"{width}x{height}")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()
        center_window(self.window)
        
        # Ana frame
        self.main_frame = ttk.Frame(self.window, padding=20)
        self.main_frame.pack(fill="both", expand=True)
        
        # Başlık
        self.title_label = ttk.Label(self.main_frame, text=title, font=("Arial", 16, "bold"))
        self.title_label.pack(pady=(0, 20))

class UyeForm(FormBase):
    """Üye ekleme/düzenleme formu"""
    def __init__(self, parent, uye_id=None):
        super().__init__(parent, "Üye Ekle/Düzenle", 600, 500)
        self.uye_id = uye_id
        self.create_widgets()
        self.load_uye_data()
        
    def create_widgets(self):
        # Form alanları
        input_frame = ttk.Frame(self.main_frame)
        input_frame.pack(fill="both", expand=True, pady=10)
        
        # Daire No
        self.daire_no_frame, self.daire_no_entry = create_entry_with_label(
