from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
from datetime import datetime
from app.models.stream import start_stream
from app.models.scheduler import scheduled_streams, ScheduledStream

# Configure APScheduler
scheduler = BackgroundScheduler(
    jobstores={"default": MemoryJobStore()},
    executors={"default": ThreadPoolExecutor(10)},
    timezone="UTC",
)

scheduler.start()

def schedule_stream_execution(stream_id: str, video_id: str, start_time: datetime, end_time: datetime):
    """Schedule a job to start the stream, ensuring no overlaps."""
    # Check for overlapping schedules
    for stream in scheduled_streams.values():
        existing_start = stream.start_time
        existing_end = stream.end_time

        if existing_end >= start_time and existing_start <= end_time:
            raise Exception(
                f"Cannot schedule stream: overlaps with existing stream "
                f"({existing_start} to {existing_end})"
            )

    # Proceed with scheduling
    def trigger_stream():
        """Trigger the stream using the start_stream logic."""
        try:
            start_stream(video_id)
        except Exception as e:
            print(f"Failed to start stream {video_id}: {e}")

    scheduler.add_job(
        func=trigger_stream,
        trigger="date",
        run_date=start_time,
        id=stream_id,
        replace_existing=True,
    )

    # Add the scheduled stream
    scheduled_streams[stream_id] = ScheduledStream(video_id, start_time, end_time)
