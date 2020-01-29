import cv2
import pyzbartest
from pyzbar import pyzbar
import time
import numpy

video = cv2.VideoCapture(0)
a = 1
while True:
    check, frame = video.read()
    w, h, c = frame.shape
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    print(frame[w // 2:(w // 2) + 1, h // 2:(h // 2) + 1, :])
    barcodes = pyzbar.decode(gray)
    #pyzbartest.frameDecode(frame)
    #     gray = cv2.GaussianBlur(gray, (21, 21), 0)
    #     if first_frame is None:
    #         first_frame = gray
    #         continue
    # delta_frame = cv2.absdiff(first_frame, gray)
    # thresh_delta = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    # thresh_delta = cv2.dilate(thresh_delta, None, iterations=0)
    # (_, cnts, _) = cv2.findContours(thresh_delta.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # for contour in cnts:
    #     if cv2.contourArea(contour) < 1000:
    #         continue
    #     (x, y, w, h) = cv2.boundingRect(contour)
    #     cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)


    # for barcode in barcodes:
    #     # extract the bounding box location of the barcode and draw
    #     # the bounding box surrounding the barcode on the image
    #     (x, y, w, h) = barcode.rect
    #     cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
    #     # the barcode data is a bytes object so if we want to draw it
    #     # on our output image we need to convert it to a string first
    #     barcodeData = barcode.data.decode("utf-8")
    #     barcodeType = barcode.type
    #     # draw the barcode data and barcode type on the image
    #     text = "{} ({})".format(barcodeData, barcodeType)
    #     cv2.putText(frame, text, (x, y - 10),
    #                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        # if the barcode text is currently not in our CSV file, write
        # the timestamp + barcode to disk and update the set
        # to uncomment here
        # if barcodeData not in found:
        #     csv.write("{},{}\n".format(datetime.datetime.now(),
        #                                barcodeData))
        #     csv.flush()
        #     found.add(barcodeData)
    #     cv2.imshow("Barcode Scanner", frame)
    #     key = cv2.waitKey(1) & 0xFF
    #
    #     #if the `q` key was pressed, break from the loop
    #     if key == ord("q"):
    #        break

    for barcode in barcodes:
        # extract the bounding box location of the barcode and draw the
        # bounding box surrounding the barcode on the image
        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # the barcode data is a bytes object so if we want to draw it on
        # our output image we need to convert it to a string first
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        # draw the barcode data and barcode type on the image
        text = "{} ({})".format(barcodeData, barcodeType)
        cv2.putText(gray, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                  0.5, (0, 0, 255), 2)
        # print the barcode type and data to the terminal
        print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
    cv2.imshow("Capturing", frame)
    key = cv2.waitKey(100)
    # a=a+1
    if (key == ord('q')):
        break
print(a)  # Number of frames will be printed
video.release()
cv2.destroyAllWindows()
