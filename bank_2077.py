import os
import pickle as p
import random as r
import tkinter as tk
from tkinter import messagebox, simpledialog

Banka_pencere = "#FFFF33"
yazı_rengi = "#1A1A24"

SİBER_BUTON = {
    "bg": "#00F0FF",
    "fg": "#FFFF33",
    "activeforeground": "#6A1B99",
    "activebackground": "#BF00FF",
    "font": ("Lucida Console", 12, "italic"),
    "bd": 1,
    "relief": "sunken",
    "highlightbackground": "#00f0ff",
    "highlightcolor": "#00F0FF",
    "highlightthickness": 3,
}


def tüm_hesapları_al():
    if os.path.isfile("hesap.listesi"):
        with open("hesap.listesi", "rb") as dosya_bulma:
            return p.load(dosya_bulma)
    return {}


def hesap_yazma(hesaplar):
    with open("hesap.listesi", "wb") as dosya_yazma:
        p.dump(hesaplar, dosya_yazma)


def para_yatırma(act_no):
    Hesaplar = tüm_hesapları_al()
    miktar = simpledialog.askinteger(
        "Para Yatırma", "Yatırılacak miktarı giriniz:", minvalue=50
    )

    if miktar:
        kdv_parası = (miktar / 100) * 10
        tam_para = miktar - kdv_parası

        mevcut_bakiye = float(Hesaplar[act_no][5])
        Hesaplar[act_no][5] = int(mevcut_bakiye + tam_para)

        hesap_yazma(Hesaplar)
        messagebox.showinfo(
            "Başarılı",
            f"{miktar} TL yatırıldı.\nYeni Bakiye: {Hesaplar[act_no][5]} TL",
        )


def para_çekme(act_no):
    Hesaplar = tüm_hesapları_al()
    miktar = simpledialog.askinteger(
        "Para Çekme", "Çekilecek miktarı giriniz:", minvalue=100
    )

    if miktar:
        kdv_parası = (miktar / 100) * 10
        toplam_kesinti = miktar + kdv_parası

        mevcut_bakiye = float(Hesaplar[act_no][5])

        if mevcut_bakiye >= toplam_kesinti:
            Hesaplar[act_no][5] = int(mevcut_bakiye - toplam_kesinti)
            hesap_yazma(Hesaplar)
            messagebox.showinfo(
                "Başarılı",
                f"{miktar} TL çekildi.\nKalan Bakiye: {Hesaplar[act_no][5]} TL",
            )
        else:
            messagebox.showerror(
                "Hata", f"Yetersiz bakiye!\nHesabınızda {mevcut_bakiye} TL var."
            )


def bakiye_kontrol(act_no):
    Hesaplar = tüm_hesapları_al()
    mevcut_bakiye = Hesaplar[act_no][5]
    messagebox.showinfo(
        "Bakiye Bilgisi", f"Güncel Bakiyeniz: {mevcut_bakiye} TL"
    )


def hesapları_görüntüle():
    Hesaplar = tüm_hesapları_al()
    liste_metni = ""
    for no in Hesaplar:
        h = Hesaplar[no]
        liste_metni += f"No: {no} | İsim: {h[0]} | Tel: {h[1]} | Cinsiyet: {h[3]} | Şifre: {h[4]} | Bakiye: {h[5]} TL\n"
    if not liste_metni:
        liste_metni = "Sisteme kayıtlı hesap yok"
    messagebox.showinfo("Tüm Hesaplar", liste_metni)


def hesap_ekle():
    hesaplar = tüm_hesapları_al()
    ac_no = simpledialog.askstring(
        "Hesap Ekle", "Yeni hesap numarası giriniz:"
    )
    if not ac_no:
        return
    if ac_no in hesaplar.keys():
        messagebox.showwarning("Uyarı", "Bu hesap numarası zaten alınmıştır!")
        return
    isim = simpledialog.askstring("Hesap Bilgisi", "Hesap sahibinin ismi:")
    telefon = simpledialog.askstring("Hesap Bilgisi", "Telefon numarası:")
    adres = simpledialog.askstring("Hesap Bilgisi", "Adres:")
    cinsiyet = simpledialog.askstring("Hesap Bilgisi", "Cinsiyet:")
    şifre = r.randint(1000, 999999)
    bakiye = 0
    hesaplar[ac_no] = [isim, telefon, adres, cinsiyet, şifre, bakiye]
    hesap_yazma(hesaplar)
    messagebox.showinfo(
        "Başarılı", f"Hesap kuruldu!\nÜretilen Şifre: {şifre}"
    )


def hesap_sil():
    Hesaplar = tüm_hesapları_al()
    ac_no = simpledialog.askstring(
        "Hesap Silme", "Silinecek hesap numarasını giriniz:"
    )
    if ac_no:
        if ac_no in Hesaplar.keys():
            del Hesaplar[ac_no]
            hesap_yazma(Hesaplar)
            messagebox.showinfo("Başarılı", "Hesap başarıyla silindi.")
        else:
            messagebox.showerror("Hata", "Hesap bulunamadı!")


