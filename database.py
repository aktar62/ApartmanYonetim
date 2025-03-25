import sqlite3
import os
from datetime import datetime
import bcrypt

def create_connection():
    """SQLite veritabanı bağlantısı oluşturur"""
    conn = sqlite3.connect("apartman.db")
    conn.row_factory = sqlite3.Row  # Sonuçları sözlük olarak almak için
    return conn

def init_database():
    """Veritabanını ve tabloları oluşturur, varsayılan veriyi ekler"""
    create_tables()
    create_user_table()
    create_default_admin()

def create_tables():
    """Gerekli veritabanı tablolarını oluşturur"""
    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()

        # Apartman tablosu
        cursor.execute('''CREATE TABLE IF NOT EXISTS apartman (
                        id INTEGER PRIMARY KEY CHECK (id=1),
                        adi TEXT, 
                        yonetici TEXT,
                        Tel TEXT,
                        yardimci TEXT,
                        denetci TEXT,
                        adres TEXT)''')

        # Üyeler tablosu
        cursor.execute('''CREATE TABLE IF NOT EXISTS uyeler (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        daire_no INTEGER,
                        adi_soyadi TEXT,
                        telefon TEXT,
                        kat_maliki_durumu TEXT,
                        apartman TEXT,
                        email TEXT,
                        UNIQUE(daire_no))''')

        # Aidatlar tablosu
        cursor.execute('''CREATE TABLE IF NOT EXISTS aidatlar (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        yil INTEGER,
                        ocak INTEGER DEFAULT 0,
                        subat INTEGER DEFAULT 0,
                        mart INTEGER DEFAULT 0,
                        nisan INTEGER DEFAULT 0,
                        mayis INTEGER DEFAULT 0,
                        haziran INTEGER DEFAULT 0,
                        temmuz INTEGER DEFAULT 0,
                        agustos INTEGER DEFAULT 0,
                        eylul INTEGER DEFAULT 0,
                        ekim INTEGER DEFAULT 0,
                        kasim INTEGER DEFAULT 0,
                        aralik INTEGER DEFAULT 0,
                        toplam INTEGER DEFAULT 0,
                        UNIQUE(yil))''')

        # Aidat ödemeleri tablosu
        cursor.execute('''CREATE TABLE IF NOT EXISTS aidat_odemeleri (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        uye_id INTEGER,
                        yil INTEGER,
                        ay TEXT,
                        odeme_tarihi TEXT,
                        tutar INTEGER,
                        aciklama TEXT,
                        FOREIGN KEY (uye_id) REFERENCES uyeler(id))''')
                        
        # Giderler tablosu
        cursor.execute('''CREATE TABLE IF NOT EXISTS giderler (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        odeme_tarihi TEXT,
                        tutar INTEGER,
                        aciklama TEXT,
                        odeme_sekli TEXT CHECK(odeme_sekli IN ('Banka', 'Nakit')),
                        banka_hesap_id INTEGER,
                        FOREIGN KEY (banka_hesap_id) REFERENCES banka_hesaplari(id))''')

        # Banka hesapları tablosu
        cursor.execute('''CREATE TABLE IF NOT EXISTS banka_hesaplari (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        banka_adi TEXT,
                        sube_adi TEXT,
                        hesap_no TEXT,
                        iban TEXT,
                        aciklama TEXT)''')

        # Banka hareketleri tablosu
        cursor.execute('''CREATE TABLE IF NOT EXISTS banka_hareketleri (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        hesap_id INTEGER,
                        tarih TEXT,
                        tutar INTEGER,
                        hareket_tipi TEXT CHECK(hareket_tipi IN ('Gelir', 'Gider')),
                        aciklama TEXT,
                        FOREIGN KEY (hesap_id) REFERENCES banka_hesaplari(id))''')

        conn.commit()
    except Exception as e:
        print(f"Veritabanı tabloları oluşturma hatası: {str(e)}")
    finally:
        if conn:
            conn.close()

