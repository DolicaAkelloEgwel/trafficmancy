import cv2
import numpy as np
from random import randint

# Load the pre-trained MobileNet-SSD model and class labels
net = cv2.dnn.readNetFromCaffe(
    "MobileNetSSD_deploy.prototxt.txt", "MobileNetSSD_deploy.caffemodel"
)

THINGS_I_CARE_ABOUT = ["car", "person", "bicycle", "bus", "motorbike"]

# Class labels for MobileNet-SSD
CLASSES = [
    "background",
    "aeroplane",
    "bicycle",
    "bird",
    "boat",
    "bottle",
    "bus",
    "car",
    "cat",
    "chair",
    "cow",
    "diningtable",
    "dog",
    "horse",
    "motorbike",
    "person",
    "pottedplant",
    "sheep",
    "sofa",
    "train",
    "tvmonitor",
]


class TrafficCounter:

    def __init__(self):
        # Initialize webcam
        self.cap = cv2.VideoCapture(1)

    def count_traffic(self):
        counts = {thing: 0 for thing in THINGS_I_CARE_ABOUT}

        while True:
            ret, frame = self.cap.read()
            if not ret:
                continue

            # Resize the frame to 300x300 pixels (as expected by the model)
            resized_frame = cv2.resize(frame, (300, 300))

            # Create a blob from the frame
            blob = cv2.dnn.blobFromImage(resized_frame, 0.007843, (300, 300), 127.5)
            net.setInput(blob)

            # Perform object detection
            detections = net.forward()

            # Loop over the detections
            for j in range(detections.shape[2]):
                confidence = detections[0, 0, j, 2]

                # Filter out weak detections
                if confidence > 0.5:
                    idx = int(detections[0, 0, j, 1])
                    label = CLASSES[idx]

                    if label not in THINGS_I_CARE_ABOUT:
                        continue

                    # Calculate bounding box coordinates
                    box = detections[0, 0, j, 3:7] * np.array(
                        [frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]]
                    )
                    (startX, startY, endX, endY) = box.astype("int")

                    # Draw the bounding box and label on the frame
                    cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                    cv2.putText(
                        frame,
                        label,
                        (startX, startY - 15),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 255, 0),
                        2,
                    )

                    counts[label] += 1

            # Display the counts on the frame
            cv2.putText(
                frame,
                f'Cars: {counts["car"]}',
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 0, 0),
                2,
            )
            cv2.putText(
                frame,
                f'Pedestrians: {counts["person"]}',
                (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 0, 0),
                2,
            )
            cv2.putText(
                frame,
                f'Cyclists: {counts["bicycle"]}',
                (10, 110),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 0, 0),
                2,
            )

            # Display the resulting frame
            cv2.imwrite(f"img.jpg", frame)
            return counts

    def test():
        return {thing: randint(0, 15) for thing in THINGS_I_CARE_ABOUT}
