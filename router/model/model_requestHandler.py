from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import logging
from log.logger import setup_logger
import tempfile
from global_path.global_path import model_path
import os
import torch
import shutil


logging_info = setup_logger('model_requestHandler', 'log_model_requestHandler.txt', logging.INFO)

model_handler = APIRouter(prefix="/model")

@model_handler.post("/replace")
async def camera_capture(file: UploadFile = File(...)):
    """
        학습 영역에서 생성한 새 모델을 받아 기존 모델을 대체
        todo training 영역에서 모델 생성 성공하면 전송 시도해보기, 성공한 이후 본 todo 주석 삭제
    """
    try:
        # 파일 확장자 검증
        if not file.filename.endswith(".pth"):
            raise HTTPException(status_code=400, detail="The file must have a .pth extension")

        # 임시 파일 생성 및 업로드된 파일 저장(접미사는 "pth" 로 정의)
        with tempfile.NamedTemporaryFile(suffix=".pth") as temp_file:
            # 업로드된 파일을 임시 파일에 저장
            with open(temp_file.name, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer) # 첫번째 인자의 파일 객체를 두번째 인자(임시 파일 객체)에 copy

            # .pth 파일 로드
            try:
                state_dict = torch.load(temp_file.name, map_location=torch.device("cpu"))
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"this is not valid .pth extension file: {str(e)}")

            # 기존 모델 존재할 시 삭제
            if os.path.exists(model_path):
                os.remove(model_path)
                logging_info('previous model file is deleted')

            # 새로운 .pth 파일로 저장
            with open(model_path, "wb") as f:
                torch.save(state_dict, f)
                logging_info('new model file is saved')

        return JSONResponse(
            status_code=200,
            content={"message": f"the model file {file.filename} is saved successfully.", "path": model_path}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": f"failed: {str(e)}"}
        )
    finally:
        file.file.close()  # UploadFile 객체 닫기