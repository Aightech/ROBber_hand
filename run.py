import numpy as np
import json
import cv2
import serial
import struct

arduino = serial.Serial('COM5', 9600, timeout=.1)

detector = cv2.SimpleBlobDetector_create()
fn = cv2.FileStorage("param.json", cv2.FILE_STORAGE_READ | cv2.FILE_STORAGE_FORMAT_JSON)
detector.read(fn.root())

json_file=  open('param.json')
data = json.load(json_file)
lower_color = np.array(data["color_target"]["lower"])
higher_color = np.array(data["color_target"]["upper"])
kernel = np.ones((10,10),np.uint8)

f_pos = [0,0,0,0]
count = 0

cv2.namedWindow('image')
cap = cv2.VideoCapture(1)
ret, frame = cap.read()
if ret != True:
    exit()
cv2.imshow('image',frame)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret!=True:
        break
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # Convert BGR to HSV
    mask = cv2.inRange(hsv, lower_color, higher_color) # Threshold the HSV image to get only blue colors
    opening = cv2.bitwise_not(cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)) # apply an opening transformation to keep only blob

    keypoints = detector.detect(opening)# Detect blobs.
    sorted_pt = sorted(keypoints, key=lambda k: k.pt[0], reverse=True)
    
    for i in range(min(len(sorted_pt),4)):
        f_pos[i] = 500-sorted_pt[i].pt[1]

    print('\r| ', end="")
    for v in f_pos:
        print("{:.2f}\t| ".format(int(max(min(v-200,255),0))), end="")
    
    str = b'##'
    for i in range(4):
        str += struct.pack('!B',int(max(min(f_pos[i]-210, 255),0)) )
    count = count + 1 if count<180 else 0
    print(str)
    arduino.write(str)
    print("#####")
    for i in range(5):
        data = arduino.read() 
        print(data)
    
    im_with_keypoints = cv2.drawKeypoints(frame, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    # Display the resulting frame
    cv2.imshow('image',im_with_keypoints)
    cv2.imshow('real',opening)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
