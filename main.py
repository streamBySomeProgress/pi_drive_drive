from fastapi import FastAPI
import logging
from log.logger import setup_logger
from router.drive.drive_requestHandler import drive_handler
from router.camera.camera_requestHandler import camera_handler
from router.model.model_requestHandler import model_handler
import uvicorn
from dotenv import load_dotenv
import os

app = FastAPI()

load_dotenv() # 환경변수 로드

# 본 서버 설정 (포트)
PORT = int(os.getenv('port'))

# 로깅 설정
logging_info = setup_logger('main', 'log_main.txt', logging.INFO)

app.include_router(drive_handler)
app.include_router(camera_handler)
app.include_router(model_handler)

if __name__ == "__main__":
    logging_info.info("FastAPI server starting the pi_drive_drive...")
    uvicorn.run(app, host="0.0.0.0", port=PORT)