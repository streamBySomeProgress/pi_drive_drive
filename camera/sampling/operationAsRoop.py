from flask import Flask, Response
from picamera2 import Picamera2
import cv2
import torch
from torchvision import transforms
import threading
import time
import logging
import os

app = Flask(__name__)

# 로깅 설정
logging.basicConfig(filename='camera.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

# 전역 변수
picam = Picamera2()
camera_running = False
thread = None
output_dir = "camera_data"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# PyTorch 변환 설정
transform = transforms.ToTensor()

def camera_loop():
    """카메라 데이터를 처리하는 루프"""
    global camera_running
    picam.configure(picam.create_preview_configuration(main={"size": (640, 480)}))
    picam.start()

    frame_count = 0
    while camera_running:
        frame = picam.capture_array()
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_tensor = transform(frame_rgb)

        # 간단한 분석: 평균 밝기 계산
        brightness = frame_tensor.mean().item()
        logging.info(f"Frame {frame_count}: Average brightness = {brightness:.3f}")

        # 프레임 저장 (선택적)
        cv2.imwrite(f"{output_dir}/frame_{frame_count}.jpg", frame)
        frame_count += 1
        time.sleep(0.1)  # 처리 속도 조절

    picam.stop()
    logging.info("Camera stopped")