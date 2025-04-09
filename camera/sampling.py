from picamera2 import Picamera2
import cv2
from torchvision import transforms
import time
import logging
import os
from log.logger import setup_logger

# 로깅 설정
logging_info = setup_logger('sampling', 'log_sampling.txt', logging.INFO)

# 전역 변수
picam = Picamera2()
output_dir = "./camera/camera_data"
camera_running = False
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# PyTorch 변환 설정
transform = transforms.ToTensor()

def camera_loop():
    """카메라 데이터를 처리하는 루프"""
    global camera_running
    if not camera_running:
        camera_running = True
        picam.configure(picam.create_preview_configuration(main={"size": (640, 480)}))
        picam.start()
        frame_count = 0
        # 중단을 희망할 시 camera_loop_abort 호출할 것
        while camera_running:
            frame = picam.capture_array()
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_tensor = transform(frame_rgb)
            print(frame_tensor)

            # 간단한 분석: 평균 밝기 계산
            brightness = frame_tensor.mean().item()
            logging_info.info(f"Frame {frame_count}: Average brightness = {brightness:.3f}")

            # 프레임 저장
            cv2.imwrite(f"{output_dir}/frame_{frame_count}.jpg", frame)
            frame_count += 1
            time.sleep(2)  # 처리 속도 조절 (2초마다 한번)

def camera_loop_abort():
    """카메라 데이터 처리 동작 중단 영역"""
    global camera_running
    camera_running = False
    picam.stop()
    logging_info.info("Camera stopped")