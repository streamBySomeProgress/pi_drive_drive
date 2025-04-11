import torch
import torch.nn as nn

# CNN 모델 정의
class LineCNN(nn.Module):
    def __init__(self):
        super(LineCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 16, 3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, 3, padding=1)
        self.pool = nn.MaxPool2d(2, 2) # 풀링(pooling)으로 특징 맵 크기 축소
        self.fc1 = nn.Linear(32 * 120 * 160, 6)  # 6개 클래스
        self.dropout = nn.Dropout(0.5)

    # 프레임워크에 의하여 굳이 명시하지 않더라도 backward 동작 또한 수행됨
    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x))) # 풀링 과정 (480x640 → 120x160)
        x = self.pool(torch.relu(self.conv2(x))) # 풀링 과정 (480x640 → 120x160)
        x = x.view(-1, 32 * 120 * 160) # 평탄화(텐서를 1차원 벡터로 변환 (614400 요소))
        x = self.dropout(x)
        x = self.fc1(x)
        return x