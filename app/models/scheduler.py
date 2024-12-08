import uuid
from pydantic import BaseModel
from datetime import datetime, timezone
from typing import List

class ScheduledStreamRequest(BaseModel):
    video_id: str
    start_time: datetime
    end_time: datetime

# Mock database for scheduled streams
scheduled_streams = {}

class ScheduledStream:
    def __init__(self, video_id: str, start_time: datetime, end_time: datetime):
        self.id = str(uuid.uuid4())
        self.video_id = video_id
        self.start_time = start_time
        self.end_time = end_time
        self.created_at = datetime.now(timezone.utc)


def add_scheduled_stream(video_id: str, start_time: datetime, end_time: datetime):
    """Add a scheduled stream."""
    if start_time.tzinfo is None:
        start_time = start_time.replace(tzinfo=timezone.utc)  # Assume naive times are UTC
    if end_time.tzinfo is None:
        end_time = end_time.replace(tzinfo=timezone.utc)  # Ensure end_time is also UTC

    stream = ScheduledStream(video_id, start_time, end_time)
    scheduled_streams[stream.id] = stream
    return stream

def list_scheduled_streams():
    """List all scheduled streams."""
    return [
        {
            "id": stream.id,
            "video_id": stream.video_id,
            "start_time": stream.start_time.isoformat(),
            "created_at": stream.created_at.isoformat(),
        }
        for stream in scheduled_streams.values()
    ]

def remove_scheduled_stream(stream_id: str):
    """Remove a scheduled stream by ID."""
    return scheduled_streams.pop(stream_id, None)
