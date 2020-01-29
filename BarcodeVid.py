import cv2
from pyzbar import pyzbar

debug = False


def Scanning(vid, debug):
    while True:
        try:
            check, frame = vid.read()
            w, h, c = frame.shape
        except AttributeError:
            print('Video Camera off probably')
            exit(1)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if debug:
            print(frame[w // 2:(w // 2) + 1, h // 2:(h // 2) + 1, :])

        barcodes = pyzbar.decode(gray)

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
        #cv2.imshow("Capturing", frame)
        key = cv2.waitKey(100)
        # a=a+1
        if key == ord('q'):
            break


if(__name__) == '__main__':
    video = cv2.VideoCapture(0)
    Scanning(video, debug)
   # print(x)  # Number of frames will be printed
    video.release()
    cv2.destroyAllWindows()
