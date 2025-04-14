from picamera2 import Picamera2
import cv2
from torchvision import transforms
import logging
from log.logger import setup_logger

# 로깅 설정
logging_info = setup_logger('sampling_eval', 'log_sampling.txt', logging.INFO)

# 카메라 인스턴스
picam = Picamera2()

# PyTorch 변환 설정
transform = transforms.ToTensor()

# 카메라 촬영(샘플링) 영역
def camera_sampling():
    """카메라 데이터, rgb 형식, 텐서 형식 반환"""
    picam.configure(picam.create_preview_configuration(main={"size": (640, 480)}))
    picam.start()

    frame = picam.capture_array() # 프레임 캡처 (480x640x3), (해당 영역에서 촬영)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # BGR -> RGB
    frame_tensor = transform(frame_rgb).unsqueeze(0) # tensor 로 변환, 0번째 차원에 1차원 요소 추가 [3, 480, 640] -> [1, 3, 480, 640]([배치 크기, rgb 채널 수, 해상도(480 * 640)])

    return frame, frame_rgb, frame_tensor