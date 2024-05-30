import cv2
import numpy as np
import json


cat = {'assault': 0}


def drawBox(boxes, image):
    for ann in boxes:
        x_center, y_center, width, height = ann
        
        # Convert from center coordinates to top-left corner coordinates
        x_min = int(x_center - width / 2)
        y_min = int(y_center - height / 2)
        x_max = int(x_center + width / 2)
        y_max = int(y_center + height / 2)
        
        # Draw rectangle on the image
        cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

    cv2.imshow("img", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def drawBoxFromAnnotfile(image):
    with open('/Users/jaeh/Documents/NVIDIA_AI_Academy/CV_Project/test_data/generated_annotations/frame_4845.txt') as f:
        boxes = [line.split(' ') for line in f.readlines()]
        boxes = [float(j) for i in boxes for j in i]
        print(boxes)

        boxes = [[boxes[1], boxes[2], boxes[3], boxes[4]], [boxes[6], boxes[7], boxes[8], boxes[9]]]
    for ann in boxes:
        x_center, y_center, width, height = ann

        x_center = x_center * 640
        y_center = y_center * 640
        width = width * 640
        height = height * 640
        
        # Convert from center coordinates to top-left corner coordinates
        x_min = int(x_center - width / 2)
        y_min = int(y_center - height / 2)
        x_max = int(x_center + width / 2)
        y_max = int(y_center + height / 2)
        
        # Draw rectangle on the image
        cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

    cv2.imshow("img", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def cvTest():
    # imageToPredict = cv2.imread("img.jpg", 3)
    imageToPredict = cv2.imread("CV_Project/test_data/2120699/frame_4845.jpg", 3)
    print("original image shape", imageToPredict.shape)

    # Note: flipped comparing to your original code!
    # x_ = imageToPredict.shape[0]
    # y_ = imageToPredict.shape[1]
    original_height = imageToPredict.shape[0]
    original_width = imageToPredict.shape[1]
    new_height = 640
    new_width = 640

    img = cv2.resize(imageToPredict, (640, 640))
    new_annotations = []

    with open('CV_Project/test_data/annotation_2120699.json') as f:
        data = json.load(f)
        x1 = data['frames'][0]['annotations'][0]['label']['x']
        y1 = data['frames'][0]['annotations'][0]['label']['y']
        w1 = data['frames'][0]['annotations'][0]['label']['width']
        h1 = data['frames'][0]['annotations'][0]['label']['height']
        x2 = data['frames'][0]['annotations'][1]['label']['x']
        y2 = data['frames'][0]['annotations'][1]['label']['y']
        w2 = data['frames'][0]['annotations'][1]['label']['width']
        h2 = data['frames'][0]['annotations'][1]['label']['height']
        annotations = [[x1, y1, w1, h1], [x2, y2, w2, h2]]

    for ann in annotations:
        # Unpack the annotation (x_min, y_min, width, height)
        x_min, y_min, width, height = ann
        
        # Convert to center coordinates
        x_center = x_min + width / 2
        y_center = y_min + height / 2
        
        # Scale the center coordinates and dimensions
        x_center_new = x_center * new_width / original_width
        y_center_new = y_center * new_height / original_height
        width_new = width * new_width / original_width
        height_new = height * new_height / original_height
        
        # Append the new annotation
        new_annotations.append([x_center_new, y_center_new, width_new, height_new])


    # drawBox(new_annotations, img)
    drawBoxFromAnnotfile(img)


def drawOriginal():
    image = cv2.imread("CV_Project/test_data/2120699/frame_4845.jpg", 3)
    with open('CV_Project/test_data/annotation_2120699.json') as f:
        data = json.load(f)
        print("frame num:", data['frames'][0])
        x1 = data['frames'][0]['annotations'][0]['label']['x']
        y1 = data['frames'][0]['annotations'][0]['label']['y']
        w1 = data['frames'][0]['annotations'][0]['label']['width']
        h1 = data['frames'][0]['annotations'][0]['label']['height']
        x2 = data['frames'][0]['annotations'][1]['label']['x']
        y2 = data['frames'][0]['annotations'][1]['label']['y']
        w2 = data['frames'][0]['annotations'][1]['label']['width']
        h2 = data['frames'][0]['annotations'][1]['label']['height']
        annotations = [[x1, y1, w1, h1], [x2, y2, w2, h2]]

    for ann in annotations:
        x_center, y_center, width, height = ann
        
        # Convert from center coordinates to top-left corner coordinates
        x_min = int(x_center - width / 2)
        y_min = int(y_center - height / 2)
        x_max = int(x_center + width / 2)
        y_max = int(y_center + height / 2)
        
        # Draw rectangle on the image
        cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

    cv2.imshow("img", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    

def fetchAnnot():
    with open('CV_Project/test_data/annotation_2120699.json') as f:
        data = json.load(f)
        for i in data['frames']:
            print(i['number'])



cvTest()
# drawBoxFromAnnotfile()
# drawOriginal()
# fetchAnnot()