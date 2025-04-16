from camera.camera_common import Camera_common
import requests
import io
from PIL import Image
import os
from dotenv import load_dotenv

load_dotenv() # 환경변수 로드

# 서버 설정 (IP와 포트)
SERVER_IP = os.getenv('server_ip')
SERVER_PORT = os.getenv('server_port')

# 라벨링을 위한 값을 인자로 받아야
def send_sampledImage(class_label: int):
    # 카메라 초기화
    with Camera_common() as camera:
        # 이미지 캡처를 위한 스트림
        stream = io.BytesIO()

        # 이미지 캡처
        frame_array = camera.capture_array()

        # NumPy 배열을 PIL 이미지로 변환
        image = Image.fromarray(frame_array)

        # 이미지 형식이 RGB임을 보장
        if not image.mode == 'RGB':
            image = image.convert('RGB')

        # JPEG로 저장
        image.save(stream, format='JPEG')
        stream.seek(0) # 파일을 읽기 위하여 기준점을 맨 앞으로 이동

        # HTTP POST 요청(이미지 및 해당하는 라벨링 값 전송)
        print(f"http://{SERVER_IP}:{SERVER_PORT}/upload/image")
        response = requests.post(
            f"http://{SERVER_IP}:{SERVER_PORT}/upload/image",
            files={'image': ('image.jpg', stream, 'image/jpeg')},
            data={'class_label': str(class_label)}  # int를 문자열로 변환
        )
        if response.status_code == 200:
            print(f"Image sent successfully: {response.json()}")
        else:
            raise requests.RequestException(f"Error: {response.status_code}, {response.text}") # 전송 실패 관련 예외