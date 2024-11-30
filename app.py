from flask import Flask, render_template, Response, request, redirect, url_for
import os
import cv2
import base64
from Detect_Track import DetectionAndTracking

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

video_source = 0
detector = DetectionAndTracking(video_source)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/live_video')
def live_video():
    return render_template('live_video.html')


@app.route('/video_feed')
def video_feed():
    def generate_frames():
        for frame_data in detector.process_video():
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')

    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/start_webcam', methods=['POST'])
def start_webcam():
    return redirect(url_for('live_video'))


@app.route('/upload_video', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return redirect(url_for('index'))

    video_file = request.files['video']
    video_path = os.path.join(UPLOAD_FOLDER, video_file.filename)
    video_file.save(video_path)

    detector = DetectionAndTracking(video_path)
    for _ in detector.process_video():
        pass

    return "Video processed successfully!"


@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return redirect(url_for('index'))

    image_file = request.files['image']
    if image_file.filename == '':
        return redirect(url_for('index'))

    image_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
    image_file.save(image_path)
    frame = cv2.imread(image_path)

    detector = DetectionAndTracking(image_path)  # Single-frame processing
    for frame_data in detector.process_video():
        processed_frame = cv2.imdecode(frame_data, cv2.IMREAD_COLOR)
        break

    _, buffer = cv2.imencode('.jpg', processed_frame)
    image_data = base64.b64encode(buffer).decode('utf-8')

    return render_template('display_image.html', image_data=image_data)


if __name__ == '__main__':
    app.run(debug=True)
