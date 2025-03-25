import tkinter as tk
from tkinter import ttk

# Ana renkler
PRIMARY_COLOR = "#2c3e50"  # Koyu mavi
SECONDARY_COLOR = "#3498db"  # Açık mavi
BG_COLOR = "#f5f5f5"  # Açık gri arka plan
TEXT_COLOR = "#333333"  # Koyu gri metin
SUCCESS_COLOR = "#2ecc71"  # Yeşil (başarı için)
WARNING_COLOR = "#f39c12"  # Turuncu (uyarı için)
ERROR_COLOR = "#e74c3c"  # Kırmızı (hata için)

def apply_styles():
    """Uygulama stillerini ayarlar"""
    style = ttk.Style()
    
    # Genel tema
    style.theme_use('clam')  # Clam teması kullanılacak
    
    # Arka plan rengi
    style.configure("TFrame", background=BG_COLOR)
    style.configure("TLabel", background=BG_COLOR, foreground=TEXT_COLOR)
    style.configure("TButton", background=PRIMARY_COLOR, foreground="white")
    
    # Treeview stilleri
    style.configure("Treeview", 
                   background="white", 
                   foreground=TEXT_COLOR, 
                   rowheight=25, 
                   fieldbackground="white")
    style.map("Treeview", 
             background=[('selected', SECONDARY_COLOR)],
             foreground=[('selected', 'white')])
    
    # Üst panel stili
    style.configure("TopPanel.TFrame", background=PRIMARY_COLOR)
    style.configure("TopPanel.TLabel", background=PRIMARY_COLOR, foreground="white")
    
    # Alt panel stili
    style.configure("Footer.TFrame", background=PRIMARY_COLOR)
    style.configure("Footer.TLabel", background=PRIMARY_COLOR, foreground="white")
    
    # Tab stilleri
    style.configure("TNotebook", background=BG_COLOR, borderwidth=0)
    style.configure("TNotebook.Tab", 
                  background=BG_COLOR, 
                  foreground=TEXT_COLOR,
                  padding=[10, 5])
    style.map("TNotebook.Tab", 
             background=[("selected", SECONDARY_COLOR)],
             foreground=[("selected", "white")])
    
    # Entry stil
    style.configure("TEntry", foreground=TEXT_COLOR, fieldbackground="white")
    
    # Combobox stil
    style.configure("TCombobox", 
                   foreground=TEXT_COLOR, 
                   background="white",
                   fieldbackground="white")
    
    # LabelFrame stil
    style.configure("TLabelframe", 
                   background=BG_COLOR, 
                   foreground=TEXT_COLOR)
    style.configure("TLabelframe.Label", 
                   background=BG_COLOR, 
                   foreground=PRIMARY_COLOR,
                   font=("Arial", 10, "bold"))
    
    # Buton stilleri
    style.configure("TButton", 
                   background=SECONDARY_COLOR, 
                   foreground="white",
                   borderwidth=1,
                   font=("Arial", 10),
                   padding=5)
    style.map("TButton",
             background=[("active", PRIMARY_COLOR)],
             foreground=[("active", "white")])
    
    # Başarı butonu
    style.configure("Success.TButton",
                  background=SUCCESS_COLOR,
                  foreground="white")
    style.map("Success.TButton",
             background=[("active", "#27ae60")],
             foreground=[("active", "white")])
    
    # Uyarı butonu
    style.configure("Warning.TButton",
                  background=WARNING_COLOR,
                  foreground="white")
    style.map("Warning.TButton",
             background=[("active", "#d35400")],
             foreground=[("active", "white")])
    
    # Hata/Tehlike butonu
    style.configure("Danger.TButton",
                  background=ERROR_COLOR,
                  foreground="white")
    style.map("Danger.TButton",
             background=[("active", "#c0392b")],
             foreground=[("active", "white")])
    
    # Scrollbar stili
    style.configure("TScrollbar", 
                   background=BG_COLOR, 
                   troughcolor="white", 
                   borderwidth=0, 
                   arrowsize=12)
    
    return style
