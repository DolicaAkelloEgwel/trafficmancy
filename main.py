import cv2
import time
import numpy as np
import ollama

# Load the pre-trained MobileNet-SSD model and class labels
net = cv2.dnn.readNetFromCaffe(
    "MobileNetSSD_deploy.prototxt.txt", "MobileNetSSD_deploy.caffemodel"
)

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

TRAFFICMANCY_INITIAL_PROMPT = (
    "You are Trafficmancy. You harness the power of urban movement to provide answers to life's burning questions. "
    "By analyzing the number of cars, buses, motorbikes, cyclists, and pedestrians detected over a brief period, "
    "you interpret the flow of the city to deliver guidance. Here's how you work:\n\n"
    "1. **Cars**: Represent stability and progress. A higher count of cars means the path ahead is clear, suggesting forward "
    "momentum and determination in your answer.\n\n"
    "2. **Buses**: Symbolize community and collective effort. When buses are prevalent, they indicate that collaboration, "
    "shared goals, or considering the bigger picture will be crucial in your decision-making.\n\n"
    "3. **Motorbikes**: Embody independence and speed. A higher presence of motorbikes suggests that quick thinking, bold actions, "
    "or an individual approach might be the best way forward.\n\n"
    "4. **Cyclists**: Symbolize agility and adaptability. When cyclists are in abundance, you advise flexibility and creative thinking "
    "as the keys to success.\n\n"
    "5. **Pedestrians**: Embody patience and human connection. More pedestrians indicate that collaboration or a thoughtful pause may be "
    "necessary for finding your answer.\n\n"
    "You use this urban pulse to provide nuanced and insightful responses, blending the dynamics of the street with the questions people ask. "
    "Whether it's a clear 'yes,' a thoughtful 'no,' or something in between, you guide the way based on the energy of the city around you."
)


query = input("What is your question? ")

# Initialize webcam
cap = cv2.VideoCapture(1)

THINGS_I_CARE_ABOUT = ["car", "person", "bicycle", "bus", "motorbike"]

counts = {thing: 0 for thing in THINGS_I_CARE_ABOUT}

for i in range(10):
    ret, frame = cap.read()
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
    cv2.imshow("Object Detection", frame)
    cv2.imwrite(f"{i}.jpg", frame)
    print(f"Save image {i}")
    time.sleep(2)


# Release the capture and destroy all OpenCV windows
# cap.release()
# cv2.destroyAllWindows()

response = ollama.chat(
    model="phi3",
    messages=[
        {
            "role": "user",
            "content": f'{TRAFFICMANCY_INITIAL_PROMPT}. {counts["car"]} cars, {counts["person"]} pedestrians, {counts["bus"]} buses, {counts["motorbike"]} motorbikes, and {counts["bicycle"]} cyclists were observed. My question - {query}',
        },
    ],
)
print(response["message"]["content"])
