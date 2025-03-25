import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
from datetime import datetime
import calendar
import os
from utils import (
    center_window, format_currency, create_scrollable_frame, setup_treeview,
    create_combobox_with_label, create_entry_with_label, get_month_name
)
from database import (
    create_connection, get_all_uyeler, get_aidat_for_year, get_aidat_odemeler_by_uye,
    get_giderler, get_all_banka_hesaplari, get_banka_hareketleri
)

class ReportBase:
    """Tüm raporlar için temel sınıf"""
    def __init__(self, parent, title, width=800, height=600):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title(title)
        self.window.geometry(f"{width}x{height}")
        self.window.resizable(True, True)
        self.window.transient(parent)
        self.window.grab_set()
        center_window(self.window)
        
        # Ana frame
        self.main_frame = ttk.Frame(self.window, padding=20)
        self.main_frame.pack(fill="both", expand=True)
        
        # Başlık
        self.title_label = ttk.Label(self.main_frame, text=title, font=("Arial", 16, "bold"))
        self.title_label.pack(pady=(0, 20))
        
        # Toolbar (filtreleme, dışa aktarma vb. işlemler için)
        self.toolbar_frame = ttk.Frame(self.main_frame)
        self.toolbar_frame.pack(fill="x", pady=(0, 10))
        
        # İçerik alanı
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill="both", expand=True)
        
        # Alt butonlar
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill="x", pady=(20, 0))
        
        # Kapat butonu
        ttk.Button(self.button_frame, text="Kapat", 
                  command=self.window.destroy).pack(side="right", padx=5)
