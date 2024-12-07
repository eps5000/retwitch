from fastapi import APIRouter

router = APIRouter()

@router.get("/status", summary="Get current stream status")
def get_stream_status():
    # Mocked response for now
    return {
        "status": "not_live",  # or "live"
        "video_path": None,
        "start_time": None
    }
