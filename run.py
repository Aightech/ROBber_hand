import numpy as np
import json
import cv2
import serial
import struct
import sys
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)


#connect to the arduino
if len(sys.argv) < 3:
    print("Usage:")
    print("\t" + sys.argv[0] + " arduino_port camera_nb")
    print("Ex:")
    print("\t" + sys.argv[0] + " COM5 1")
    exit()


arduino = serial.Serial(sys.argv[1], 9600, timeout=1)

#get parameters
detector = cv2.SimpleBlobDetector_create()
fn = cv2.FileStorage("param.json", cv2.FILE_STORAGE_READ | cv2.FILE_STORAGE_FORMAT_JSON)
detector.read(fn.root())
json_file=  open('param.json')
data = json.load(json_file)
lower_color = np.array(data["color_target"]["lower"])
higher_color = np.array(data["color_target"]["upper"])
kernel = np.ones((data["opening_kernel"],data["opening_kernel"]),np.uint8)
NB_FINGER = data["NB_FINGER"]
f_pos = [0 for i in range(NB_FINGER)]
coef = [245/(data["finger_bound"]["upper"][i]-data["finger_bound"]["lower"][i]) for i in range(NB_FINGER)]
offset = [5-coef[i]*data["finger_bound"]["lower"][i] for i in range(NB_FINGER)]

#get camera
cap = cv2.VideoCapture(int(sys.argv[2]))
cap_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret!=True:
        break
    
    #processing to get only target at the tip of fingers
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # Convert BGR to HSV
    mask = cv2.inRange(hsv, lower_color, higher_color) # Threshold the HSV image to get only blue colors
    opening = cv2.bitwise_not(cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)) # apply an opening transformation to keep only blob
    keypoints = detector.detect(opening)# Detect blobs.
    sorted_pt = sorted(keypoints, key=lambda k: k.pt[0], reverse=True)#sort the key point to get them from right to left
    im_with_keypoints = cv2.drawKeypoints(frame, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    
    #process the finger position to get value from 0 to 255
    ind=0
    for i in range(min(len(sorted_pt),NB_FINGER)):
        if i==0 or sorted_pt[i].pt[0]<sorted_pt[i-1].pt[0]-20:
            f_pos[ind] = np.uint8(max(min(coef[ind]*sorted_pt[i].pt[1]+offset[ind],255),0))
            cv2.rectangle(im_with_keypoints, (int(sorted_pt[i].pt[0]-cap_width/8), data["finger_bound"]["upper"][ind]), (int(sorted_pt[i].pt[0]+cap_width/8), data["finger_bound"]["lower"][i]), (0,255,0), 2)
            ind += 1
    
    #Send position to the arduino and print in the terminal
    buffer = b'##'
    crc = np.uint8(0)
    print('\r| ', end="")
    for i in range(NB_FINGER):
        print(str(f_pos[i]) + "\t| ", end="")
        buffer += struct.pack('!B',f_pos[i])
        crc += f_pos[i]
    buffer += struct.pack('!B',crc)
    arduino.write(buffer)
    d = arduino.read()
    if int.from_bytes(d,"big") == int(crc):
        print("\t COM OK         ", end="")
    else:
        print("\t COM ERR " + str(int.from_bytes(d,"big")) + "|" + str(crc))
    # Display the resulting frame
    cv2.imshow('image',im_with_keypoints)
    cv2.imshow('real',opening)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
print("\nEND")
