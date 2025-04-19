# Auto W (Auto Writer)

## Basit Kurulum

Dosya vb. şeyler uğraşmak istemiyorsanız ve bir begginer sanız (buraya tıklayarak)[still-working-on] linux versiyonunu indirebilirsiniz daha windows versiyonu geliştirme aşamasında ancak manuel olarak windowsa kurup deneyebilirsiniz (buraya tıklayarak)[https://github.com/ATOMGAMERAGA/autow/tree/main#windows]

## Linux:

Kurmak için (buraya tıklayıp)[https://github.com/ATOMGAMERAGA/autow/archive/refs/heads/main.zip] inderilen dosyaya sağ tıkalyıp ordan çıkarın zip dosyasını , ardından bulunduğnuz konumda boş bir yere dosya yöneticinizde sağ tıklayıp burda terminal aça tıklayın sonra sanal ortam oluşturun ve orayada "bash" yazıp sonra aktif edin sonra gerekli modülleri ve gerekli yan moülleri yükleyin ve en son herşey bitince sanal ortamdayken "python main.py" yazın ve hazırsınız bu dediğim kodlarda aşşağda (komutlar)[https://github.com/ATOMGAMERAGA/autow/tree/main#komutlar] bölümünde yazıyor.

## Windows:

Kurmak için (buraya tıklayıp)[https://github.com/ATOMGAMERAGA/autow/archive/refs/heads/main.zip] indirilen dosyayı winrar veya vb. bir uygulama kullanarak çıkarın , ardından bilgisayarınıza en son pythonu [buraya tıklayarak](https://www.python.org/ftp/python/3.13.2/python-3.13.2-amd64.exe) yükleyin sonra yukardaki dosya konum yerine tıklayıp herşeyi silip "cmd" yazıp enter tuşuna basın açılan yere gerekli modülleri yükleyin ancak yan mödül olan tkinterı siz "pip install tk" komutuyla indirin ve herşey bitince "python main.py" yazın burda bahsettiğim herşeyi (komutlar)[https://github.com/ATOMGAMERAGA/autow/tree/main#komutlar] bölümünde bulabilirsiniz.

## Komutlar: 

### Sanal Ortamı Oluşturma:
   `python3 -m venv myenv`

### Sanal Ortamı Aktif Etme:
   `source myenv/bin/activate`

### Gerekli Modül:
   `pip install pynput pystray pillow requests pyautogui sv-ttk`



### Gerekli Yan Modül (Sadece Linux):
 Debian or Ubuntu:
  `sudo apt-get update`
  `sudo apt-get install python3-tk`

 Fedora:
  `sudo dnf install python3-tkinter`

 Arch:
  `sudo pacman -S tk`

### Gerekli Yan Modül (Sadece Windows):
 Windows:
  `pip install tk`
  
