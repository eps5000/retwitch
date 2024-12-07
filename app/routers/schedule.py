from fastapi import APIRouter

router = APIRouter()

@router.get("/", summary="Schedule management endpoint placeholder")
def schedule_root():
    return {"message": "Schedule management service is running"}
