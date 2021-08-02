#Normal çalışma ortamı 200 lx
#Konferans odası 300
#Spor salonu 500
#İç Koridor 200
#Konferans Salonu 200
#Giriş, Atria 200
#Merdiven 200
#Tuvalet 200
#Dolap Ofası 200
#Depo 200
#Çöp Odası 200
#Mutfak 500
#Yemek Salonu 150

import serial.tools.list_ports
import serial
import PySimpleGUI as sg
import time
ser = None  #Global tanımlanmalı
def serial_ports():
    ports = serial.tools.list_ports.comports()
    print(ports)
    seri_port = []
    for p in ports:
        print(p.device)
        seri_port.append(p.device)
    print(seri_port)
    return seri_port
########################
def serial_baglan():
    com_deger = value[0]
    baud_deger = value[1]
    print("Baud Deger", value[1])
    global ser
    ser = serial.Serial(com_deger, baud_deger, timeout=0, parity=serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE , bytesize = serial.EIGHTBITS, rtscts=0)
    window["-BAGLANDI_TEXT-"].update('Bağlandı...')

def lux_oku(ortam):
    print(ortam)
    for i in range(20):
        data = ser.readline().decode('Ascii')
        time.sleep(0.1)
    print(data)
    mix_lux = 0
    if (ortam == "Ofis" or ortam == "İç Koridor" or ortam == "Konferans Salonu" or ortam == "Giriş" or ortam == "Merdiven" or ortam == "Tuvalet" or ortam == "Dolap Odası" or ortam == "Depo" or ortam == "Çöp Odası"):
        min_lux = 200
    elif (ortam == "Konferans Odası"):
        min_lux = 300
    elif(ortam == "Spor Salonu" or ortam == "Mutfak"):
        min_lux = 500
    elif(ortam == "Yemek Salonu"):
        min_lux = 150
    
    lux = int(data)

    if (lux < min_lux):
        sg.popup("Yetersiz Işık... Ölçülen {} lux En az olması gereken {} lux".format(lux, min_lux), title="UYARI!")
    elif(lux > (min_lux + 200)):
        sg.popup("Fazla Işık..! Ölçülen {} lux En az olması gereken {} lux".format(lux, min_lux), title="UYARI")
    elif(lux > min_lux):
        sg.popup("Aydınlatma Yeterli... Ölçülen {} lux. En az miktar {} lux".format(lux, min_lux), title="OK!")

sg.theme("Reddit")

secim = ["Ofis", "Konferans Odası", "Spor Salonu", "İç Koridor", "Konferans Salonu",
        "Giriş", "Merdiven", "Tuvalet", "Dolap Odası", "Depo", "Çöp Odası", "Mutfak", "Yemek Salonu"]

olcum_layout = [
    [sg.Text("Ölçüm Yapılan Ortamı Seçiniz:"), sg.Combo(secim, key="secim"), sg.Button("Ölçüm Yap", key="olc")],
    [sg.Text("Ölçüm Yaparken Algılayıcıyı Çalışma Ortamında Işık Kaynağına Doğru Tutunuz.")]
]

layout =[ [sg.Text("Port Seçiniz:"), sg.Combo(serial_ports(), size=(10,1)),
            sg.Text("Baud Seçiniz:"), sg.Combo(["110","300","600","1200", "2400", "4800", "9600", "14400", "19200", "38400", "57600", "115200", "128000", "256000"], default_value=9600), 
            sg.Button(button_text="Bağlan", key="-BAGLAN-", size=(10,1)) ],
            [sg.Text("", size=(10,1), key="-BAGLANDI_TEXT-")],
            [sg.Frame("Ölçüm", olcum_layout)]
        ]

window = sg.Window("Python Seri Port", layout)

while True:
    event, value = window.read(timeout=1000) 
    if event == sg.WIN_CLOSED or event == 'Exit':
        break    
    if event == "-BAGLAN-":
        if (value[0] == ""):
            sg.popup("Bir Port Seçiniz!", title="Hata", custom_text="Tamam") 
        elif (value[1] == ""):
            sg.popup("Baud Oranını Seçiniz!", title="Hata", custom_text="Tamam")
        else:
            serial_baglan()
    if event == "olc":
        lux_oku(value['secim'])
window.close()
