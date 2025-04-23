
# Autow (Auto Writer) App

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import pyautogui
import requests
import sys
import os
from PIL import Image, ImageDraw, ImageTk
import sv_ttk  # Sun Valley tema kütüphanesi

def load_version():
    try:
        with open("VERSION.json", "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception:
        return "0.0.0"

CURRENT_VERSION = load_version()
GITHUB_VERSION_URL = "https://raw.githubusercontent.com/ATOMGAMERAGA/autow/main/VERSION.json"
GITHUB_MAIN_URL = "https://raw.githubusercontent.com/ATOMGAMERAGA/autow/main/main.py"
GITHUB_LOGO_URL = "https://raw.githubusercontent.com/ATOMGAMERAGA/autow/main/logos/logo.png"
typing_thread = None
typing_flag = False
assigned_key = None

def convert_key(keysym):
    mapping = {
        "Return": "enter",
        "space": "space",
        "Tab": "tab",
        "BackSpace": "backspace",
        "Escape": "esc",
    }
    if keysym in mapping:
        return mapping[keysym]
    elif len(keysym) == 1:
        return keysym
    else:
        return keysym

def auto_typing(text, interval):
    global typing_flag, assigned_key
    time.sleep(1)  # Hedef uygulamaya odaklanmak için bekleme
    while typing_flag:
        pyautogui.write(text, interval=0.05)
        if assigned_key is not None:
            converted_key = convert_key(assigned_key)
            try:
                pyautogui.press(converted_key)
            except Exception as e:
                print(f"Tuş gönderilemedi: {e}")
        time.sleep(interval)

def update_status_label():
    status = "Aktif" if typing_flag else "Deaktif"
    label_status.config(text=f"Durum: {status}")

def start_typing():
    global typing_flag, typing_thread
    text = entry_text.get()
    try:
        interval = float(entry_interval.get())
    except ValueError:
        messagebox.showerror("Hata", "Lütfen geçerli bir sayı giriniz!")
        return
    if text == "":
        messagebox.showerror("Hata", "Lütfen yazılacak metni giriniz!")
        return
    if typing_flag:
        messagebox.showinfo("Bilgi", "Auto Writer zaten çalışıyor!")
        return
    typing_flag = True
    update_status_label()
    typing_thread = threading.Thread(target=auto_typing, args=(text, interval))
    typing_thread.daemon = True
    typing_thread.start()

def stop_typing():
    global typing_flag, typing_thread
    typing_flag = False
    if typing_thread:
        typing_thread.join(timeout=1)
    update_status_label()
    messagebox.showinfo("Bilgi", "Autow durduruldu.")

def create_image():
    try:
        image = Image.open("logos/logo.png")
        image = image.resize((64, 64))
    except Exception:
        image = Image.new('RGB', (64, 64), "white")
        dc = ImageDraw.Draw(image)
        dc.rectangle((0, 0, 64, 64), fill="blue")
    return image

def on_closing():
    global typing_flag, typing_thread
    typing_flag = False
    if typing_thread:
        typing_thread.join(timeout=1)
    root.destroy()

def capture_key():
    capture_win = tk.Toplevel(root)
    capture_win.title("Tuş Ataması")
    capture_win.geometry("300x100")
    label = ttk.Label(capture_win, text="Lütfen bir tuşa basın...", font=("Helvetica", 12))
    label.pack(expand=True, pady=20)
    def key_pressed(event):
        global assigned_key
        assigned_key = event.keysym
        label_assigned.config(text=f"Atanmış Tuş: {assigned_key}")
        capture_win.destroy()
    capture_win.bind("<Key>", key_pressed)
    capture_win.focus_force()

def reset_key():
    global assigned_key
    assigned_key = None
    label_assigned.config(text="Atanmış Tuş: Yok!")

def check_for_update():
    try:
        response = requests.get(GITHUB_VERSION_URL, timeout=5)
        if response.status_code != 200:
            messagebox.showerror("Güncelleme Hatası", f"Güncelleme kontrolü yapılamadı: HTTP {response.status_code}. Destek için githuba bildirebilirsiniz.")
            return
        remote_version = response.text.strip()
    except Exception as e:
        messagebox.showerror("Güncelleme Hatası", f"Güncelleme kontrolü yapılamadı: {e}")
        return

    try:
        current_version_tuple = tuple(map(int, CURRENT_VERSION.split(".")))
        remote_version_tuple = tuple(map(int, remote_version.split(".")))
    except Exception as e:
        messagebox.showerror("Güncelleme Hatası", f"Sürüm bilgisi okunamadı: {e}")
        return

    if remote_version_tuple > current_version_tuple:
        if messagebox.askyesno("Güncelleme Var", f"Yeni sürüm mevcut: {remote_version}\nGüncellemek ister misiniz?"):
            try:
                main_response = requests.get(GITHUB_MAIN_URL, timeout=10)
                if main_response.status_code != 200:
                    messagebox.showerror("Güncelleme Hatası", f"Yeni sürüm indirilemedi: HTTP {main_response.status_code}")
                    return
                with open(sys.argv[0], "w", encoding="utf-8") as f:
                    f.write(main_response.text)
                with open("VERSION.json", "w", encoding="utf-8") as f:
                    f.write(remote_version)
                messagebox.showinfo("Güncelleme", "Güncelleme tamamlandı.\nLütfen uygulamayı yeniden başlatın.")
                os._exit(0)
            except Exception as e:
                messagebox.showerror("Güncelleme Hatası", f"Güncelleme yapılamadı: {e}")
    else:
        messagebox.showinfo("Güncelleme", "Uygulamanız güncel.")

def update_app():
    threading.Thread(target=check_for_update, daemon=True).start()

def show_info():
    info_text = (
        "Uygulama: Autow (Auto Writer)\n"
        "Geliştirici: Atom Gamer Arda A.G.A\n"
        f"Sürüm: {CURRENT_VERSION}\n"
        "Bu uygulama otomatik yazma işlemi için geliştirilmiştir."
    )
    messagebox.showinfo("Uygulama Bilgisi", info_text)

def toggle_theme():
    sv_ttk.toggle_theme()

# Ana pencere oluşturma
root = tk.Tk()
root.title(f"Autow (Auto Writer) {CURRENT_VERSION}")
root.geometry("500x700")

# Sun Valley teması koyu modda başlat
sv_ttk.set_theme("dark")

if sys.platform == "darwin":
    messagebox.showwarning("Uyarı", "Bu uygulama macOS'ta düzgün çalışmayabilir.")

# Logo yükleme
try:
    logo_image = Image.open("logos/logo.png")
    logo_image = logo_image.resize((200, 200))
    logo_photo = ImageTk.PhotoImage(logo_image)
    label_logo = ttk.Label(root, image=logo_photo)
    label_logo.pack(padx=10, pady=10)
except Exception as e:
    print("Logo yüklenemedi:", e)

# Metin girişi
label_text = ttk.Label(root, text="Yazılacak metni giriniz:")
label_text.pack(padx=10, pady=5)

entry_text = ttk.Entry(root, width=50)
entry_text.pack(padx=10, pady=5)

# Yazma aralığı
label_interval = ttk.Label(root, text="Kaç saniyede bir (saniye):")
label_interval.pack(padx=10, pady=5)

entry_interval = ttk.Entry(root, width=20)
entry_interval.pack(padx=10, pady=5)
entry_interval.insert(0, "5")  # Varsayılan 5 saniye

# Durum etiketi
label_status = ttk.Label(root, text="Durum: Deaktif", font=("Helvetica", 12, "bold"))
label_status.pack(padx=10, pady=5)

# Tuş atama çerçevesi
frame_key = ttk.Frame(root)
frame_key.pack(padx=10, pady=10)

label_assigned = ttk.Label(frame_key, text="Atanmış Tuş: Yok")
label_assigned.grid(row=0, column=0, columnspan=2, pady=(0, 5))

button_set_key = ttk.Button(frame_key, text="Tuş Ata", command=capture_key)
button_set_key.grid(row=1, column=0, padx=5, pady=5)

button_reset_key = ttk.Button(frame_key, text="Tuşu Sıfırla", command=reset_key)
button_reset_key.grid(row=1, column=1, padx=5, pady=5)

# Başlat ve Durdur butonları
button_start = ttk.Button(root, text="Başlat", command=start_typing)
button_start.pack(padx=10, pady=5, fill='x')

button_stop = ttk.Button(root, text="Durdur", command=stop_typing)
button_stop.pack(padx=10, pady=5, fill='x')

# Tema değiştirme butonu
button_theme = ttk.Button(root, text="Tema Değiştir", command=toggle_theme)
button_theme.pack(padx=10, pady=5, fill='x')

# Güncelleme ve bilgi butonları çerçevesi
frame_bottom = ttk.Frame(root)
frame_bottom.pack(padx=10, pady=10, fill='x')

button_update = ttk.Button(frame_bottom, text="Güncelle", command=update_app)
button_update.pack(side='left', expand=True, fill='x', padx=5)

button_info = ttk.Button(frame_bottom, text="Bilgi", command=show_info)
button_info.pack(side='left', expand=True, fill='x', padx=5)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
