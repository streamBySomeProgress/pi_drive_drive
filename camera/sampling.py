from picamera2 import Picamera2
import cv2
import torch
from torchvision import transforms
import time
import logging
import os
from log.logger import setup_logger
from torchArea.cnn import simpleCnn

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

model = simpleCnn.SimpleCNN()
model.eval()  # 평가 모드 (학습이 아닌 추론용)

def camera_loop():
    """카메라 데이터를 처리하는 루프"""
    global camera_running, frame_count
    if not camera_running:
        camera_running = True
        picam.configure(picam.create_preview_configuration(main={"size": (640, 480)}))
        picam.start()

        frame_count = 0
        while camera_running:
            frame = picam.capture_array()                    # 프레임 캡처 (480x640x3)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_tensor = transform(frame_rgb).unsqueeze(0) # 0번째 차원에 1차원 요소 추가 [3, 480, 640] -> [1, 3, 480, 640]

            # 모델 예측
            with torch.no_grad():                            # 기울기 계산 비활성화
                output = model(frame_tensor)                 # [1, 3] 출력
                prediction = torch.argmax(output).item()     # 최대값 인덱스 (0, 1, 2)

                print(output)

            logging_info.info(f"Frame {frame_count}: Prediction = {prediction}")
            cv2.imwrite(f"{output_dir}/frame_{frame_count}.jpg", frame)
            frame_count += 1
            time.sleep(2)  # 처리 속도 조절 (2초마다 한번)

def camera_loop_abort():
    """카메라 데이터 처리 동작 중단 영역"""
    global camera_running
    camera_running = False # 전역 변수를 변경함으로서 while 반복문 중단
    picam.stop()
    logging_info.info("Camera stopped")