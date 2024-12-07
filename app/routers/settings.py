from fastapi import APIRouter

router = APIRouter()

@router.get("/", summary="Settings endpoint placeholder")
def settings_root():
    return {"message": "Settings service is running"}
