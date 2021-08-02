from machine import *
from bh1750 import BH1750

uart = UART(1, 9600, tx = Pin(8), rx = Pin(9))
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
print(i2c.scan())
s = BH1750(i2c)

while True:
    s.on()
    okuma = s.luminance(BH1750.ONCE_HIRES_1)
    deger = int.from_bytes(okuma, "big")
    uart.write(str(deger) + '\n')