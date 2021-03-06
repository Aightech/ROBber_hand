import numpy as np
import json
import cv2
import serial
import struct
arduino = serial.Serial('COM5', 9600, timeout=.1)
count = 0
v = np.uint8(255)
w = np.uint8(2)
a = v+w
print(a)
# while True:
    # arduino.write(bytes('#',"utf-8"))
    # str = b''
    # for i in range(4):
        # str += struct.pack('!B',count)
    # count = count + 1 if count<180 else 0
    # print(str)
    # arduino.write(str)
    # print("#####")
    # for i in range(5):
        # data = arduino.read() 
        # print(data)