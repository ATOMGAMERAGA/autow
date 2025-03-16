# Auto W (Auto Writer)

## Linux:

Kurmak için relases bölümünden en son versiyonun bütün kodunu yükleyin ve dosyaya çıkarın zip dosyasını , ardından sağ tıklayıp burda terminal aça tıklayın sonra sanal ortam oluşturun ve ondanda "bash" yazıp sonra aktif edin sonra gerekli modülleri ve gerekli yan moülleri yükleyin ve en son herşey bitince sanal ortamdayken "python main.py" yazın.

## Windows:

Kurmak için relases bölümünden en son versiyonun bütün kodunu yükleyin ve dosyaya çıkarın zip dosyasını , ardından bilgisayarınıza en son pythonu [buraya tıklayarak](https://www.python.org/ftp/python/3.13.2/python-3.13.2-amd64.exe) yükleyin sonra yukardaki dosya konum yerine tıklayıp herşeyi silip "cmd" yazıp enter tuşuna basın açılan yere gerekli modülleri yükleyin ancak yan mödül olan tkinterı siz "pip install tk" komutuyla indirin ve herşey bitince "python main.py" yazın.

## Komutlar:

Sanal Ortamı Oluşturma:
 python3 -m venv myenv

Sanal Ortamı Aktif Etme:
 source myenv/bin/activate

Gerekli Modül:
 pip install pynput pystray pillow requests pyautogui



Gerekli Yan Modül:
 Debian or Ubuntu:
  sudo apt-get update
  sudo apt-get install python3-tk

 Fedora:
  sudo dnf install python3-tkinter

 Arch:
  sudo pacman -S tk
