import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import re
from datetime import datetime
import locale

# Locale ayarı - Türkçe para birimi formatlaması için
try:
    locale.setlocale(locale.LC_ALL, 'tr_TR.UTF-8')
except locale.Error:
    try:
        # Fallback to English locale if Turkish is not available
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    except locale.Error:
        # If both fail, use the default locale
        locale.setlocale(locale.LC_ALL, '')

def center_window(window):
    """Pencereyi ekranın ortasına konumlandırır"""
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

def set_icon(window, icon_path=None):
    """Pencere ikonunu ayarlar"""
    if icon_path:
        try:
            window.iconbitmap(icon_path)
        except:
            pass  # İkon ayarlaması başarısız olursa sessizce devam et

def is_valid_phone(phone):
    """Telefon numarası doğrulama"""
    return phone.isdigit() and len(phone) <= 11

def is_valid_email(email):
    """E-posta adresi doğrulama"""
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None

def format_currency(amount):
    """Para birimini formatlar"""
    try:
        return f"{int(amount):,}".replace(",", ".")
    except:
        return "0"

def validate_numeric_input(P):
    """Entry widget için sayısal veri doğrulama"""
    if P == "":
        return True
    return P.isdigit()

def get_current_date():
    """Güncel tarihi döndürür (YYYY-MM-DD formatında)"""
    return datetime.now().strftime("%Y-%m-%d")

def get_month_name(month_number):
    """Verilen ay numarasına göre ay adını döndürür"""
    months = [
        "ocak", "subat", "mart", "nisan", "mayis", "haziran",
        "temmuz", "agustos", "eylul", "ekim", "kasim", "aralik"
    ]
    
    if 1 <= month_number <= 12:
        return months[month_number - 1]
    return ""

def create_scrollable_frame(parent, **kwargs):
    """Kaydırılabilir frame oluşturur"""
    # Ana container frame
    container = ttk.Frame(parent, **kwargs)
    
    # Canvas oluştur
    canvas = tk.Canvas(container)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    
    # Kaydırılabilir frame
    scrollable_frame = ttk.Frame(canvas)
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    # Canvas içine frame yerleştir
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Yerleştirme
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    return container, scrollable_frame

def setup_treeview(parent, columns, headings, column_widths=None):
    """Treeview widget'ı oluşturur ve yapılandırır"""
    # Scrollbar ile birlikte frame oluştur
    frame = ttk.Frame(parent)
    
    # Treeview oluştur
    tree = ttk.Treeview(frame, columns=columns, show="headings")
    
    # Scrollbar ekle
    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    
    # Başlıkları ayarla
    for i, col in enumerate(columns):
        tree.heading(col, text=headings[i])
        if column_widths and i < len(column_widths):
            tree.column(col, width=column_widths[i])
    
    # Yerleştirme
    vsb.pack(side='right', fill='y')
    hsb.pack(side='bottom', fill='x')
    tree.pack(side='left', fill='both', expand=True)
    
    return frame, tree

def create_combobox_with_label(parent, label_text, values=None, default=None, width=20):
    """Etiket ile birlikte combobox oluşturur"""
    frame = ttk.Frame(parent)
    
    # Etiket
    label = ttk.Label(frame, text=label_text)
    label.pack(side="left", padx=(0, 5))
    
    # Combobox
    combo = ttk.Combobox(frame, values=values, width=width)
    if default:
        combo.set(default)
    combo.pack(side="left", fill="x", expand=True)
    
    return frame, combo

def create_entry_with_label(parent, label_text, validate_cmd=None, width=20):
    """Etiket ile birlikte entry oluşturur"""
    frame = ttk.Frame(parent)
    
    # Etiket
    label = ttk.Label(frame, text=label_text)
    label.pack(side="left", padx=(0, 5))
    
    # Entry
    if validate_cmd:
        vcmd = (parent.register(validate_cmd), '%P')
        entry = ttk.Entry(frame, validate='key', validatecommand=vcmd, width=width)
    else:
        entry = ttk.Entry(frame, width=width)
    
    entry.pack(side="left", fill="x", expand=True)
    
    return frame, entry
