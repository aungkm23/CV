from __future__ import print_function
import pyzbar.pyzbar as pyzbar
import numpy as np
import time
import cv2


def decode(name):
    # Find barcodes and QR codes
    decodedObjects = pyzbar.decode(name)

    # Print results
    for obj in decodedObjects:
        print('Type : ', obj.type)
        print('Data : ', str(obj.data), '\n')

    return decodedObjects


# Display barcode and QR code location
def display(name, decodedObjects):
    # Loop over all decoded objects
    for decodedObject in decodedObjects:
        points = decodedObject.polygon

        # If the points do not form a quad, find convex hull
        if len(points) > 4:
            hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
            hull = list(map(tuple, np.squeeze(hull)))
        else:
            hull = points;

        # Number of points in the convex hull
        n = len(hull)

        # Draw the convext hull
        for j in range(0, n):
            cv2.line(name, hull[j], hull[(j + 1) % n], (255, 0, 0), 3)

    #cv2.imshow("Results", im);
    cv2.waitKey(0);


# Main
# if __name__ == '__main__':
#   # Read image
#   #im = cv2.imread('zbar-test.jpg')
#   #im = cv2.resize(im, (500,500))
#   video = cv2.VideoCapture(0)
#   a = 1
#   while True:
#     a = a+1
#     check, frame = video.read()
#   #im = cv2.resize(im, (500,500))
#     decodedObjects = decode(frame)
#     display(frame, decodedObjects)
#     cv2.imshow("frame", frame)
#     key = cv2.waitKey(1)
#     if (key == ord('q')):
#       break
#   video.release()
#   cv2.destroyAllWindows()

def frameDecode(name):
    decodedObjects = decode(name)
    display(name, decodedObjects)


# Main
if __name__ == '__main__':
    im = cv2.imread('zbar-test.jpg')
    print(im)
    frameDecode(im)
