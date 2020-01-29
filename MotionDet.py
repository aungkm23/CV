import cv2, datetime, pandas

first_frame = None
#status_list = [None, None]
#times = []
#df = pandas.DataFrame(columns=["Start", "End"])

video = cv2.VideoCapture(0)
while True:
    check, frame = video.read()
    #status = 0
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
        status = 1
        (x, y, w, h) = cv2.boundingRect(contour)  # box around the object
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    #status_list.append(status)
    #status_list = status_list[-2:]

    #if status_list[-1] == 1 and status_list[-2] ==0:
    #    times.append(datetime.datetime.now())
    #if status_list[-1] == 0 and status_list[-2] == 1:
    #    times.append(datetime.datetime.now())
    #print(status_list)
    #print(times)
  #  for i in range(0,len(times),2):
 #       df = df.append({"Start": times[i], "End": times[i+1]}, ignore_index=True)
#    print(df)
    cv2.imshow('frame', frame)
    cv2.imshow('Capturing', gray)
    cv2.imshow('delta', delta_frame)
    cv2.imshow('thresh', thresh_delta)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
video.release()
cv2.destroyAllWindows()
