from fastapi import HTTPException
from drive.drive_operate import startDrive, stopDrive
from fastapi import APIRouter
from fastapi.responses import JSONResponse
import logging
from log.logger import setup_logger

# 로깅 설정
logging_info = setup_logger('drive_requestHandler', 'log_drive_requestHandler.txt', logging.INFO)

drive_handler = APIRouter(prefix="/drive")


@drive_handler.post("/start")
async def drive_start():
    """주행 시작 요청 핸들러(앤드포인트)"""
    try:
        startDrive()
        logging_info.info("Driving is started via HTTP")
        return JSONResponse(
            status_code=200,
            content={"message": "Driving is started"}
        )
    except Exception as exception:
        return JSONResponse(
            status_code=400,
            content=exception
        )

@drive_handler.post("/stop")
async def drive_stop():
    """주행 종료 요청 핸들러(앤드포인트)"""
    try:
        stopDrive()
        logging_info.info("Driving is stopped via HTTP")
        return JSONResponse(
            status_code=200,
            content={"message": "Driving is stopped"}
        )
    except Exception as exception:
        return JSONResponse(
            status_code=400,
            content=exception
        )