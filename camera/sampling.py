from picamera2 import Picamera2
import cv2
from torchvision import transforms
import time
import logging
import os

# 로깅 설정
logging.basicConfig(filename='camera.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

# 전역 변수
picam = Picamera2()
output_dir = "camera_data"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# PyTorch 변환 설정
transform = transforms.ToTensor()

def camera_loop(camera_running):
    """카메라 데이터를 처리하는 루프"""
    picam.configure(picam.create_preview_configuration(main={"size": (640, 480)}))
    picam.start()

    frame_count = 0
    while camera_running:
        frame = picam.capture_array()
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_tensor = transform(frame_rgb)
        print(frame_tensor)

        # 간단한 분석: 평균 밝기 계산
        brightness = frame_tensor.mean().item()
        logging.info(f"Frame {frame_count}: Average brightness = {brightness:.3f}")

        # 프레임 저장
        cv2.imwrite(f"{output_dir}/frame_{frame_count}.jpg", frame)
        frame_count += 1
        time.sleep(1)  # 처리 속도 조절

    picam.stop()
    logging.info("Camera stopped")