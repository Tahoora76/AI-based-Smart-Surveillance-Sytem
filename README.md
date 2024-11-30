# AI-based-Smart-Surveillance-Sytem
This project implements an intelligent surveillance system using YOLOv8 for object detection and Deep SORT for object tracking, aimed at enhancing security by identifying and tracking suspicious or harmful objects in real-time. The system leverages a webcam feed to continuously monitor and alert security teams when dangerous items such as weapons or other threatening objects are detected.

https://github.com/user-attachments/assets/1f9854ea-bcde-4d25-9591-1352cdd7a6c3

Features:
Real-time Object Detection: Uses YOLOv8, a state-of-the-art deep learning model, to detect objects in the video feed.
Object Tracking: Implements Deep SORT for accurate tracking of detected objects across frames.
Alert System: Sends alerts if harmful objects (e.g., guns, knives, etc.) are detected in the video stream.
Flask Web Interface: Provides a simple user interface to control the system, view live feed, and manage alerts.
Customizable: The system can be expanded to detect other objects, integrate with different cameras, and trigger custom alert actions.
Technologies Used:
Python: Main programming language used for developing the backend and logic.
YOLOv8: Pre-trained object detection model for accurate real-time detection.
Deep SORT: Algorithm for tracking detected objects across frames.
Flask: Python-based web framework to create a user interface for controlling the system.
OpenCV: For capturing webcam feed and processing video frames.
NumPy, Pandas: For handling data processing and manipulation.

