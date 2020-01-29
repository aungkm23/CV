import cv2, datetime, pandas
import pyzbartest
import BarcodeVid

first_frame = None
#status_list = [None, None]
#times = []
#df = pandas.DataFrame(columns=["Start", "End"])
def motionDet(testvideo,first_frame):
    while True:
        check, frame = testvideo.read()
        flag = 0
        # status = 0
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        if first_frame is None:
            first_frame = gray
            continue
        delta_frame = cv2.absdiff(first_frame, gray)  # calculates the difference between the first and other frames
        thresh_delta = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]  # threshold value, if difference > 30, it will convert pixels to white
        thresh_delta = cv2.dilate(thresh_delta, None, iterations=0)
        cnts, B = cv2.findContours(thresh_delta.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in cnts:
                if cv2.contourArea(contour) < 1000:  # removes noises and shadows (< 1000 pixels)
                    continue
                else:
                    flag = 1
                    break
        if flag == 1:
            break
        #cv2.imshow("frame", frame)
        # cv2.imshow('Capturing', gray)
        # cv2.imshow('delta', delta_frame)
        # cv2.imshow('thresh', thresh_delta)
        key = cv2.waitKey(1)
        # if key == ord('q'):
        #     break
   # cv2.destroyAllWindows()
    return 1;

if (__name__)  == '__main__' :
    video = cv2.VideoCapture(0) #swap this out with the Image file
    x = motionDet(video, first_frame)
    print(x)
    BarcodeVid.Scanning(video, False)
    video.release()

