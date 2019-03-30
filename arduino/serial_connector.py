import serial
import time

s = serial.Serial("COM3", 9600)  # port is COM3, and baud rate is 9600
time.sleep(2)  # wait for the Serial to initialize
s.write(b'Ready...')
while True:
    text = input('Enter text: ')
    text = text.strip()
    if text == 'exit':
        break
    s.write(bytes(text, "utf8"))
