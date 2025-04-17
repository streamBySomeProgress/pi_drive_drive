from fastapi import APIRouter
from fastapi.responses import JSONResponse
from send_something.send_sampledData import send_sampledImage
import logging
from log.logger import setup_logger
import requests

logging_info = setup_logger('camera_requestHandler', 'log_camera_requestHandler.txt', logging.INFO)

camera_handler = APIRouter(prefix="/camera")

@camera_handler.post("/capture")
async def camera_capture(class_label: int):
    """라즈베리 파이의 카메라를 이용하여 사진 한장을 촬영한 후 학습 영역으로 전송"""
    try:
        send_sampledImage(class_label)
        return JSONResponse(
            status_code=200,
            content={"message": "img is captured and sent"}
        )
    except requests.RequestException as requestException:
        return JSONResponse(
            status_code=500,
            content=requestException
        )
    except Exception as exception:
        return JSONResponse(
            status_code=500,
            content=exception
        )