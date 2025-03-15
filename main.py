import tkinter as tk
from tkinter import messagebox
import threading
import time
from pynput.keyboard import Controller, Key
import pystray
from PIL import Image, ImageDraw, ImageTk
import requests
import sys
import os

def load_version():
    """
    VERSION.txt dosyasından sürüm bilgisini okur.
    Dosya sadece "major.minor.patch" formatında bir sürüm numarası içermelidir.
    """
    try:
        with open("VERSION.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception as e:
        return "0.0.0"

# Versiyon bilgisi ve GitHub URL ayarları (URL'leri kendi deponuza göre güncelleyin)
CURRENT_VERSION = load_version()
GITHUB_VERSION_URL = "https://raw.githubusercontent.com/YourUsername/YourRepo/main/VERSION.txt"
GITHUB_MAIN_URL = "https://raw.githubusercontent.com/YourUsername/YourRepo/main/main.py"

# Global değişkenler
typing_flag = False
typing_thread = None
assigned_key = None  # Atanmış tuşu tutar
tray_icon = None     # Tray ikonunu global tutmak için

def convert_key(keysym):
    """
    Yakalanan keysym değerini pynput'un kabul edeceği forma dönüştürür.
    Eğer tuş özel bir tuşsa, mapping'den karşılığı verilir.
    """
    mapping = {
        "Return": Key.enter,
        "space": Key.space,
        "Tab": Key.tab,
        "BackSpace": Key.backspace,
        "Escape": Key.esc,
        # İhtiyaca göre eklemeler yapılabilir.
    }
    if keysym in mapping:
        return mapping[keysym]
    elif len(keysym) == 1:
        return keysym
    else:
        return keysym

def auto_typing(text, interval):
    """
    Belirtilen metni, belirlenen aralıklarla otomatik olarak yazar.
    Eğer atanmış tuş varsa, metin yazıldıktan sonra o tuşa da basar.
    """
    global typing_flag, assigned_key
    keyboard = Controller()
    while typing_flag:
        for char in text:
            keyboard.press(char)
            keyboard.release(char)
        if assigned_key is not None:
            converted_key = convert_key(assigned_key)
            try:
                keyboard.press(converted_key)
                keyboard.release(converted_key)
            except ValueError as e:
                print(f"Tuş gönderilemedi: {e}")
        time.sleep(interval)

def update_status_label():
    """
    Ana pencere üzerindeki 'Durum' etiketini günceller.
    """
    status = "Aktif" if typing_flag else "Deaktif"
    label_status.config(text=f"Durum: {status}")
    # Tray menü güncellenecekse burada işlem yapılabilir

def start_typing():
    """
    Kullanıcının girdiği metin ve aralık değerlerine göre otomatik yazmayı başlatır.
    Başlatıldığında GUI arka plana gizlenir.
    """
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
        messagebox.showinfo("Bilgi", "Auto Typer zaten çalışıyor!")
        return
    typing_flag = True
    update_status_label()
    typing_thread = threading.Thread(target=auto_typing, args=(text, interval))
    typing_thread.daemon = True
    typing_thread.start()
    root.withdraw()  # Ana pencereyi gizle, uygulama tray'de çalışmaya devam eder

def stop_typing():
    """
    Otomatik yazma işlemini durdurur.
    """
    global typing_flag, typing_thread
    typing_flag = False
    if typing_thread:
        typing_thread.join(timeout=1)
    update_status_label()
    messagebox.showinfo("Bilgi", "Auto Typer durduruldu.")

def create_image():
    """
    Sistem tepsisi için ikon resmi oluşturur. Mümkünse logo.png kullanılır.
    """
    try:
        image = Image.open("logo.png")
        image = image.resize((64, 64))
    except Exception:
        image = Image.new('RGB', (64, 64), "white")
        dc = ImageDraw.Draw(image)
        dc.rectangle((0, 0, 64, 64), fill="blue")
    return image

def on_closing():
    """
    Pencere kapatma tuşuna basıldığında pencereyi gizler.
    """
    root.withdraw()

def show_window(icon, item):
    """
    Sistem tepsisindeki 'Göster' tuşuna basıldığında ana pencereyi açar.
    """
    root.deiconify()

def quit_app(icon, item):
    """
    Sistem tepsisindeki 'Çık' tuşuna basıldığında uygulamayı tamamen kapatır.
    """
    global typing_flag, typing_thread
    typing_flag = False
    if typing_thread:
        typing_thread.join(timeout=1)
    icon.stop()
    root.destroy()

def show_status(icon, item):
    """
    Sistem tepsisindeki 'Durum' tuşuna basıldığında, uygulamanın durumunu gösteren
    küçük bir pencere açar.
    """
    status = "Aktif" if typing_flag else "Deaktif"
    status_win = tk.Toplevel()
    status_win.title("Uygulama Durumu")
    status_win.geometry("250x100")
    tk.Label(status_win, text=f"Uygulama Durumu: {status}", font=("Helvetica", 12)).pack(expand=True, pady=20)
    # Pencereyi otomatik kapatma için bir 'Tamam' butonu ekleyebilirsiniz
    tk.Button(status_win, text="Tamam", command=status_win.destroy, font=("Helvetica", 12)).pack(pady=5)

def on_clicked(icon, event):
    """
    Tray ikonuna sol tıklama algılandığında ana pencereyi açar.
    """
    if hasattr(event, 'button') and event.button == 1:
        show_window(icon, None)

def setup_tray():
    """
    Sistem tepsisi simgesini ve menüsünü oluşturur.
    Menüde dinamik durum bilgisi, 'Göster', 'Durum' ve 'Çık' seçenekleri yer alır.
    """
    global tray_icon
    image = create_image()
    menu = pystray.Menu(
        # Dinamik durum bilgisi de menüde gösterilebilir ama ayrı "Durum" butonu eklendi
        pystray.MenuItem('Göster', show_window),
        pystray.MenuItem('Durum', show_status),
        pystray.MenuItem('Çık', quit_app)
    )
    tray_icon = pystray.Icon("AutoTyper", image, "AutoTyper", menu)
    if hasattr(tray_icon, '_listener'):
        try:
            tray_icon._listener.on_click = on_clicked
        except Exception as e:
            print("Sol tıklama desteği yok:", e)
    tray_icon.run()

def capture_key():
    """
    Tuş ataması için geçici pencere açılır; basılan tuş yakalanır.
    """
    capture_win = tk.Toplevel(root)
    capture_win.title("Tuş Ataması")
    capture_win.geometry("300x100")
    label = tk.Label(capture_win, text="Lütfen bir tuşa basın...", font=("Helvetica", 12))
    label.pack(expand=True, pady=20)
    def key_pressed(event):
        global assigned_key
        assigned_key = event.keysym
        label_assigned.config(text=f"Atanmış Tuş: {assigned_key}")
        capture_win.destroy()
    capture_win.bind("<Key>", key_pressed)
    capture_win.focus_force()

def reset_key():
    """
    Atanmış tuşu sıfırlar.
    """
    global assigned_key
    assigned_key = None
    label_assigned.config(text="Atanmış Tuş: Yok")

def check_for_update():
    """
    GitHub deposundaki güncel sürüm bilgisi ile karşılaştırarak güncelleme kontrolü yapar.
    Eğer yeni bir sürüm varsa, güncelleme işlemini gerçekleştirir.
    """
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
                messagebox.showinfo("Güncelleme", "Güncelleme tamamlandı.\nLütfen uygulamayı yeniden başlatın.")
                os._exit(0)
            except Exception as e:
                messagebox.showerror("Güncelleme Hatası", f"Güncelleme yapılamadı: {e}")
    else:
        messagebox.showinfo("Güncelleme", "Uygulamanız güncel.")

def update_app():
    """
    Güncelleme kontrolü için ayrı bir iş parçacığında çalışır.
    """
    threading.Thread(target=check_for_update, daemon=True).start()

def show_info():
    """
    "Bilgi" butonuna tıklandığında uygulama bilgilerini gösterir.
    """
    info_text = (
        "Uygulama: Auto Typer\n"
        "Geliştirici: btlab\n"
        f"Sürüm: {CURRENT_VERSION}\n"
        "Bu uygulama otomatik yazma işlemi için geliştirilmiştir."
    )
    messagebox.showinfo("Uygulama Bilgisi", info_text)

# Tkinter GUI oluşturma
root = tk.Tk()
root.title(f"Auto Typer v{CURRENT_VERSION}")

# Eğer işletim sistemi macOS ise uyarı göster
if sys.platform == "darwin":
    messagebox.showwarning("Uyarı", "Bu uygulama macOS'ta düzgün çalışmayabilir.")

# Logo ekle (logo.png)
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

label_interval = tk.Label(root, text="Kaç saniyede bir (saniye):", font=("Helvetica", 12))
label_interval.pack(padx=10, pady=5)

entry_interval = tk.Entry(root, width=20, font=("Helvetica", 12))
entry_interval.pack(padx=10, pady=5)

label_status = tk.Label(root, text="Durum: Deaktif", font=("Helvetica", 12, "bold"))
label_status.pack(padx=10, pady=5)

frame_key = tk.Frame(root)
frame_key.pack(padx=10, pady=10)

label_assigned = tk.Label(frame_key, text="Atanmış Tuş: Yok", font=("Helvetica", 12))
label_assigned.grid(row=0, column=0, columnspan=2, pady=(0, 5))

button_set_key = tk.Button(frame_key, text="Tuş Ata", command=capture_key,
                           bg="#2196F3", fg="white", font=("Helvetica", 12, "bold"),
                           relief=tk.RAISED, bd=3, width=10)
button_set_key.grid(row=1, column=0, padx=5, pady=5)

button_reset_key = tk.Button(frame_key, text="Tuşu Sıfırla", command=reset_key,
                             bg="#FF9800", fg="white", font=("Helvetica", 12, "bold"),
                             relief=tk.RAISED, bd=3, width=10)
button_reset_key.grid(row=1, column=1, padx=5, pady=5)

button_start = tk.Button(root, text="Başlat", command=start_typing,
                         bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"),
                         relief=tk.RAISED, bd=3, width=15)
button_start.pack(padx=10, pady=5)

button_stop = tk.Button(root, text="Durdur", command=stop_typing,
                        bg="#f44336", fg="white", font=("Helvetica", 12, "bold"),
                        relief=tk.RAISED, bd=3, width=15)
button_stop.pack(padx=10, pady=5)

button_update = tk.Button(root, text="Güncelle", command=update_app,
                          bg="#9C27B0", fg="white", font=("Helvetica", 12, "bold"),
                          relief=tk.RAISED, bd=3, width=15)
button_update.pack(padx=10, pady=5)

button_info = tk.Button(root, text="Bilgi", command=show_info,
                        bg="#607D8B", fg="white", font=("Helvetica", 12, "bold"),
                        relief=tk.RAISED, bd=3, width=15)
button_info.pack(padx=10, pady=5)

root.protocol("WM_DELETE_WINDOW", on_closing)

# Tray (sistem tepsisi) işlemi ayrı bir iş parçacığında çalıştırılır.
tray_thread = threading.Thread(target=setup_tray)
tray_thread.daemon = True
tray_thread.start()

root.mainloop()
