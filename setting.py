import numpy as np
import json
import cv2
import sys

if len(sys.argv) < 2:
    print("Usage:")
    print("\t" + sys.argv[0] + " camera_nb")
    print("Ex:")
    print("\t" + sys.argv[0] + " 1")
    exit()

cap = cv2.VideoCapture(int(sys.argv[1]))
cap_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
cap_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

detector = cv2.SimpleBlobDetector_create()
fn = cv2.FileStorage("param.json", cv2.FILE_STORAGE_READ | cv2.FILE_STORAGE_FORMAT_JSON)
detector.read(fn.root())

json_file=  open('param.json')
data = json.load(json_file)
lower_color = np.array(data["color_target"]["lower"])
higher_color = np.array(data["color_target"]["upper"])
kernel = np.ones((data["opening_kernel"],data["opening_kernel"]),np.uint8)
NB_FINGER = data["NB_FINGER"]
coef = [245/(data["finger_bound"]["upper"][i]-data["finger_bound"]["lower"][i]) for i in range(NB_FINGER)]
offset = [5-coef[i]*data["finger_bound"]["lower"][i] for i in range(NB_FINGER)]
f_pos = [0 for i in range(NB_FINGER)]
count=0


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
        data["color_target"]["upper"][:] = [int(v) for v in higher_color]
        data["color_target"]["lower"][:] = [int(v) for v in lower_color]
        print()
        print("Color(HSV):")
        print(lower_color, higher_color) 
    if event == cv2.EVENT_RBUTTONDOWN:
        global count
        count = (count+1)%2
        ind=0
        for i in range(min(len(sorted_pt),NB_FINGER)):
            if i==0 or sorted_pt[i].pt[0]<sorted_pt[i-1].pt[0]-20:
                if count==0:
                    data["finger_bound"]["upper"][ind]=int(sorted_pt[i].pt[1])
                else:
                    data["finger_bound"]["lower"][ind]=int(sorted_pt[i].pt[1])
                coef[ind] = 245/(data["finger_bound"]["upper"][ind]-data["finger_bound"]["lower"][ind])
                offset[ind] = 5-coef[ind]*data["finger_bound"]["lower"][ind]
                ind+=1


#CALLBACK FUNCTION
cv2.namedWindow("image")
cv2.setMouseCallback("image", pick_color)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret!=True:
        break
    
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # Convert BGR to HSV
    mask = cv2.inRange(frame_hsv, lower_color, higher_color) # Threshold the HSV image to get only blue colors
    opening = cv2.bitwise_not(cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)) # apply an opening transformation to keep only blob
    keypoints = detector.detect(opening)# Detect blobs.
    sorted_pt = sorted(keypoints, key=lambda k: k.pt[0], reverse=True)
    im_with_keypoints = cv2.drawKeypoints(frame, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    ind=0
    for i in range(min(len(sorted_pt),NB_FINGER)):
        if i==0 or sorted_pt[i].pt[0]<sorted_pt[i-1].pt[0]-20:
            f_pos[i] = np.uint8(max(min(coef[i]*sorted_pt[i].pt[1]+offset[i],255),0))
            cv2.putText(im_with_keypoints, "top", (int(sorted_pt[i].pt[0]-cap_width/8), data["finger_bound"]["upper"][i]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            cv2.rectangle(im_with_keypoints, (int(sorted_pt[i].pt[0]-cap_width/8), data["finger_bound"]["upper"][i]), (int(sorted_pt[i].pt[0]+cap_width/8), data["finger_bound"]["lower"][i]), (0,255,0), 2)
            ind+=1
    print('\r| ', end="")
    for i in range(NB_FINGER):
        print(str(f_pos[i]) + "\t| ", end="")
    
    cv2.putText(im_with_keypoints, "Left click on the color targeted           Right click to set the " + ("Top" if count else "Lower") + " Boundaries", (0, cap_height-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    cv2.imshow('image',im_with_keypoints)
    cv2.imshow('im2',mask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        with open('param.json', 'w') as outfile:
             json.dump(data, outfile)
             cap.release()
        break

# When everything done, release the capture
cv2.destroyAllWindows()
