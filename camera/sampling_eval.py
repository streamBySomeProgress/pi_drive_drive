from picamera2 import Picamera2
import cv2
import torch
from torchvision import transforms
import time
import logging
from log.logger import setup_logger
from torchArea.cnn.lineCnn import LineCNN

# 로깅 설정
logging_info = setup_logger('sampling_eval', 'log_sampling_eval.txt', logging.INFO)

# 전역 변수
picam = Picamera2()
camera_running = False
model_path = 'model.pth'

# PyTorch 변환 설정
transform = transforms.ToTensor()

# 모델 초기화 및 가중치 로드
model = LineCNN()
try:
    model.load_state_dict(torch.load(model_path)) # 모델을 불러옴
    logging.info("Loaded trained model from model.pth")
except FileNotFoundError:
    logging.info("No trained model found, using random weights")

model.eval() # 평가 모드 (학습이 아닌 추론용)

# 실 주행을 위한 연속 촬영
def camera_loop():
    """카메라 데이터를 CNN으로 처리 (이미지 저장 없음)"""
    global camera_running, frame_count
    if not camera_running:
        camera_running = True
        picam.configure(picam.create_preview_configuration(main={"size": (640, 480)}))
        picam.start()

        frame_count = 0
        while camera_running:
            frame = picam.capture_array() # 프레임 캡처 (480x640x3), (해당 영역에서 촬영)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # BGR -> RGB
            frame_tensor = transform(frame_rgb).unsqueeze(0) # tensor 로 변환, 0번째 차원에 1차원 요소 추가 [3, 480, 640] -> [1, 3, 480, 640]([배치 크기, rgb 채널 수, 해상도(480 * 640)])

            # CNN으로 예측
            with torch.no_grad():
                output = model(frame_tensor) # [1, 6] -> [batch_size, 출력 클래스 수]
                # 예: tensor([[0.2, -1.5, 3.7, 0.1, 2.3, -0.9]])
                prediction = torch.argmax(output).item() # 최종 예측은 가장 높은 점수의 인덱스를 선택(예: index 2(right))

            # 결과 로깅
            position_map = {
                0: "Left",
                1: "Center",
                2: "Right",
                3: "None", # 선 없음
                4: "Left Curve",
                5: "Right Curve"
            }
            logging_info.info(f"Frame {frame_count}: Prediction = {prediction} ({position_map[prediction]})")

            frame_count += 1
            time.sleep(2)  # 처리 속도 조절 (2초마다 한번)

# 실 주행을 위한 연속 촬영을 중단하는 영역
def camera_loop_abort():
    """카메라 데이터 처리 동작 중단 영역"""
    global camera_running
    camera_running = False # 전역 변수를 변경함으로서 while 반복문 중단
    picam.stop()
    logging_info.info("Camera stopped")