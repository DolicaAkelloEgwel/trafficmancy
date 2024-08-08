import cv2
import time
import numpy as np
import ollama

# Load the pre-trained MobileNet-SSD model and class labels
net = cv2.dnn.readNetFromCaffe('MobileNetSSD_deploy.prototxt.txt', 'MobileNetSSD_deploy.caffemodel')

# Class labels for MobileNet-SSD
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]

TRAFFICMANCY_INITIAL_PROMPT = (
    "You are Trafficmany. You harness the power of urban movement to provide answers to life's burning questions. "
    "By analyzing the number of cars, cyclists, and pedestrians detected over a 10-second period, you interpret the flow of the city to deliver guidance. Here's how you work:\n\n"
    "1. Cars: Represent stability and progress. A higher count of cars means the path ahead is clear, suggesting forward momentum and determination in your answer.\n\n"
    "2. Cyclists: Symbolize agility and adaptability. When cyclists are in abundance, you advise flexibility and creative thinking as the keys to success.\n\n"
    "3. Pedestrians: Embody patience and human connection. More pedestrians indicate that collaboration or a thoughtful pause may be necessary for finding your answer.\n\n"
    "You use this urban pulse to provide nuanced and insightful responses, blending the dynamics of the street with the questions people ask. "
    "Whether it's a clear 'yes,' a thoughtful 'no,' or something in between, you guide the way based on the energy of the city around you."
)

# Initialize webcam
cap = cv2.VideoCapture(1)

# Record for 10 seconds
start_time = time.time()
while time.time() - start_time < 10:
    ret, frame = cap.read()
    if not ret:
        break

    # Resize the frame to 300x300 pixels (as expected by the model)
    resized_frame = cv2.resize(frame, (300, 300))

    # Create a blob from the frame
    blob = cv2.dnn.blobFromImage(resized_frame, 0.007843, (300, 300), 127.5)
    net.setInput(blob)

    # Perform object detection
    detections = net.forward()

    # Initialize counters
    car_count = 0
    pedestrian_count = 0
    cyclist_count = 0

    # Loop over the detections
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        # Filter out weak detections
        if confidence > 0.25:
            idx = int(detections[0, 0, i, 1])
            label = CLASSES[idx]

            # Calculate bounding box coordinates
            box = detections[0, 0, i, 3:7] * \
                np.array([frame.shape[1], frame.shape[0],
                          frame.shape[1], frame.shape[0]])
            (startX, startY, endX, endY) = box.astype("int")

            # Draw the bounding box and label on the frame
            cv2.rectangle(frame, (startX, startY), (endX, endY),
                          (0, 255, 0), 2)
            cv2.putText(frame, label, (startX, startY - 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Count cars, pedestrians, and cyclists
            if label == "car":
                car_count += 1
            elif label == "person":
                pedestrian_count += 1
            elif label == "bicycle":
                cyclist_count += 1

    # Display the counts on the frame
    cv2.putText(frame, f'Cars: {car_count}', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.putText(frame, f'Pedestrians: {pedestrian_count}', (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.putText(frame, f'Cyclists: {cyclist_count}', (10, 110),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    # Display the resulting frame
    cv2.imshow('Object Detection', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and destroy all OpenCV windows
cap.release()
cv2.destroyAllWindows()

query = input("What is your question? ")

response = ollama.chat(model='llama3.1', messages=[
  {
    'role': 'user',
    'content': f"{TRAFFICMANCY_INITIAL_PROMPT}. {car_count} cars, {pedestrian_count} pedestrians, and {cyclist_count} cyclists have just passed by. My question - {query}"
  },
])
print(response['message']['content'])
