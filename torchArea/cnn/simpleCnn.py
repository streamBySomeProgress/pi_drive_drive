import torch
import torch.nn as nn

class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 16, 3, padding=1)  # 입력 채널 3, 출력 채널 16, 커널 크기 3x3
        self.pool = nn.MaxPool2d(2, 2)               # 2x2 풀링
        self.fc1 = nn.Linear(16 * 240 * 320, 3)      # 완전 연결층, 출력 3 (좌, 우, 직진)

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))     # 합성곱 -> ReLU -> 풀링
        x = x.view(-1, 16 * 240 * 320)               # 평탄화
        x = self.fc1(x)                              # 완전 연결층
        return x