# pi_drive_drive
라즈베리 파이를 사용한 주행 로직을 작성하는 영역

가상환경 활성: source venv/bin/activate

비활성화: deactive

패키지 목록 최신화: pip freeze > requirements.txt

목록에 있는 패키지 일괄 설치: pip install -r requirements.txt

## 유의사항

1. pi_drive_training 에서 학습된 모델을 받아서 본 영역에서 실 테스트 진행


## .env 파일(프로젝트 최상단 위치) 에 별도 작성해야 할 변수
1. training_server_ip -> 학습을 수행하는 컴퓨터(pi_drive_training 프로젝트가 구동중인)의 ip주소
2. training_server_port
3. port
