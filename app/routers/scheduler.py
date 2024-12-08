from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from app.models.scheduler import add_scheduled_stream, list_scheduled_streams, remove_scheduled_stream, ScheduledStreamRequest, scheduled_streams
from app.services.scheduler import schedule_stream_execution

router = APIRouter()

@router.get("", summary="List all scheduled streams")
def get_scheduled_streams():
    return list_scheduled_streams()

@router.post("", summary="Schedule a new stream")
def schedule_stream(request: ScheduledStreamRequest):
    # Add the stream to the database
    stream = add_scheduled_stream(request.video_id, request.start_time, request.end_time)

    # Schedule the stream execution
    try:
        schedule_stream_execution(stream.id, stream.video_id, stream.start_time, stream.end_time)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "id": stream.id,
        "video_id": stream.video_id,
        "start_time": stream.start_time.isoformat(),
        "end_time": stream.end_time.isoformat(),
        "created_at": stream.created_at.isoformat(),
    }

@router.delete("/{stream_id}", summary="Remove a scheduled stream")
def delete_scheduled_stream(stream_id: str):
    stream = remove_scheduled_stream(stream_id)
    if not stream:
        raise HTTPException(status_code=404, detail="Stream not found")
    return {"detail": "Scheduled stream removed successfully"}