def create_user_table():
    """Kullanıcılar tablosunu oluşturur"""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS kullanicilar (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    kullanici_adi TEXT UNIQUE,
                    sifre TEXT,
                    rol TEXT CHECK(rol IN ('yönetici', 'sakin')),
                    uye_id INTEGER,
                    FOREIGN KEY (uye_id) REFERENCES uyeler(id)
                )''')
    conn.commit()
    conn.close()

def create_default_admin():
    """Varsayılan yönetici hesabını oluşturur"""
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM kullanicilar WHERE rol='yönetici'")
        admin = cursor.fetchone()

        if not admin:
            # Varsayılan yönetici hesabı
            hashed_password = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt())
            cursor.execute(
                "INSERT INTO kullanicilar (kullanici_adi, sifre, rol) VALUES (?, ?, ?)",
                ("admin", hashed_password, "yönetici")
            )
            conn.commit()
            print("Varsayılan yönetici hesabı oluşturuldu!")
    except Exception as e:
        print(f"Yönetici hesabı oluşturma hatası: {str(e)}")
    finally:
        if conn:
            conn.close()

def get_table_data(table_name, conditions=None):
    """Belirtilen tablodan veri alır"""
    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()
        
        if conditions:
            query = f"SELECT * FROM {table_name} WHERE {conditions}"
        else:
            query = f"SELECT * FROM {table_name}"
            
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print(f"Veri alma hatası: {str(e)}")
        return []
    finally:
        if conn:
            conn.close()

def get_all_uyeler():
    """Tüm üyeleri alır"""
    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM uyeler ORDER BY daire_no")
        return cursor.fetchall()
    except Exception as e:
        print(f"Üye verileri alma hatası: {str(e)}")
        return []
    finally:
        if conn:
            conn.close()

def get_all_banka_hesaplari():
    """Tüm banka hesaplarını alır"""
    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM banka_hesaplari")
        return cursor.fetchall()
    except Exception as e:
        print(f"Banka hesapları alma hatası: {str(e)}")
        return []
    finally:
        if conn:
            conn.close()

def get_aidat_for_year(year):
    """Belirli yıl için aidat tutarlarını alır"""
    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM aidatlar WHERE yil=?", (year,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Aidat verileri alma hatası: {str(e)}")
        return None
    finally:
        if conn:
            conn.close()

def get_aidat_odemeler_by_uye(uye_id, year=None):
    """Bir üyenin aidat ödemelerini alır"""
    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()
        
        if year:
            cursor.execute(
                "SELECT * FROM aidat_odemeleri WHERE uye_id=? AND yil=? ORDER BY odeme_tarihi DESC", 
                (uye_id, year)
            )
        else:
            cursor.execute(
                "SELECT * FROM aidat_odemeleri WHERE uye_id=? ORDER BY odeme_tarihi DESC", 
                (uye_id,)
            )
            
        return cursor.fetchall()
    except Exception as e:
        print(f"Aidat ödemeleri alma hatası: {str(e)}")
        return []
    finally:
        if conn:
            conn.close()

def get_banka_hareketleri(hesap_id=None, start_date=None, end_date=None):
    """Banka hareketlerini alır, isteğe bağlı filtrelerle"""
    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM banka_hareketleri"
        params = []
        
        conditions = []
        if hesap_id:
            conditions.append("hesap_id=?")
            params.append(hesap_id)
        
        if start_date:
            conditions.append("tarih>=?")
            params.append(start_date)
        
        if end_date:
            conditions.append("tarih<=?")
            params.append(end_date)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY tarih DESC"
        
        cursor.execute(query, params)
        return cursor.fetchall()
    except Exception as e:
        print(f"Banka hareketleri alma hatası: {str(e)}")
        return []
    finally:
        if conn:
            conn.close()

def get_giderler(start_date=None, end_date=None):
    """Giderleri alır, isteğe bağlı tarih filtresi ile"""
    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()
        
        query = "SELECT g.*, b.banka_adi FROM giderler g LEFT JOIN banka_hesaplari b ON g.banka_hesap_id = b.id"
        params = []
        
        conditions = []
        if start_date:
            conditions.append("g.odeme_tarihi>=?")
            params.append(start_date)
        
        if end_date:
            conditions.append("g.odeme_tarihi<=?")
            params.append(end_date)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY g.odeme_tarihi DESC"
        
        cursor.execute(query, params)
        return cursor.fetchall()
    except Exception as e:
        print(f"Gider verileri alma hatası: {str(e)}")
        return []
    finally:
        if conn:
            conn.close()

def get_apartman_bilgileri():
    """Apartman bilgilerini alır"""
    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM apartman WHERE id=1")
        return cursor.fetchone()
    except Exception as e:
        print(f"Apartman bilgileri alma hatası: {str(e)}")
        return None
    finally:
        if conn:
            conn.close()
