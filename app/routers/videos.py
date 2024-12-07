from fastapi import APIRouter

router = APIRouter()

@router.get("/", summary="Video management endpoint placeholder")
def videos_root():
    return {"message": "Video management service is running"}
