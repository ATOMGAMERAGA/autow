import tkinter as tk
from tkinter import messagebox
import threading
from pynput.keyboard import Controller, Key
from pynput.mouse import Listener as MouseListener
import pystray
from PIL import Image, ImageDraw, ImageTk
import requests
import sys
import os

# Sürüm bilgisi yükleme fonksiyonu
def load_version():
    try:
        with open("VERSION.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception:
        return "0.0.0"

CURRENT_VERSION = load_version()
GITHUB_VERSION_URL = "https://raw.githubusercontent.com/ATOMGAMERAGA/autow/main/VERSION.txt"
GITHUB_MAIN_URL = "https://raw.githubusercontent.com/ATOMGAMERAGA/autow/main/main.py"

# Global değişkenler
text_to_type = ""
keyboard = Controller()
mouse_listener = None

def on_mouse_click(x, y, button, pressed):
    """
    Sol tıklama gerçekleştiğinde, eğer kullanıcı tarafından metin girilmişse
    bu metni o an odaklı uygulamaya yazar.
    """
    # Sadece tıklama basıldığında çalışır.
    if pressed and button.name == 'left' and text_to_type:
        for char in text_to_type:
            keyboard.press(char)
            keyboard.release(char)
        # İsteğe bağlı: Yazım sonrası Enter tuşuna basar.
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)

def start_auto_typing():
    """
    Kullanıcı tarafından girilen metni alır, geçerli bir sayı kontrol eder ve
    mouse listener'ı başlatır. Ayrıca, uygulama penceresini gizleyerek
    metnin hedef uygulamaya gönderilmesini sağlar.
    """
    global text_to_type, mouse_listener
    text = entry_text.get()
    if text == "":
        messagebox.showerror("Hata", "Lütfen yazılacak metni giriniz!")
        return

    try:
        # Aralık değeri; örneğin iki tıklama arasında bekleme süresi olarak kullanılabilir
        interval = float(entry_interval.get())
    except ValueError:
        messagebox.showerror("Hata", "Lütfen geçerli bir sayı giriniz!")
        return

    text_to_type = text

    # Ekran erişim izni gerekliyse, burada kullanıcıya bilgi verilebilir.
    # Örneğin: "Lütfen bu uygulamaya ekran erişimi izni verin (Sistem Ayarlarından)"
    messagebox.showinfo("Erişim İzni", "Uygulamanın çalışabilmesi için sisteminizde 'Erişim İzni' verilmiş olmalıdır.")

    # Uygulama penceresini gizleyerek dışarıdaki uygulamalara yazım yapılmasını sağlıyoruz.
    root.withdraw()

    # Mouse listener'ı başlatıyoruz
    mouse_listener = MouseListener(on_click=on_mouse_click)
    mouse_listener.start()

def stop_auto_typing():
    """
    Mouse listener'ı durdurur ve uygulama penceresini tekrar gösterir.
    """
    global mouse_listener
    if mouse_listener:
        mouse_listener.stop()
        mouse_listener = None
    messagebox.showinfo("Bilgi", "Auto Writer durduruldu.")
    root.deiconify()

def exit_app():
    """
    Uygulamayı tamamen sonlandırır.
    """
    global mouse_listener
    if mouse_listener:
        mouse_listener.stop()
        mouse_listener = None
    root.destroy()

def create_image():
    """
    Tray simgesi için basit bir ikon oluşturur.
    """
    try:
        image = Image.open("logo.png")
        image = image.resize((64, 64))
    except Exception:
        image = Image.new('RGB', (64, 64), "white")
        dc = ImageDraw.Draw(image)
        dc.rectangle((0, 0, 64, 64), fill="blue")
    return image

def show_window(icon, item):
    root.deiconify()

def quit_from_tray(icon, item):
    exit_app()

def setup_tray():
    """
    Sistem tepsisi (tray) menüsü oluşturur.
    """
    image = create_image()
    menu = pystray.Menu(
        pystray.MenuItem('Göster', show_window),
        pystray.MenuItem('Çık', quit_from_tray)
    )
    tray_icon = pystray.Icon("AutoTyper", image, "AutoTyper", menu)
    tray_icon.run()

