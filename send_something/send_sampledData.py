from camera.sampling import Sampling_normal
import socket
import io
from PIL import Image
import os
from dotenv import load_dotenv

load_dotenv() # 환경변수 로드

# 서버 설정 (IP와 포트)
SERVER_IP = os.getenv('server_ip')
SERVER_PORT = os.getenv('server_port')

def send_sampledImage():
    try:
        # 카메라 초기화
        with Sampling_normal() as camera:
            camera.camera_on() # 활성화(내부적인 sleep 함수 호출로 인하여 약 2초 지연됨)

            # 이미지 캡처를 위한 스트림
            stream = io.BytesIO()

            # 이미지 캡처
            frame_array = camera.do()

            # NumPy 배열을 PIL 이미지로 변환
            image = Image.fromarray(frame_array)

            # BytesIO 스트림 초기화 및 JPEG로 저장
            stream.seek(0)
            stream.truncate()
            image.save(stream, format='JPEG')

            # 소켓 연결
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((SERVER_IP, SERVER_PORT)) # 라즈베리는 학습용 컴퓨터에 접속하는 client 로 간주할 수 있다

                image_data = stream.getvalue()
                size = len(image_data)
                client_socket.send(str(size).encode().ljust(16)) # 이미지 데이터 크기 전송
                client_socket.sendall(image_data) # 이미지 데이터 전송

                print(f"Image sent: {size} bytes")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        camera.camera_off()