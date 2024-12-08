from datetime import datetime, timezone
from pydantic import BaseModel

class StartStreamRequest(BaseModel):
    video_id: str


# Global variable to track the active stream
active_stream = None

def start_stream(video_id: str):
    """Start streaming a video."""
    global active_stream
    if active_stream:
        raise Exception("A stream is already active")
    active_stream = {
        "video_id": video_id,
        "start_time": datetime.now(timezone.utc),
    }
    return active_stream

def stop_stream():
    """Stop the current stream."""
    global active_stream
    if not active_stream:
        raise Exception("No active stream to stop")
    active_stream = None
    return {"detail": "Stream stopped successfully"}

def get_active_stream():
    """Retrieve the current stream state."""
    return active_stream
