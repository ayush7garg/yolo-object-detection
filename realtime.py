import cv2
import numpy as np

def gray(image):
    gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)#cvtColor converts an image from one color space to another
    return gray

def yolo():

    # Load Yolo
    net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
    classes = []
    with open("coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))

    #Loading Video
    cap = cv2.VideoCapture(0)
    while(True):
        _,img = cap.read()
        # img = gray(img)
        # img = cv2.resize(img, None, fx=1, fy=1)
        height, width, channels = img.shape
    	# Detecting objects
        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

        net.setInput(blob)
        outs = net.forward(output_layers)

        # Showing informations on the screen
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.6:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        length = len(boxes)
        # print(indexes)
        font = cv2.FONT_HERSHEY_PLAIN
        for i in range(length):
            if i in indexes:
                x, y, w, h = boxes[i]
                cv2.rectangle(img, (x, y), (x + w, y + h), colors[i], 2)
                cv2.putText(img, str(classes[class_ids[i]]), (x, y + 30), font, 3, colors[i], 3)


        cv2.imshow("Objects Detected", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
if __name__ == '__main__':
    yolo()
