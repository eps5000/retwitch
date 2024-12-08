import uuid
from datetime import datetime, timedelta, timezone

# Mock session store
session_store = {}

MAX_SESSION_LIFETIME = timedelta(hours=24)  # 24-hour maximum session lifetime

def create_or_update_session(token: str, username: str = None):
    """Create a new session or update the expiration of an existing one."""
    now = datetime.now(timezone.utc)
    if token in session_store:
        # Update the expiration time of the existing session
        session_store[token]["expires_at"] = now + timedelta(minutes=15)
    else:
        # Create a new session
        token = str(uuid.uuid4())
        session_store[token] = {
            "username": username,
            "created_at": now,
            "expires_at": now + timedelta(minutes=15)
        }
    return token, session_store[token]["expires_at"]

def get_session(token: str):
    session = session_store.get(token)
    if session and session["expires_at"] > datetime.now(timezone.utc):
        return session
    return None

def invalidate_session(token: str):
    if token in session_store:
        del session_store[token]

def is_session_expired(session):
    """Check if the session exceeds the maximum lifetime."""
    return datetime.now(timezone.utc) - session["created_at"] > MAX_SESSION_LIFETIME
