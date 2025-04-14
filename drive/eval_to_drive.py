import torch
from torchvision import transforms
import time
import logging
from log.logger import setup_logger
from torchArea.cnn.lineCnn import LineCNN
from global_path.global_path import model_path
from camera.sampling import camera_sampling
from map.line_position_map import position_map

# 로깅 설정
logging_info = setup_logger('eval_to_drive', 'log_eval_to_drive.txt', logging.INFO)

# 전역 변수
operating = False
global_model_path = model_path

# PyTorch 변환 설정
transform = transforms.ToTensor()

# 모델 초기화 및 가중치 로드
model = LineCNN()
try:
    model.load_state_dict(torch.load(global_model_path)) # 모델을 불러옴
    logging.info("Loaded trained model from model.pth")
except FileNotFoundError:
    logging.info("No trained model found, using random weights")

model.eval() # 평가 모드 (학습이 아닌 추론용)

# 실 주행을 위한 연속적인 샘플링 이미지 검증
def eval_to_drive():
    """카메라 데이터를 CNN으로 처리 (이미지 저장 없음)"""
    global operating, frame_count
    if not operating:
        operating = True

        logging_info.info("driving is just started")

        frame_count = 0
        while operating:
            frame, frame_rgb, frame_tensor = camera_sampling()

            # todo cnn 동작 코드 분리
            # CNN으로 예측
            with torch.no_grad():
                output = model(frame_tensor) # [1, 6] -> [batch_size, 출력 클래스 수]
                # 예: tensor([[0.2, -1.5, 3.7, 0.1, 2.3, -0.9]])
                prediction = torch.argmax(output).item() # 최종 예측은 가장 높은 점수의 인덱스를 선택(예: index 2(right))

            # 결과 로깅
            logging_info.info(f"Frame {frame_count}: Prediction = {prediction} ({position_map[prediction]})")

            frame_count += 1
            time.sleep(2)  # 처리 속도 조절 (2초마다 한번)
        else:
            raise Exception('driving is already being done')

# 실 주행을 위한 연속적인 샘플링 이미지 검증 중단
def eval_to_drive_abort():
    """샘플링 이미지 검증 반복 중단 영역"""
    global operating
    if operating:
        operating = False # 전역 변수를 변경함으로서 while 반복문 중단
        #picam.stop()
        logging_info.info("driving is stopped")
    else:
        raise Exception('driving has already been stopped')