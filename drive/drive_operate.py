import torch
from torchvision import transforms
import time
import logging
from log.logger import setup_logger
from torchArea.cnn.lineCnn import LineCNN
from global_path.global_path import model_path
from torchArea.eval.eval_to_drive import eval_to_drive
import threading

# 로깅 설정
logging_info = setup_logger('eval_to_drive', 'log_eval_to_drive.txt', logging.INFO)

# 전역 변수
operating = False
global_model_path = model_path
thread = None

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

# 실질적 주행 동작을 수행하는 영역
def drive_execute_operator():
    logging_info.info("driving is just started")
    while operating:
        # while 이하부터 주행 동작 영역
        eval_to_drive()
        time.sleep(1)  # 처리 속도 조절 (1초마다 한번)

    # 반복문 종료 -> 주행 동작 중지됨(operating = False)
    logging_info.info("driving is stopped")

# 주행 시작 요청
def startDrive():
    global operating, thread
    if not operating:
        operating = True
        thread = threading.Thread(target=drive_execute_operator)
        thread.start()
    else:
        raise Exception('driving is already being done')

# 주행 중단 요청
def stopDrive():
    global operating, thread
    if operating:
        operating = False # 전역 변수를 변경함으로서 while 반복문 중단
        thread.join() # drive_execute_operator 를 실행하는 스레드가 중단될 때까지 대기
        thread = None # 할당 해제
    else:
        raise Exception('driving has already been stopped')