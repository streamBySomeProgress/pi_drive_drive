from picamera2 import Picamera2
import cv2
import logging
from log.logger import setup_logger
import os

# 로깅 설정
logging_info = setup_logger('sampling_collect', 'log_sampling_collect.txt', logging.INFO)

# 전역 변수
picam = Picamera2()
output_dir = "./camera/camera_data"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
else:
    os.removedirs(output_dir)
    os.makedirs(output_dir) # 사진 저장 디렉터리가 이미 존재할시 삭제 후 재생성

frame_count = 0  # 저장 파일명에 사용할 카운터(파일명 중복 방지)

# 학습용 이미지를 촬영하기 위한 영역 todo 동작 실행 도중에는 작동하지 않도록 호출 영역에서 조건문 작성
def camera_capture():
    picam.configure(picam.create_preview_configuration(main={"size": (640, 480)}))
    picam.start()
    frame = picam.capture_array() # 프레임 캡처 (480x640x3)
    cv2.imwrite(f"{output_dir}/frame_{frame_count}.jpg", frame)