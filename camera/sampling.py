from picamera2 import Picamera2
import cv2
from torchvision import transforms
import logging
from log.logger import setup_logger
import time

# 로깅 설정
logging_info = setup_logger('sampling_eval', 'log_sampling.txt', logging.INFO)

# PyTorch 변환 설정
transform = transforms.ToTensor()

picam = Picamera2()

# 기본적인 샘플링(촬영) 동작 수행 영역(카메라 초기화 영역 포함)
class Sampling_normal():
    """카메라 데이터, rgb 형식, 텐서 형식 반환"""
    def __init__(self, camera_isRunning = False):
        picam.configure(picam.create_preview_configuration(main={"size": (640, 480)})) # 640x480 은 선의 패턴을 인지하기에 충분
        if camera_isRunning:
            # 인스턴스 생성과 즉시 카메라를 활성화하고자 할 때
            picam.start()   # 센서 활성화
            time.sleep(2)  # 센서 안정화
            self.camera_isRunning = True # 동작 상태 변경
        else:
            self.camera_isRunning = False # 기본적으로는 camera_on 함수를 별도 호출하여야

    def __del__(self):
        # 인스턴스 소멸 시 정리 작업
        picam.stop()


    # 카메라 활성화
    def camera_on(self):
        if self.camera_isRunning:
            raise Exception('camera is already running')
        else:
            picam.start()   # 센서 활성화
            time.sleep(2)  # 센서 안정화
            self.camera_isRunning = True # 동작 상태 변경

    # 카메라 비활성화
    def camera_off(self):
        if not self.camera_isRunning:
            raise Exception('camera is already stopped')
        else:
            picam.stop()   # 센서 비활성화 (picamera2 리소스 정리)
            self.camera_isRunning = False # 동작 상태 변경

    # 실 촬영 동작
    def do(self):
        frame_array = picam.capture_array() # NumPy 배열(해당 영역에서 촬영)
        frame_rgb = cv2.cvtColor(frame_array, cv2.COLOR_BGR2RGB) # BGR -> RGB
        frame_tensor = transform(frame_rgb).unsqueeze(0) # tensor 로 변환, 0번째 차원에 1차원 요소 추가 [3, 480, 640] -> [1, 3, 480, 640]([배치 크기, rgb 채널 수, 해상도(480 * 640)])
        return frame_array, frame_rgb, frame_tensor
