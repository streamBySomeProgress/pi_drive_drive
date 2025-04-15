from camera.sampling import Sampling_normal
import socket
import io
from PIL import Image

# 서버 설정 (Mac Mini의 IP와 포트) todo 환경변수 등으로 별도 관리
SERVER_IP = '192.168.1.100'  # Mac Mini의 IP 주소로 변경하세요
SERVER_PORT = 12345

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

                # 이미지 데이터 크기 전송
                image_data = stream.getvalue()
                size = len(image_data)
                client_socket.send(str(size).encode().ljust(16))

                # 이미지 데이터 전송
                client_socket.sendall(image_data)

                print(f"Image sent: {size} bytes")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        camera.camera_off()