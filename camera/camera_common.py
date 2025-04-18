from picamera2 import Picamera2
import cv2
from torchvision import transforms
import logging
from log.logger import setup_logger
import time

# 로깅 설정
logging_info = setup_logger('camera_common', 'log_camera_common.txt', logging.INFO)

# PyTorch 변환 설정
transform = transforms.ToTensor()


# 본 클래스는 context manager 형식으로 구현됨(이를 통하여 카메라 자원이 누수되는 일이 없도록 함)
class Camera_common(Picamera2):
    """카메라 데이터, rgb 형식, 텐서 형식 반환"""
    def __init__(self):
        super().__init__() # Picamera2 인스턴스 생성
        self.configure(self.create_preview_configuration(main={"size": (640, 480)})) # 640x480 은 선의 패턴을 인지하기에 충분
        logging_info.info('Camera_common instance is initialized')

    def __del__(self):
        # 인스턴스 소멸 시 정리 작업(리소스 해제 포함)
        self.close()
        logging_info.info('Camera_common instance is destroyed')

    def __enter__(self):
        # context 시작 시 카메라 ON
        logging_info.info('Camera_common instance is entered as context manager')
        self.start()   # 센서 활성화
        time.sleep(2)  # 센서 안정화
        return self # picamera 인스턴스 요소들 또한 사용 가능

    def __exit__(self, exc_type, exc_value, traceback):
        # context 종료 시 카메라 OFF
        logging_info.info('Camera_common instance is exited as context manager')
        self.close()   # 카메라 종료 (picamera2 리소스 정리)

    def capture_as_rgb(self):
        logging_info.info('Camera_common instance captured img as rgb')
        frame_array = self.capture_array() # NumPy 배열(해당 영역에서 촬영)
        frame_rgb = cv2.cvtColor(frame_array, cv2.COLOR_BGR2RGB) # BGR -> RGB
        return frame_rgb

    def capture_as_tensor(self):
        logging_info.info('Camera_common instance captured img as tensor')
        frame_array = self.capture_array() # NumPy 배열(해당 영역에서 촬영)
        frame_rgb = cv2.cvtColor(frame_array, cv2.COLOR_BGR2RGB) # BGR -> RGB
        frame_tensor = transform(frame_rgb).unsqueeze(0) # tensor 로 변환, 0번째 차원에 1차원 요소 추가 [3, 480, 640] -> [1, 3, 480, 640]([배치 크기, rgb 채널 수, 해상도(480 * 640)])
        return frame_tensor
