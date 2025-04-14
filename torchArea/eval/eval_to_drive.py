import torch
from torchvision import transforms
import logging
from log.logger import setup_logger
from torchArea.cnn.lineCnn import LineCNN
from global_path.global_path import model_path
from camera.sampling import camera_sampling
from map.line_position_map import position_map

# 로깅 설정
logging_info = setup_logger('eval_to_drive', 'log_eval_to_drive.txt', logging.INFO)

# 전역 변수
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

# 실 주행을 위한 샘플링 이미지 평가, 최종 예측 산출 todo 현재는 학습을 통하여 선을 인식하는지만 관찰하므로 해당 함수의 반환값을 별도 명시하지는 않음, 추후 필요할 시 생성
def eval_to_drive():
    """카메라 데이터를 CNN으로 처리 (이미지 저장 없음)"""

    # 사진 데이터 할당
    frame, frame_rgb, frame_tensor = camera_sampling() # todo 라즈베리 파이를 통하여 촬영한 사진 이외의 다른 사진도 활용할수 있도록 하기(모델 테스트용), camera_sampling 을 손보거나 새로운 함수를 생성하는 걸 고려

    # CNN으로 예측
    with torch.no_grad():
        output = model(frame_tensor) # [1, 6] -> [batch_size, 출력 클래스 수]
        # 예: tensor([[0.2, -1.5, 3.7, 0.1, 2.3, -0.9]])
        prediction = torch.argmax(output).item() # 최종 예측은 가장 높은 점수의 인덱스를 선택(예: index 2(right))

    # 결과 로깅
    logging_info.info(f"Prediction = {prediction} ({position_map[prediction]})")