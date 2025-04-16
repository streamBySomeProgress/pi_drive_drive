from torchvision import transforms
import time
import logging
from log.logger import setup_logger
from global_path.global_path import model_path
from torchArea.eval.eval_to_drive import eval_to_drive
import threading
from camera.camera_common import Camera_common

# 로깅 설정
logging_info = setup_logger('eval_to_drive', 'log_eval_to_drive.txt', logging.INFO)

# 전역 변수
operating = False
global_model_path = model_path
thread = None

# PyTorch 변환 설정
transform = transforms.ToTensor()


# 실질적 주행 동작을 수행하는 영역
def drive_execute_operator():
    with Camera_common() as camera:
        logging_info.info("driving is just started")
        # while 이하부터 주행 동작 영역
        while operating:
            # 사진 데이터 할당
            frame_tensor = camera.capture_as_tensor()
            eval_to_drive(frame_tensor) # 모델을 기반으로 선의 방향을 반환하는 함수 todo 추후 실 주행 영역에 사용하기 위한 반환값 혹은 인자 생성 고려
            time.sleep(1)  # 처리 속도 조절 (1초마다 한번)
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