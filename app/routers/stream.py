from fastapi import APIRouter, HTTPException
from app.models.stream import start_stream, stop_stream, get_active_stream, StartStreamRequest

router = APIRouter()

@router.post("/start", summary="Start a new stream")
def start(request: StartStreamRequest):
    try:
        stream = start_stream(request.video_id)
        return {
            "detail": "Stream started successfully",
            "video_id": stream["video_id"],
            "start_time": stream["start_time"].isoformat(),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/stop", summary="Stop the current stream")
def stop():
    try:
        return stop_stream()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("", summary="Get the current stream status")
def status():
    stream = get_active_stream()
    if not stream:
        return {"detail": "No active stream"}
    return {
        "video_id": stream["video_id"],
        "start_time": stream["start_time"].isoformat(),
    }
