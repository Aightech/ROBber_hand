import numpy as np
import json
import cv2

cap = cv2.VideoCapture(1)
ret, frame = cap.read()
if ret != True:
    exit()
cv2.imshow('image',frame)
main_window = cv2.namedWindow('image')

json_file = open('param.json')
data = json.load(json_file)
# define range of color in HSV
lower_color = np.array(data["color_target"]["lower"])
higher_color = np.array(data["color_target"]["upper"])


def pick_color(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel = frame_hsv[y,x]
        hh = min(pixel[0]+20, 180)
        hl = max(pixel[0]-20, 0)
        sh = min(pixel[1]+70, 255)
        sl = max(pixel[1]-70, 0)
        vh = 255#min(pixel[2]+40, 255)
        vl = 0#max(pixel[2]-40, 0)

        higher_color[:] =  [hh, sh, vh]
        lower_color[:] =  [hl, sl, vl]
        print(data)
        data["color_target"]["upper"][:] = [int(v) for v in higher_color]
        data["color_target"]["lower"][:] = [int(v) for v in lower_color]
        print(data)
        print(lower_color, higher_color) 
    if event == cv2.EVENT_RBUTTONDOWN:
        print("hey")



#CALLBACK FUNCTION
cv2.setMouseCallback("image", pick_color)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # Convert BGR to HSV
    mask = cv2.inRange(frame_hsv, lower_color, higher_color) # Threshold the HSV image to get only blue colors
    cv2.imshow('image',frame)
    cv2.imshow('im2',mask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        with open('param.json', 'w') as outfile:
             print(data)
             json.dump(data, outfile)
             cap.release()
        break

# When everything done, release the capture
cv2.destroyAllWindows()
