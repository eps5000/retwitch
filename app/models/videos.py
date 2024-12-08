import uuid
from datetime import datetime, timezone
from pydantic import BaseModel
from typing import List

class VideoRequest(BaseModel):
    name: str
    path: str
    size: int

class DeleteVideosRequest(BaseModel):
    video_ids: List[str]
    delete_file: bool = False  # Optional field

# Mock database for videos
video_store = {}

def add_video(name: str, path: str, size: int):
    """Add a video to the store."""
    video_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    video_store[video_id] = {
        "id": video_id,
        "name": name,
        "path": path,
        "size": size,
        "created_at": now,
        "metadata": {
            # Placeholder for future metadata (e.g., duration, resolution)
        },
    }
    return video_store[video_id]

def list_videos():
    """List all videos in the store."""
    return list(video_store.values())

def remove_video(video_id: str, delete_file: bool = False):
    """Remove a video from the store."""
    video = video_store.pop(video_id, None)
    if not video:
        return None
    if delete_file:
        import os
        try:
            os.remove(video["path"])
        except FileNotFoundError:
            pass
    return video

def get_video(video_id: str):
    """Retrieve a video by its ID."""
    return video_store.get(video_id)

# Initialize with sample data
if not video_store:
    add_video(name="Sample Video 1", path="/videos/sample1.mp4", size=1048576)
    add_video(name="Sample Video 2", path="/videos/sample2.mp4", size=2097152)
