import cv2
import torch
from ultralytics import YOLO
from deep_sort_pytorch.deep_sort import DeepSort
from twilio.rest import Client

# Twilio credentials
TWILIO_ACCOUNT_SID = "xxxxxxxxxxxxx"
TWILIO_AUTH_TOKEN = "xxxxxxxxxx"
TWILIO_PHONE_NUMBER = "xxxxxxxxxx"
ALERT_PHONE_NUMBER = "xxxxxxxxxx"

# Initialize Twilio client
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


class DetectionAndTracking:
    def __init__(self, video_source):

        self.model1 = YOLO("models/yolov8n.pt")
        self.model2 = YOLO("models/yolov8_harmful_object_detection.pt")

        self.target_classes_model1 = ["person", "bicycle", "car", "motorbike", "knife", "pistol"]
        self.target_classes_model2 = ["knife", "pistol"]

        self.class_indices_model1 = [idx for idx, name in self.model1.names.items() if
                                     name in self.target_classes_model1]
        self.class_indices_model2 = [idx for idx, name in self.model2.names.items() if
                                     name in self.target_classes_model2]

        self.deep_sort = DeepSort(model_path="models/ckpt.t7", max_age=30, n_init=3, max_iou_distance=0.7,
                                  use_cuda=True)

        self.cap = cv2.VideoCapture(video_source)

    def process_video(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("End of video or error reading frame.")
                break

            results1 = self.model1.predict(frame, classes=self.class_indices_model1)
            results2 = self.model2.predict(frame, classes=self.class_indices_model2)

            # Prepare detections
            detections = []
            confidences = []
            classes = []

            for box in results1[0].boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = float(box.conf[0])
                if confidence < 0.5:
                    continue
                class_id = int(box.cls[0])

                detections.append([x1, y1, x2, y2])
                confidences.append(confidence)
                classes.append(class_id)

                label = f"{self.model1.names[class_id]} {confidence:.2f}"
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

            for box in results2[0].boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = float(box.conf[0])
                if confidence < 0.5:
                    continue
                class_id = int(box.cls[0])

                detections.append([x1, y1, x2, y2])
                confidences.append(confidence)
                classes.append(class_id)

                # Draw detections on frame
                label = f"{self.model2.names[class_id]} {confidence:.2f}"
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                if detections in self.target_classes_model2:
                    alert_message = f"ALERT: {detections.upper()} detected!"
                    try:
                        twilio_client.messages.create(
                            body=alert_message,
                            from_=TWILIO_PHONE_NUMBER,
                            to=ALERT_PHONE_NUMBER
                        )
                        print(f"Alert sent: {alert_message}")
                    except Exception as e:
                        print(f"Error sending alert: {e}")

            detections = torch.tensor(detections) if detections else torch.empty((0, 4))

            tracks = self.deep_sort.update(detections, confidences, classes, frame)

            for track in tracks:
                if hasattr(track, "track_id") and hasattr(track, "to_tlbr"):
                    track_id = track.track_id
                    bbox = track.to_tlbr()


                    cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (0, 255, 255), 2)
                    cv2.putText(frame, f"ID: {track_id}", (int(bbox[0]), int(bbox[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                0.5,
                                (0, 255, 255), 2)


            _, buffer = cv2.imencode('.jpg', frame)
            yield buffer.tobytes()
