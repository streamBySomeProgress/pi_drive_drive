from flask import Flask, Response
import threading
import logging

app = Flask(__name__)

@app.route('/start', methods=['GET'])
def start_camera():
    """카메라 시작 엔드포인트"""
    global camera_running, thread
    if not camera_running:
        camera_running = True
        thread = threading.Thread(target=camera_loop)
        thread.start()
        logging.info("Camera started via HTTP")
        return Response("Camera started", status=200)
    return Response("Camera already running", status=400)

@app.route('/stop', methods=['GET'])
def stop_camera():
    """카메라 종료 엔드포인트"""
    global camera_running, thread
    if camera_running:
        camera_running = False
        thread.join()
        thread = None
        logging.info("Camera stopped via HTTP")
        return Response("Camera stopped", status=200)
    return Response("Camera not running", status=400)

@app.route('/')
def index():
    """기본 페이지"""
    return "Camera Control: Use /start or /stop"

if __name__ == '__main__':
    logging.info("Flask server starting...")
    app.run(host='0.0.0.0', port=5000, threaded=True)