def hesap_arat():
    Hesaplar = tüm_hesapları_al()
    ac_no = simpledialog.askstring(
        "Hesap Arama", "Aranacak hesap numarasını giriniz:"
    )
    if ac_no:
        if ac_no in Hesaplar.keys():
            h = Hesaplar[ac_no]
            detay = (
                f"İsim: {h[0]}\nTel: {h[1]}\nAdres: {h[2]}\nBakiye: {h[5]} TL"
            )
            messagebox.showinfo("Hesap Bulundu", detay)
        else:
            messagebox.showerror("Hata", "Hesap bulunamadı!")


def admin_paneli():
    admin = tk.Toplevel(pencere)
    admin.title("Admin Paneli")
    admin.geometry("400x380")
    admin.configure(bg=Banka_pencere)
    tk.Label(
        admin,
        text=":: ADMIN TERMINAL ::",
        bg=Banka_pencere,
        fg=yazı_rengi,
        font=("Courier", 12, "bold"),
    ).pack(pady=10)
    tk.Button(
        admin, text="1. Hesap Gör", command=hesap_arat, **SİBER_BUTON
    ).pack(pady=5, fill="x", padx=40)
    tk.Button(
        admin, text="2. Hesap Sil", command=hesap_sil, **SİBER_BUTON
    ).pack(pady=5, fill="x", padx=40)
    tk.Button(
        admin, text="3. Hesap Ekle", command=hesap_ekle, **SİBER_BUTON
    ).pack(pady=5, fill="x", padx=40)
    tk.Button(
        admin,
        text="Tüm Hesapları Gör",
        command=hesapları_görüntüle,
        **SİBER_BUTON,
    ).pack(pady=5, fill="x", padx=40)
    tk.Button(
        admin,
        text="[ DISCONNECT ]",
        command=admin.destroy,
        bg=Banka_pencere,
        fg="#FF0000",
        font=("Courier", 9, "bold"),
        bd=0,
    ).pack(pady=10)


def kullanıcı_paneli(act_no):
    kullanıcı = tk.Toplevel(pencere)
    kullanıcı.title("Kullanıcı Paneli")
    kullanıcı.geometry("400x350")
    kullanıcı.configure(bg=Banka_pencere)
    tk.Label(
        kullanıcı,
        text=" KULLANICI ERİŞİMİ ",
        bg=Banka_pencere,
        fg=yazı_rengi,
        font=("Courier", 12, "bold"),
    ).pack(pady=10)
    tk.Button(
        kullanıcı,
        text="1. Para Yatır",
        command=lambda: para_yatırma(act_no),
        **SİBER_BUTON,
    ).pack(pady=5, fill="x", padx=40)
    tk.Button(
        kullanıcı,
        text="2. Para Çek",
        command=lambda: para_çekme(act_no),
        **SİBER_BUTON,
    ).pack(pady=5, fill="x", padx=40)
    tk.Button(
        kullanıcı,
        text="3. Bakiye Gör",
        command=lambda: bakiye_kontrol(act_no),
        **SİBER_BUTON,
    ).pack(pady=5, fill="x", padx=40)
    tk.Button(
        kullanıcı,
        text="[ DISCONNECT ]",
        command=kullanıcı.destroy,
        bg=Banka_pencere,
        fg="#FF0000",
        font=("Courier", 9, "bold"),
        bd=0,
    ).pack(pady=10)


def kullanıcı_kontrolü():
    Hesaplar = tüm_hesapları_al()
    act_no = simpledialog.askstring(
        "Kullanıcı Girişi", "Hesap numaranızı giriniz:"
    )
    if act_no:
        if act_no in Hesaplar.keys():
            şifre = simpledialog.askinteger(
                "Kullanıcı Girişi", "Şifrenizi giriniz:"
            )
            if şifre is not None:
                if Hesaplar[act_no][4] == şifre:
                    kullanıcı_paneli(act_no)
                else:
                    messagebox.showerror("Hata", "Şifre yanlış!")
        else:
            messagebox.showerror("Hata", "Geçersiz hesap numarası!")


def admin_kontrolü():
    input_id = simpledialog.askstring("Admin Girişi", "Admin ID giriniz:")
    input_sifre = simpledialog.askstring(
        "Admin Girişi", "Admin Şifre giriniz:"
    )
    if input_id == "ArdaAsan" and input_sifre == "5551515A.":
        admin_paneli()
    else:
        messagebox.showerror("Hata", "ID veya şifre yanlış!")


pencere = tk.Tk()
pencere.title("2077 Bankası")
pencere.geometry("400x250")
pencere.configure(bg=Banka_pencere)

tk.Label(
    pencere,
    text="=== 2077 Bankası ===",
    bg=Banka_pencere,
    fg=yazı_rengi,
    font=("Courier", 14, "bold"),
).pack(pady=20)

btn1 = tk.Button(
    pencere, text="SECURE: Admin Girişi", command=admin_kontrolü, **SİBER_BUTON
)
btn1.pack(pady=10, fill="x", padx=50)

btn2 = tk.Button(
    pencere,
    text="SECURE: Kullanıcı Girişi",
    command=kullanıcı_kontrolü,
    **SİBER_BUTON,
)
btn2.pack(pady=10, fill="x", padx=50)

pencere.mainloop()
