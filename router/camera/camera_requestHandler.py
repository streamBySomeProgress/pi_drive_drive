from fastapi import APIRouter

camera_handler = APIRouter(prefix="/camera")

@camera_handler.get("/status")
async def status():
    """카메라 상태 확인"""
    return {"camera_running": camera_running}