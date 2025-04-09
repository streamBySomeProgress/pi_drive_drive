import logging

# 기본 로거 설정 함수
def setup_logger(name, log_file, level=logging.INFO):
    # 포매터 설정 (로그 메시지의 형식)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # 파일 핸들러 생성
    file_handler = logging.FileHandler('./log/' + log_file) # log 디렉터리 이하
    file_handler.setFormatter(formatter)

    # 로거 생성
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(file_handler)
    return logger