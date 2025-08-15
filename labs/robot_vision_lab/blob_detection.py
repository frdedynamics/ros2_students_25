import cv2
import numpy as np
import glob

def plot_channels(image, plot=False):
    if plot:
        cv2.imshow("Original RGB", image)
        cv2.imshow("B", image[:,:,0])
        cv2.imshow("G", image[:,:,1])
        cv2.imshow("R", image[:,:,2])
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def convert_colorspace(image, plot=False):
    # Convert to Lab color space
    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    if plot:
        cv2.imshow("Original RGB", image)
        cv2.imshow("L", lab_image[:,:,0])
        cv2.imshow("A", lab_image[:,:,1])
        cv2.imshow("B", lab_image[:,:,2])
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return lab_image

def threshold_image_rgb(image, plot=False):
    # Threshold the image
    thresholded_image = cv2.inRange(image, np.array([5,30,180]), np.array([160,60,195]))

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(image, image, mask=thresholded_image)
    if plot:
        cv2.imshow("Thresholded", thresholded_image)
        cv2.imshow("Result", res)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return thresholded_image

def threshold_image(lab_image, image, plot=False):
    # Threshold the image
    threshold = 20
    #_, thresholded_image = cv2.threshold(lab_image[:,:,2], threshold, 255, cv2.THRESH_BINARY)
    thresholded_image = cv2.inRange(lab_image[:,:,2], 20, 180)
    
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(image, image, mask=thresholded_image)
    if plot:
        cv2.imshow("Thresholded", thresholded_image)
        cv2.imshow("Result", res)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return thresholded_image

def setup_blob_detector():
    # Set up the SimpleBlobDetector parameters.
    params = cv2.SimpleBlobDetector_Params()

    # Filter by Area.
    params.filterByArea = False
    params.minArea = 15
    params.maxArea = 6000

    # Filter by Circularity
    params.filterByCircularity = False
    params.minCircularity = 0.1

    # Filter by Convexity
    params.filterByConvexity = False
    params.minConvexity = 0.5

    # Filter by Inertia
    params.filterByInertia = False
    params.minInertiaRatio = 0.01

    # Create a detector with the parameters
    detector = cv2.SimpleBlobDetector_create(params)
    return detector

def detect_blobs(thresholded_image, image, detector, plot=False):
    # Detect blobs.
    keypoints = detector.detect(~thresholded_image)

    # Draw detected blobs as red circles.
    im_with_keypoints = cv2.drawKeypoints(image, keypoints, np.array([]), (0, 0, 255),
                                        cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    # Draw a marker at the center of each keypoint
    for keypoint in keypoints:
        cv2.drawMarker(im_with_keypoints, tuple(int(i) for i in keypoint.pt), color=(0,255,0))

    # Show blobs
    if plot:
        cv2.imshow("Blobs", im_with_keypoints)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    
    # Load single color image:
    # images = [cv2.imread("img/ball01.jpg")]
    # if images is None:
    #     print("Image not found. Check file path to image.")
    #     exit()

    # Load all images:
    images = [cv2.imread(file) for file in glob.glob("img/*.jpg")]
    if len(images) == 0:
        print("No images found. Check file path to images.")
        exit()
    
    # Plot the channels
    for image in images:
        plot_channels(image, plot=True)

    # Convert to Lab color space:
    lab_images = []
    for image in images:
        lab_image = convert_colorspace(image, plot=True)
        lab_images.append(lab_image)

    # Threshold the image
    thresholded_images = []
    for lab_image, image in zip(lab_images, images):
        #thresholded_image = threshold_image_rgb(image, plot=True)
        thresholded_image = threshold_image(lab_image, image, plot=True)
        thresholded_images.append(thresholded_image)

    # Set up the blob detector
    detector = setup_blob_detector()
    
    # Detect blobs
    for thresholded_image, image in zip(thresholded_images, images):
        detect_blobs(thresholded_image, image, detector, plot=True)
