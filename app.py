from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

live_video_url = 0
graph_url = 0

def generate_frames(video_url):
    # Open the webcam
    cap = cv2.VideoCapture(video_url)  # Change the parameter to the appropriate camera index if needed

    while True:
        # Read frame from the camera
        success, frame = cap.read()

        if not success:
            break

        # Convert the frame to JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)

        if not ret:
            break

        # Yield the output frame in the byte format
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    # Release the camera and close the window
    cap.release()

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/live_cam')
def video_feed():
    return Response(generate_frames(live_video_url), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/graph')
def plot_graph():
    return Response(generate_frames(graph_url), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)


