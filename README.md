# pi_drive
라즈베리 파이를 사용한 주행 로직 및 이를 위한 학습 로직을 작성하는 영역

가상환경 활성: source venv/bin/activate

비활성화: deactive

패키지 목록 최신화: pip freeze > requirements.txt

목록에 있는 패키지 일괄 설치: pip install -r requirements.txt

## 유의사항

1. 학습해야 할 클래스는 총 6개(Left, Center, Right, None, Left Curve, Right Curve)
2. 클래스당 최소 20~30장의 사진이 필요하며 각 클래스당 사진의 개수는 비슷하게 유지할 것(클래스당 최소 20개의 사진이 존재하지 않을 경우 샘플링 이외 동작을 수행하지 않음)
3. 카메라 데이터까지 git 에 push 하여 라즈베리가 아닌 상대적으로 성능이 우월한 컴퓨터(맥) 에서 모델 생성 진행하기
