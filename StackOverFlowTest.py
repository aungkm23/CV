# import the necessary packages
import numpy as np
import cv2
import easygui
from matplotlib import pyplot as plt


# Defining function for finding barcodes
def find_barcode(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Sobel gradients for x an y direction of the image
    X = cv2.Sobel(gray, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=-1)
    Y = cv2.Sobel(gray, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=-1)

    # Sobel gradient magnitude (normalised to 0-3)
    grad_sobel = np.sqrt(X * X + Y * Y)
    cv2.normalize(grad_sobel, grad_sobel, 0, 3, cv2.NORM_MINMAX)

    # Blur and threshold the gradient magnitude
    blurred = cv2.blur(grad_sobel, (12, 12))

    # Extract maximum values of the pixels from blurred image
    (_, maxVal, _, _) = cv2.minMaxLoc(blurred)

    # Extract mean and standard deviation values of the pixels from 'Blurred Sobel Gradient Magnitude'
    (mean, stddev) = cv2.meanStdDev(blurred)

    # Apply threshold:
    # mean+stddev and maxVal as lower and upper limits
    (_, thresh) = cv2.threshold(blurred, mean + stddev, maxVal, cv2.THRESH_BINARY)

    # Kernel created
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))

    # Kernel applied to the image with opening and closing algorithms
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    opened = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel)

    # Convert the float image to 8-bit image
    opened = cv2.convertScaleAbs(opened)

    # Find all contours
    contours,B = cv2.findContours(opened, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_NONE)

    # Sort all contours by area (descending order)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    # Bounding rectangle thickness is set relative to the image
    height, width, channels = image.shape
    if height > width:
        lineThickness = int(round(height * 0.01))
    else:
        lineThickness = int(round(width * 0.01))

    # Draw bounding rectangle around the biggest contour on the original image
    # The rectangle is a minimum area rectangle meaning it is rotated to fit the contour
    rect = cv2.minAreaRect(contours[0])
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(image, [box], 0, (255, 0, 0), lineThickness)

    # Create variables to store contour index number and margin
    count = 1
    margin = 0.15

    # While the nth contour area is within the set margin - highlight it.
    while ((cv2.contourArea(contours[0]) - cv2.contourArea(contours[count])) / cv2.contourArea(contours[0]) < margin):
        rect = cv2.minAreaRect(contours[count])
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(image, [box], 0, (255, 0, 0), lineThickness)
        # Increment the index to check the next contour
        count = count + 1

    # Returns back image with highlighted barcodes
    return image


# Initialise the camera
cap = cv2.VideoCapture(0)

while (True):
    # Capture frame
    ret, frame = cap.read()

    # Pass the frame to the function and display the returned result
    cv2.imshow('Any Barcodes are highlighted', find_barcode(frame))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()