def check_for_update():
    try:
        response = requests.get(GITHUB_VERSION_URL, timeout=5)
        if response.status_code != 200:
            messagebox.showerror("Güncelleme Hatası", f"Güncelleme kontrolü yapılamadı: HTTP {response.status_code}")
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
                with open("VERSION.txt", "w", encoding="utf-8") as f:
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
        "Uygulama: Auto Writer\n"
        "Geliştirici: Atom Gamer Arda A.G.A\n"
        f"Sürüm: {CURRENT_VERSION}\n"
        "Bu uygulama, aktif olan uygulamaya otomatik olarak metin yazmak üzere tasarlanmıştır.\n\n"
        "ÖNEMLİ: Uygulamanın çalışabilmesi için ekran erişim izninin (Accessibility) verilmiş olması gerekmektedir."
    )
    messagebox.showinfo("Uygulama Bilgisi", info_text)

# Tkinter GUI oluşturma
root = tk.Tk()
root.title(f"Auto Writer v{CURRENT_VERSION}")

if sys.platform == "darwin":
    messagebox.showwarning("Uyarı", "macOS'ta çalışabilmesi için sisteminizde 'Accessibility' (Erişim) iznini vermelisiniz.")

# Logo ekleme
try:
    logo_image = Image.open("logo.png")
    logo_image = logo_image.resize((200, 200))
    logo_photo = ImageTk.PhotoImage(logo_image)
    label_logo = tk.Label(root, image=logo_photo)
    label_logo.pack(padx=10, pady=10)
except Exception as e:
    print("Logo yüklenemedi:", e)

label_text = tk.Label(root, text="Yazılacak metni giriniz:", font=("Helvetica", 12))
label_text.pack(padx=10, pady=5)

entry_text = tk.Entry(root, width=50, font=("Helvetica", 12))
entry_text.pack(padx=10, pady=5)

label_interval = tk.Label(root, text="Tıklamalar arası bekleme süresi (saniye):", font=("Helvetica", 12))
label_interval.pack(padx=10, pady=5)

entry_interval = tk.Entry(root, width=20, font=("Helvetica", 12))
entry_interval.pack(padx=10, pady=5)

frame_buttons = tk.Frame(root)
frame_buttons.pack(padx=10, pady=10)

button_start = tk.Button(frame_buttons, text="Başlat", command=start_auto_typing,
                         bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"),
                         relief=tk.RAISED, bd=3, width=10)
button_start.grid(row=0, column=0, padx=5, pady=5)

button_stop = tk.Button(frame_buttons, text="Durdur", command=stop_auto_typing,
                        bg="#f44336", fg="white", font=("Helvetica", 12, "bold"),
                        relief=tk.RAISED, bd=3, width=10)
button_stop.grid(row=0, column=1, padx=5, pady=5)

button_update = tk.Button(frame_buttons, text="Güncelle", command=update_app,
                          bg="#9C27B0", fg="white", font=("Helvetica", 12, "bold"),
                          relief=tk.RAISED, bd=3, width=10)
button_update.grid(row=1, column=0, padx=5, pady=5)

button_info = tk.Button(frame_buttons, text="Bilgi", command=show_info,
                        bg="#607D8B", fg="white", font=("Helvetica", 12, "bold"),
                        relief=tk.RAISED, bd=3, width=10)
button_info.grid(row=1, column=1, padx=5, pady=5)

button_exit = tk.Button(root, text="Çık", command=exit_app,
                        bg="#000000", fg="white", font=("Helvetica", 12, "bold"),
                        relief=tk.RAISED, bd=3, width=15)
button_exit.pack(padx=10, pady=5)

# Tray (sistem tepsisi) işlemi ayrı bir iş parçacığında çalıştırılır.
tray_thread = threading.Thread(target=setup_tray)
tray_thread.daemon = True
tray_thread.start()

root.mainloop()
