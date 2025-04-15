from fastapi import HTTPException
from drive.drive_operate import startDrive, stopDrive
from fastapi import APIRouter
import logging
from log.logger import setup_logger

# 로깅 설정
logging_info = setup_logger('main', 'log_drive_requestHandler.txt', logging.INFO)

drive_handler = APIRouter(prefix="/drive")


@drive_handler.get("/start")
async def drive_start():
    """주행 시작 요청 핸들러(앤드포인트)"""
    try:
        startDrive()
        logging_info.info("Driving is started via HTTP")
        return {"message": "Driving is started"}
    except Exception as exception:
        raise HTTPException(status_code=400, detail=exception)

@drive_handler.get("/stop")
async def drive_stop():
    """주행 종료 요청 핸들러(앤드포인트)"""
    try:
        stopDrive()
        logging_info.info("Driving is stopped via HTTP")
        return {"message": "Driving is stopped"}
    except Exception as exception:
        raise HTTPException(status_code=400, detail=exception)