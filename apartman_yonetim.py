import tkinter as tk
from tkinter import ttk, messagebox, filedialog, Menu
import sqlite3
from datetime import date, datetime
import calendar
import os
import csv
import bcrypt
from utils import center_window, set_icon, is_valid_phone, is_valid_email, format_currency
from database import create_connection, init_database
from forms import (
    UyeForm, AidatForm, AidatOdemeForm, GiderForm, BankaHesapForm, 
    BankaHareketForm, ApartmanBilgileriForm, KullaniciForm
)
from reports import (
    AidatRaporu, GiderRaporu, BankaRaporuForm, GenelRaporForm,
    export_data_to_csv
)
from styles import apply_styles, PRIMARY_COLOR, SECONDARY_COLOR, BG_COLOR, TEXT_COLOR

# Global değişkenler
current_user = None
current_role = None

class ApartmanYonetimSistemi:
    def __init__(self, root):
        self.root = root
        self.root.title("Apartman Yönetim Sistemi")
        self.root.geometry("1024x768")
        self.root.configure(bg=BG_COLOR)
        
        # ESC tuşu ile tam ekrandan çıkış
        self.root.bind('<Escape>', self.toggle_fullscreen)
        
        # Tam ekran yapma
        self.root.attributes('-fullscreen', True)
        
        # Stil uygula
        apply_styles()
        
        # Veritabanını başlat
        init_database()
        
        # Login ekranını göster
        self.show_login_form()
    
    def toggle_fullscreen(self, event=None):
        """Tam ekran modunu değiştirir"""
        is_fullscreen = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not is_fullscreen)
        if is_fullscreen:
            self.root.geometry("1024x768")
            center_window(self.root)
    
    def show_login_form(self):
        """Giriş formunu gösterir"""
        # Mevcut widget'ları temizle
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Login formu oluştur
        login_frame = ttk.Frame(self.root, padding=20)
        login_frame.pack(expand=True, fill="both")
        
        # Pozisyonu ayarla
        login_frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=300)
        
        # Başlık
        title_label = ttk.Label(login_frame, text="Apartman Yönetim Sistemi", font=("Arial", 18, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Kullanıcı adı
        ttk.Label(login_frame, text="Kullanıcı Adı:").pack(anchor="w", pady=(10, 5))
        username_entry = ttk.Entry(login_frame, width=30)
        username_entry.pack(fill="x", pady=(0, 10))
        
        # Şifre
        ttk.Label(login_frame, text="Şifre:").pack(anchor="w", pady=(10, 5))
        password_entry = ttk.Entry(login_frame, show="*", width=30)
        password_entry.pack(fill="x", pady=(0, 10))
        
        # Giriş butonu
        login_button = ttk.Button(login_frame, text="Giriş", 
                                 command=lambda: self.login(username_entry.get(), password_entry.get()))
        login_button.pack(pady=20)
        
        # ENTER tuşuna basıldığında giriş yap
        password_entry.bind("<Return>", lambda event: self.login(username_entry.get(), password_entry.get()))
        
        # İlk alana odaklan
        username_entry.focus()
    
    def login(self, username, password):
        """Kullanıcı girişi için doğrulama"""
        global current_user, current_role
        
        if not username or not password:
            messagebox.showerror("Hata", "Kullanıcı adı ve şifre gereklidir!")
            return
        
        try:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT sifre, rol FROM kullanicilar WHERE kullanici_adi=?", (username,))
            user = cursor.fetchone()
            
            if user and bcrypt.checkpw(password.encode('utf-8'), user[0]):
                current_user = username
                current_role = user[1]
                self.create_main_menu()
            else:
                messagebox.showerror("Hata", "Geçersiz kullanıcı adı veya şifre!")
                
        except Exception as e:
            messagebox.showerror("Hata", f"Giriş hatası: {str(e)}")
        finally:
            if conn:
                conn.close()
    
    def logout(self):
        """Kullanıcı çıkışı yapar"""
        global current_user, current_role
        current_user = None
        current_role = None
        self.show_login_form()
    
    def create_main_menu(self):
        """Ana menüyü oluşturur"""
        global current_role
        
        # Mevcut widget'ları temizle
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Ana frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)
        
        # Üst panel
        top_panel = ttk.Frame(main_frame, style="TopPanel.TFrame")
        top_panel.pack(fill="x", side="top")
        
        # Başlık
        title_label = ttk.Label(top_panel, text="Apartman Yönetim Sistemi", 
                               font=("Arial", 16, "bold"), style="TopPanel.TLabel")
        title_label.pack(side="left", padx=10, pady=10)
        
        # Kullanıcı bilgisi
        user_label = ttk.Label(top_panel, 
                              text=f"Kullanıcı: {current_user} ({current_role})",
                              style="TopPanel.TLabel")
        user_label.pack(side="right", padx=10, pady=10)
        
        # Menü çubuğu oluştur
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        
        # Dosya menüsü
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Dosya", menu=file_menu)
        file_menu.add_command(label="Çıkış", command=self.logout)
        
        # Apartman menüsü
        apartman_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Apartman", menu=apartman_menu)
        apartman_menu.add_command(label="Apartman Bilgileri", 
                                 command=lambda: ApartmanBilgileriForm(self.root))
        
        # Üyeler menüsü
        uyeler_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Üyeler", menu=uyeler_menu)
        uyeler_menu.add_command(label="Üye Ekle/Düzenle", 
                               command=lambda: UyeForm(self.root))
        
        # Aidat menüsü
        aidat_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Aidatlar", menu=aidat_menu)
        aidat_menu.add_command(label="Aidat Belirle", 
                              command=lambda: AidatForm(self.root))
        aidat_menu.add_command(label="Aidat Ödeme Kaydet", 
                              command=lambda: AidatOdemeForm(self.root))
        aidat_menu.add_command(label="Aidat Raporu", 
                              command=lambda: AidatRaporu(self.root))
        
        # Giderler menüsü
        gider_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Giderler", menu=gider_menu)
        gider_menu.add_command(label="Gider Ekle", 
                              command=lambda: GiderForm(self.root))
        gider_menu.add_command(label="Gider Raporu", 
                              command=lambda: GiderRaporu(self.root))
        
        # Banka menüsü
        banka_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Banka", menu=banka_menu)
        banka_menu.add_command(label="Banka Hesapları", 
                              command=lambda: BankaHesapForm(self.root))
        banka_menu.add_command(label="Banka Hareketleri", 
                              command=lambda: BankaHareketForm(self.root))
        banka_menu.add_command(label="Banka Raporu", 
                              command=lambda: BankaRaporuForm(self.root))
        
        # Raporlar menüsü
        rapor_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Raporlar", menu=rapor_menu)
        rapor_menu.add_command(label="Genel Rapor", 
                              command=lambda: GenelRaporForm(self.root))
        rapor_menu.add_command(label="Veri Dışa Aktar", 
                              command=lambda: self.show_export_options())
        
        # Sadece yönetici için olan menüler
        if current_role == "yönetici":
            admin_menu = Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Yönetim", menu=admin_menu)
            admin_menu.add_command(label="Kullanıcı Yönetimi", 
                                  command=lambda: KullaniciForm(self.root))
        
        # Yardım menüsü
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Yardım", menu=help_menu)
        help_menu.add_command(label="Hakkında", command=self.show_about)
        
        # İçerik alanı
        content_frame = ttk.Frame(main_frame, padding=20)
        content_frame.pack(fill="both", expand=True)
        
        # Ana ekran widget'ları
        heading = ttk.Label(content_frame, text="Hoş Geldiniz", font=("Arial", 24, "bold"))
        heading.pack(pady=30)
        
        # Apartman bilgilerini göster
        self.show_apartment_summary(content_frame)
        
        # Alt panel
        footer = ttk.Frame(main_frame, style="Footer.TFrame")
        footer.pack(fill="x", side="bottom")
        
        # Telif hakkı metni
        copyright_label = ttk.Label(footer, 
                                   text="© 2023 Apartman Yönetim Sistemi", 
                                   style="Footer.TLabel")
        copyright_label.pack(pady=10)
    
    def show_apartment_summary(self, parent_frame):
        """Ana sayfada apartman özet bilgilerini gösterir"""
        try:
            conn = create_connection()
            cursor = conn.cursor()
            
            # Apartman bilgilerini al
            cursor.execute("SELECT adi, yonetici FROM apartman WHERE id=1")
            apartman_data = cursor.fetchone()
            
            # Üye sayısını al
            cursor.execute("SELECT COUNT(*) FROM uyeler")
            uye_sayisi = cursor.fetchone()[0]
            
            # Güncel ay aidat bilgilerini al
            current_year = datetime.now().year
            current_month = datetime.now().month
            ay_isimleri = ["ocak", "subat", "mart", "nisan", "mayis", "haziran", 
                          "temmuz", "agustos", "eylul", "ekim", "kasim", "aralik"]
            current_month_name = ay_isimleri[current_month - 1]
            
            cursor.execute(f"SELECT {current_month_name} FROM aidatlar WHERE yil=?", (current_year,))
            aidat_tutari_result = cursor.fetchone()
            aidat_tutari = aidat_tutari_result[0] if aidat_tutari_result else 0
            
            # Toplam borç
            cursor.execute("""
                SELECT SUM(a.tutar) 
                FROM aidat_odemeleri AS a
                WHERE a.yil = ? AND a.ay = ?
            """, (current_year, current_month_name))
            odenen_toplam = cursor.fetchone()[0] or 0
            toplam_borc = (aidat_tutari * uye_sayisi) - odenen_toplam
            
            # Özet frame
            summary_frame = ttk.LabelFrame(parent_frame, text="Apartman Özeti", padding=10)
            summary_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Bilgileri göster
            if apartman_data:
                ttk.Label(summary_frame, 
                         text=f"Apartman: {apartman_data[0]}", 
                         font=("Arial", 12)).pack(anchor="w", pady=5)
                ttk.Label(summary_frame, 
                         text=f"Yönetici: {apartman_data[1]}", 
                         font=("Arial", 12)).pack(anchor="w", pady=5)
            else:
                ttk.Label(summary_frame, 
                         text="Apartman bilgileri henüz girilmemiş.", 
                         font=("Arial", 12)).pack(anchor="w", pady=5)
            
            ttk.Label(summary_frame, 
                     text=f"Toplam Daire Sayısı: {uye_sayisi}", 
                     font=("Arial", 12)).pack(anchor="w", pady=5)
            ttk.Label(summary_frame, 
                     text=f"Güncel Aidat ({calendar.month_name[current_month]} {current_year}): {format_currency(aidat_tutari)} TL", 
                     font=("Arial", 12)).pack(anchor="w", pady=5)
            ttk.Label(summary_frame, 
                     text=f"Toplam Tahsil Edilecek: {format_currency(toplam_borc)} TL", 
                     font=("Arial", 12)).pack(anchor="w", pady=5)
            
            # Kısa yollar
            shortcuts_frame = ttk.Frame(parent_frame)
            shortcuts_frame.pack(fill="x", pady=20)
            
            ttk.Button(shortcuts_frame, 
                      text="Üye Ekle", 
                      command=lambda: UyeForm(self.root)).pack(side="left", padx=10)
            ttk.Button(shortcuts_frame, 
                      text="Aidat Ödeme Kaydet", 
                      command=lambda: AidatOdemeForm(self.root)).pack(side="left", padx=10)
            ttk.Button(shortcuts_frame, 
                      text="Gider Ekle", 
                      command=lambda: GiderForm(self.root)).pack(side="left", padx=10)
            ttk.Button(shortcuts_frame, 
                      text="Genel Rapor", 
                      command=lambda: GenelRaporForm(self.root)).pack(side="left", padx=10)
                
        except Exception as e:
            messagebox.showerror("Hata", f"Özet bilgileri yüklenirken hata: {str(e)}")
        finally:
            if conn:
                conn.close()
    
    def show_export_options(self):
        """Veri dışa aktarma seçeneklerini gösterir"""
        export_window = tk.Toplevel(self.root)
        export_window.title("Veri Dışa Aktar")
        export_window.geometry("400x300")
        center_window(export_window)
        
        ttk.Label(export_window, 
                 text="Dışa Aktarılacak Veriyi Seçin", 
                 font=("Arial", 14, "bold")).pack(pady=20)
        
        ttk.Button(export_window, 
                  text="Üye Listesi", 
                  command=lambda: export_data_to_csv(export_window, "uyeler")).pack(fill="x", padx=50, pady=5)
        ttk.Button(export_window, 
                  text="Aidat Ödemeleri", 
                  command=lambda: export_data_to_csv(export_window, "aidat_odemeleri")).pack(fill="x", padx=50, pady=5)
        ttk.Button(export_window, 
                  text="Giderler", 
                  command=lambda: export_data_to_csv(export_window, "giderler")).pack(fill="x", padx=50, pady=5)
        ttk.Button(export_window, 
                  text="Banka Hareketleri", 
                  command=lambda: export_data_to_csv(export_window, "banka_hareketleri")).pack(fill="x", padx=50, pady=5)
        
        ttk.Button(export_window, 
                  text="Kapat", 
                  command=export_window.destroy).pack(pady=20)
    
    def show_about(self):
        """Hakkında penceresini gösterir"""
        about_window = tk.Toplevel(self.root)
        about_window.title("Hakkında")
        about_window.geometry("400x300")
        center_window(about_window)
        
        ttk.Label(about_window, 
                 text="Apartman Yönetim Sistemi", 
                 font=("Arial", 16, "bold")).pack(pady=20)
        ttk.Label(about_window, 
                 text="Sürüm 1.0").pack()
        ttk.Label(about_window, 
                 text="© 2023 Tüm Hakları Saklıdır").pack(pady=10)
        ttk.Label(about_window, 
                 text="Bu uygulama apartman yönetiminde aidat takibi,\ngider yönetimi ve banka işlemleri için tasarlanmıştır.",
                 justify="center").pack(pady=20)
        
        ttk.Button(about_window, 
                  text="Kapat", 
                  command=about_window.destroy).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = ApartmanYonetimSistemi(root)
    root.mainloop()
