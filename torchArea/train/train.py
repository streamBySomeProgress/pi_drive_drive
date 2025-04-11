import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from PIL import Image
from torchvision import transforms
import os  # 누락된 os 임포트 추가
from torchArea.cnn.lineCnn import LineCNN
from global_path.global_camera_path import camera_data_path
from global_path.global_model_path import model_path


global_model_path = model_path()

# 데이터셋 정의
class LineDataset(Dataset):
    def __init__(self, label_file, img_dir):
        self.img_labels = [(line.split()[0], int(line.split()[1])) for line in open(label_file)]
        self.img_dir = img_dir
        self.transform = transforms.Compose([
            transforms.Resize((480, 640)),
            transforms.ToTensor(),
            transforms.Normalize((0.5,), (0.5,))
        ])

    def __len__(self):
        return len(self.img_labels)

    def __getitem__(self, idx):
        img_path, label = self.img_labels[idx]
        image = Image.open(os.path.join(self.img_dir, img_path)).convert("RGB")
        image = self.transform(image)
        return image, label

# 모델 훈련 함수 todo 추후 훈련 동작이 필요한 곳에서 사용
def TrainModel():
    # 데이터셋 및 로더
    dataset = LineDataset("labels.txt", camera_data_path())
    loader = DataLoader(dataset, batch_size=4, shuffle=True)

    # 모델, 손실 함수, 최적화
    model = LineCNN()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # 학습 루프
    for epoch in range(10):
        running_loss = 0.0
        for images, labels in loader:
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        print(f"Epoch {epoch+1}, Loss: {running_loss / len(loader)}")

    if not os.path.exists(global_model_path):
        # 기존 모델 삭제
        os.remove(global_model_path)
    # 모델 저장
    torch.save(model.state_dict(), global_model_path) # 파일 형식으로 저장됨
    print("Model saved as model.pth")