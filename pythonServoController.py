import serial
import struct
usbport = "COM6"
arduino = serial.Serial(usbport, 9600)
arduino.write(struct.pack('>B',40))
