# GenData.py

import numpy as np
import cv2


# module level variables ##########################################################################
MIN_CONTOUR_AREA = 40


RESIZED_IMAGE_WIDTH = 20
RESIZED_IMAGE_HEIGHT = 30

###################################################################################################


def main():
    # read in training numbers image
    imgTrainingNumbers = cv2.imread("training_chars.png")

    # get grayscale image
    imgGray = cv2.cvtColor(imgTrainingNumbers, cv2.COLOR_BGR2GRAY)
    imgBlurred = cv2.GaussianBlur(
        imgGray, (5, 5), 0)                        # blur

    # filter image from grayscale to black and white
    imgThresh = cv2.adaptiveThreshold(imgBlurred,                           # input image
                                      255,                                  # make pixels that pass the threshold full white
                                      # use gaussian rather than mean, seems to give better results
                                      cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      # invert so foreground will be white, background will be black
                                      cv2.THRESH_BINARY_INV,
                                      # size of a pixel neighborhood used to calculate threshold value
                                      11,
                                      2)                                    # constant subtracted from the mean or weighted mean

    # show threshold image for reference
    cv2.imshow("imgThresh", imgThresh)

    # make a copy of the thresh image, this in necessary b/c findContours modifies the image
    imgThreshCopy = imgThresh.copy()

    imgContours, npaContours, npaHierarchy = cv2.findContours(imgThreshCopy,        # input image, make sure to use a copy since the function will modify this image in the course of finding contours
                                                              cv2.RETR_EXTERNAL,                 # retrieve the outermost contours only
                                                              cv2.CHAIN_APPROX_SIMPLE)           # compress horizontal, vertical, and diagonal segments and leave only their end points

    # declare empty numpy array, we will use this to write to file later
    # zero rows, enough cols to hold all image data
    npaFlattenedImages = np.empty(
        (0, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))

    # declare empty classifications list, this will be our list of how we are classifying our chars from user input, we will write to file at the end
    intClassifications = []

    intValidChars = [ord('0'), ord('1'), ord('2'), ord('3'), ord('4'), ord('5'), ord('6'), ord('7'), ord('8'), ord('9'),
                     ord('A'), ord('B'), ord('C'), ord('D'), ord('E'), ord(
                         'F'), ord('G'), ord('H'), ord('I'), ord('J'),
                     ord('K'), ord('L'), ord('M'), ord('N'), ord('O'), ord(
                         'P'), ord('Q'), ord('R'), ord('S'), ord('T'),
                     ord('U'), ord('V'), ord('W'), ord('X'), ord('Y'), ord('Z')]  # L?? m?? ascii c???a m???y ch??? n??y

    for npaContour in npaContours:                          # for each contour
        # if contour is big enough to consider
        if cv2.contourArea(npaContour) > MIN_CONTOUR_AREA:
            [intX, intY, intW, intH] = cv2.boundingRect(
                npaContour)         # get and break out bounding rect

            # draw rectangle around each contour as we ask user for input
            cv2.rectangle(imgTrainingNumbers,           # draw rectangle on original training image
                          (intX, intY),                 # upper left corner
                          (intX+intW, intY+intH),        # lower right corner
                          (0, 0, 255),                  # red
                          2)                            # thickness

            # crop char out of threshold image
            imgROI = imgThresh[intY:intY+intH, intX:intX+intW]
            # resize image, this will be more consistent for recognition and storage
            imgROIResized = cv2.resize(
                imgROI, (RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT))

            # show cropped out char for reference
            cv2.imshow("imgROI", imgROI)
            # show resized image for reference
            cv2.imshow("imgROIResized", imgROIResized)

            # show training numbers image, this will now have red rectangles drawn on it
            cv2.imshow("training_numbers.png", imgTrainingNumbers)

            intChar = cv2.waitKey(0)                     # get key press

            if intChar == 27:                   # if esc key was pressed
                sys.exit()                      # exit program
            # else if the char is in the list of chars we are looking for . . .
            elif intChar in intValidChars:

                # append classification char to integer list of chars (we will convert to float later before writing to file)
                intClassifications.append(intChar)
                # L?? file ch???a label c???a t???t c??? c??c ???nh m???u, t???ng c???ng c?? 32 x 5 = 160 m???u.
                # flatten image to 1d numpy array so we can write to file later
                npaFlattenedImage = imgROIResized.reshape(
                    (1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))

                # add current flattened impage numpy array to list of flattened image numpy arrays
                npaFlattenedImages = np.append(
                    npaFlattenedImages, npaFlattenedImage, 0)

            # end if
        # end if
    # end for

    # convert classifications list of ints to numpy array of floats
    fltClassifications = np.array(intClassifications, np.float32)

    # flatten numpy array of floats to 1d so we can write to file later
    npaClassifications = fltClassifications.reshape(
        (fltClassifications.size, 1))

    print("\n\ntraining complete !!\n")

    # write flattened images to file
    np.savetxt("classifications.txt", npaClassifications)
    np.savetxt("flattened_images.txt", npaFlattenedImages)          #

    cv2.destroyAllWindows()             # remove windows from memory

    return


###################################################################################################
if __name__ == "__main__":
    main()
# end if
