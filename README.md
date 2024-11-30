# AI-based-Smart-Surveillance-Sytem
This project implements an intelligent surveillance system using YOLOv8 for object detection and Deep SORT for object tracking, aimed at enhancing security by identifying and tracking suspicious or harmful objects in real-time. The system leverages a webcam feed to continuously monitor and alert security teams when dangerous items such as weapons or other threatening objects are detected.

https://github.com/user-attachments/assets/1f9854ea-bcde-4d25-9591-1352cdd7a6c3

## Download Models & DeepSORT folder

- [YOLOv8 Model](https://drive.google.com/file/d/1blTgoGuVcJmmfhWlYgvEq5uGePmTZ3dH/view?usp=sharing)
- [DeepSORT Model](https://drive.google.com/file/d/1IPC-ppaLETfAYh7k8HDMs50PUPtCFi_y/view?usp=sharing)
- [DeepSORT Files](https://drive.google.com/drive/folders/17-Ak9zUE1cK0oZI-r7_JHK4B60GdlLu9?usp=sharing)

## Requirements

To set up the project and install the necessary dependencies, create a virtual environment and install the following packages:

1. Clone the repository:
   ```bash
   git clone https://github.com/Tahoora76/AI-based-Smart-Surveillance-Sytem.git
   cd AI-based-Smart-Surveillance-Sytem



### Features:

- **Real-time Object Detection:** Uses YOLOv8 for accurate detection.  
- **Object Tracking:** Implements Deep SORT for tracking.  
- **Alert System:** Sends alerts for harmful objects.  
- **Web Interface:** Built with Flask for user control.  

### Technologies Used:

- **Python**: Main programming language.  
- **YOLOv8**: Object detection model.  
- **Deep SORT**: Tracking algorithm.  
- **Flask**: Python framework for the web interface.  
Usage:
Start Webcam: Begins the live video feed from the webcam.
Stop Stream: Stops the video feed and tracking.
Alert System: Automatically triggers alerts based on harmful object detection.

Future Improvements:
Integrate with cloud storage for saving video footage.
Implement facial recognition for additional security.
Expand object detection capabilities to include more harmful items.
Provide multi-camera support and centralized monitoring.
