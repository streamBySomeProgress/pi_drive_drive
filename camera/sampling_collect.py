from picamera2 import Picamera2
import cv2
import logging
from log.logger import setup_logger
from torchvision import transforms
import os
import torch
from torchArea.cnn.lineCnn import LineCNN
from global_path.global_camera_path import camera_data_path

# 로깅 설정
logging_info = setup_logger('sampling_collect', 'log_sampling_collect.txt', logging.INFO)

# Picamera2 인스턴스
picam = Picamera2()

# PyTorch 변환 설정
transform = transforms.ToTensor()

# 모델 초기화
model = LineCNN()

output_dir = camera_data_path() # 해당 디렉토리 이하의 클래스별 디렉토리에 이미지가 저장됨
labels_file = os.path.join(output_dir, "labels.txt") # 라벨링 파일 경로(이미지를 클래스별로 라벨링)

if not os.path.exists(output_dir):
    # 신규 생성
    os.makedirs(output_dir)

# 학습용 이미지를 촬영하기 위한 영역 todo 동작 실행 도중에는 작동하지 않도록 호출 영역에서 조건문 작성
# 인자 -> class_label((방향)클래스의 라벨 값), output_dir(이미지 데이터가 저장되는 각각의 클래스 디렉터리들이 저장되는 상위 디렉터리 경로)
def camera_capture(class_label: int = None):
    if class_label is None:
        raise Exception('class_label is None')  # 인자 부재

    if not 0 <= class_label <= 5:
        raise Exception('class_label is not valid value') # 부적절 인자

    picam.configure(picam.create_preview_configuration(main={"size": (640, 480)}))
    picam.start()

    # 프레임 캡처(480x640x3)
    frame = picam.capture_array()
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_tensor = transform(frame_rgb).unsqueeze(0)

    # 클래스별 디렉토리 생성 및 저장
    class_dir = os.path.join(output_dir, f"class_{class_label}")
    if not os.path.exists(class_dir):
        os.makedirs(class_dir)

    class_dir_list = os.listdir(class_dir) # 클래스별 디렉토리의 파일 목록
    filename = f"frame_{len(class_dir_list)}.jpg" # 파일 구분자는 해당 클래스의 파일 목록의 길이
    filepath = os.path.join(class_dir, filename)

    # 이미지 생성
    cv2.imwrite(filepath, frame)

    # labels.txt에 기록 (상대 경로 사용)
    rel_filepath = os.path.relpath(filepath, output_dir)
    with open(labels_file, "a") as f:
        # 이미지를 클래스별로 라벨링
        f.write(f"{rel_filepath} {class_label}\n") # 예: class_0/frame_0.jpg 0

    # CNN 예측 todo capture 동작 내에서 예측 동작을 수행하고자 할 경우 일정 이상의 샘플 데이터가 축적된 뒤에 가능, 조건문 사용하여 학습된 데이터양에 따라 실행 여부가 결정되도록 할 것
    with torch.no_grad():
        output = model(frame_tensor)
        prediction = torch.argmax(output).item()

    position_map = {0: "Left", 1: "Center", 2: "Right", 3: "None", 4: "Left Curve", 5: "Right Curve"}
    logging.info(f"Captured frame saved as {filepath}: Prediction = {prediction} ({position_map[prediction]})") # 학습이 제대로 이루어졌을 경우 class_label 에 해당하는 prediction 값이 반환되어야

    return filepath, prediction
