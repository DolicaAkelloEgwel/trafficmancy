import blobconverter
import cv2
import numpy as np
import time
import depthai as dai

ROI_POSITION = 0.5

labelMap = [
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

TRACKING_LABELS = ["motorbike", "car", "bus", "person", "bicycle"]
RIGHT_COUNT = {label: 0 for label in TRACKING_LABELS}
LEFT_COUNT = {label: 0 for label in TRACKING_LABELS}
TRACKING_IDX = [labelMap.index(label) for label in TRACKING_LABELS]


def label_to_text(label: int) -> str:
    return labelMap.index(label)


model = blobconverter.from_zoo(name="mobilenet-ssd", shaves=6)

# Create pipeline
pipeline = dai.Pipeline()

# Define a neural network that will make predictions based on the source frames
nn = pipeline.create(dai.node.MobileNetDetectionNetwork)
nn.setConfidenceThreshold(0.5)
nn.setBlobPath(model)
nn.setNumInferenceThreads(2)
nn.input.setBlocking(False)

# Define a source for the neural network input
# Create color camera node.
cam = pipeline.create(dai.node.ColorCamera)
cam.setPreviewSize(300, 300)
cam.setInterleaved(False)
# Connect (link) the camera preview output to the neural network input
cam.preview.link(nn.input)

# Create XLinkOut object as conduit for passing camera frames to the host
xoutFrame = pipeline.create(dai.node.XLinkOut)
xoutFrame.setStreamName("outFrame")
cam.preview.link(xoutFrame.input)

# Create neural network output (inference) stream
nnOut = pipeline.create(dai.node.XLinkOut)
nnOut.setStreamName("nn")
nn.out.link(nnOut.input)

# Create and configure the object tracker
objectTracker = pipeline.create(dai.node.ObjectTracker)
objectTracker.setDetectionLabelsToTrack(TRACKING_IDX)  # track only person
# possible tracking types: ZERO_TERM_COLOR_HISTOGRAM, ZERO_TERM_IMAGELESS, SHORT_TERM_IMAGELESS, SHORT_TERM_KCF
objectTracker.setTrackerType(dai.TrackerType.ZERO_TERM_COLOR_HISTOGRAM)
# take the smallest ID when new object is tracked, possible options: SMALLEST_ID, UNIQUE_ID
objectTracker.setTrackerIdAssignmentPolicy(dai.TrackerIdAssignmentPolicy.SMALLEST_ID)

# Link detection networks outputs to the object tracker
nn.passthrough.link(objectTracker.inputTrackerFrame)
nn.passthrough.link(objectTracker.inputDetectionFrame)
nn.out.link(objectTracker.inputDetections)

# Send tracklets to the host
trackerOut = pipeline.create(dai.node.XLinkOut)
trackerOut.setStreamName("tracklets")
objectTracker.out.link(trackerOut.input)


# from https://www.pyimagesearch.com/2018/08/13/opencv-people-counter/
class TrackableObject:
    def __init__(self, objectID, centroid):
        # store the object ID, then initialize a list of centroids
        # using the current centroid
        self.objectID = objectID
        self.centroids = [centroid]

        # initialize a boolean used to indicate if the object has
        # already been counted or not
        self.counted = False


# Pipeline defined, now the device is connected to
with dai.Device(pipeline) as device:

    # Define queues for image frames

    # Output queue for retrieving camera frames from device
    qOut_Frame = device.getOutputQueue(name="outFrame", maxSize=4, blocking=False)

    qDet = device.getOutputQueue(name="nn", maxSize=4, blocking=False)
    tracklets = device.getOutputQueue("tracklets", 4, False)

    def should_run():
        return True

    def get_frame():
        in_Frame = qOut_Frame.get()
        frame = in_Frame.getCvFrame()
        return True, frame

    startTime = time.monotonic()
    detections = []
    frame_count = 0
    counter = [0, 0, 0, 0]  # left, right, up, down

    trackableObjects = {}

    def to_planar(arr: np.ndarray, shape: tuple) -> np.ndarray:
        return cv2.resize(arr, shape).transpose(2, 0, 1).flatten()

    while should_run():
        # Get image frames from camera or video file
        read_correctly, frame = get_frame()
        if not read_correctly:
            break

        in_Frame = qOut_Frame.tryGet()

        if in_Frame is not None:
            frame = in_Frame.getCvFrame()
            cv2.putText(
                frame,
                "NN fps: {:.2f}".format(frame_count / (time.monotonic() - startTime)),
                (2, frame.shape[0] - 4),
                cv2.FONT_HERSHEY_TRIPLEX,
                0.4,
                color=(255, 255, 255),
            )

        inDet = qDet.tryGet()
        if inDet is not None:
            detections = inDet.detections
            frame_count += 1

        track = tracklets.tryGet()

        if frame is not None:
            height = frame.shape[0]
            width = frame.shape[1]

            if track:
                trackletsData = track.tracklets
                for t in trackletsData:
                    to = trackableObjects.get(t.id, None)

                    # calculate centroid
                    roi = t.roi.denormalize(width, height)
                    x1 = int(roi.topLeft().x)
                    y1 = int(roi.topLeft().y)
                    x2 = int(roi.bottomRight().x)
                    y2 = int(roi.bottomRight().y)
                    centroid = (int((x2 - x1) / 2 + x1), int((y2 - y1) / 2 + y1))

                    # If new tracklet, save its centroid
                    if t.status == dai.Tracklet.TrackingStatus.NEW:
                        to = TrackableObject(t.id, centroid)
                    elif to is not None:
                        if not to.counted:
                            x = [c[0] for c in to.centroids]
                            direction = centroid[0] - np.mean(x)

                            if (
                                centroid[0] > ROI_POSITION * width
                                and direction > 0
                                and np.mean(x) < ROI_POSITION * width
                            ):  # right to left
                                counter[1] += 1
                                to.counted = True

                                RIGHT_COUNT[label_to_text(t.label)] += 1

                            elif (
                                centroid[0] < ROI_POSITION * width
                                and direction < 0
                                and np.mean(x) > ROI_POSITION * width
                            ):
                                counter[0] += 1
                                to.counted = True

                                LEFT_COUNT[label_to_text(t.label)] += 1

                        to.centroids.append(centroid)

                    trackableObjects[t.id] = to  # right to left

                    if (
                        t.status != dai.Tracklet.TrackingStatus.LOST
                        and t.status != dai.Tracklet.TrackingStatus.REMOVED
                    ):
                        text = "ID {}".format(t.id)
                        cv2.putText(
                            frame,
                            text,
                            (centroid[0] - 10, centroid[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            (255, 255, 255),
                            2,
                        )
                        cv2.circle(
                            frame, (centroid[0], centroid[1]), 4, (255, 255, 255), -1
                        )

            # Draw ROI line
            cv2.line(
                frame,
                (int(ROI_POSITION * width), 0),
                (int(ROI_POSITION * width), height),
                (0xFF, 0, 0),
                5,
            )

            # display count and status
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(
                frame,
                f"Left: {counter[0]}; Right: {counter[1]}",
                (10, 35),
                font,
                0.8,
                (0, 0xFF, 0xFF),
                2,
                cv2.FONT_HERSHEY_SIMPLEX,
            )

            cv2.imshow("cumulative_object_counting", frame)
            if cv2.waitKey(25) & 0xFF == ord("q"):
                break

    cv2.destroyAllWindows()
