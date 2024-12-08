from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.models.videos import add_video, list_videos, remove_video, VideoRequest, DeleteVideosRequest

router = APIRouter()

@router.get("", summary="List all videos")
def get_videos(verbose: bool = False):
    videos = list_videos()
    if not verbose:
        return [{"id": v["id"], "name": v["name"], "path": v["path"]} for v in videos]
    return videos

@router.post("", summary="Add a new video")
def upload_video(video: VideoRequest):
    # Add the video to the store
    video_data = add_video(name=video.name, path=video.path, size=video.size)
    return video_data

@router.delete("", summary="Remove one or more videos")
def delete_videos(request: DeleteVideosRequest):
    results = {"success": [], "failure": []}
    for video_id in request.video_ids:
        video = remove_video(video_id, delete_file=request.delete_file)
        if video:
            results["success"].append(video_id)
        else:
            results["failure"].append(video_id)

    if not results["success"]:
        raise HTTPException(status_code=404, detail="No videos were deleted")

    return {
        "detail": "Deletion completed",
        "success": results["success"],
        "failure": results["failure"],
    }