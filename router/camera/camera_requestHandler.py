from fastapi import APIRouter

camera_handler = APIRouter(prefix="/camera")

@camera_handler.get("/capture")
async def capture():
    """라즈베리 파이의 카메라를 이용하여 사진 한장을 촬영한 후 """
    return {"camera_running": camera_running}