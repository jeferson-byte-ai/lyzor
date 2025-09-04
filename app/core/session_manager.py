import asyncio
from .meeting_session import MeetingSession

class SessionManager:
    def __init__(self):
        self.sessions = {}
        self.lock = asyncio.Lock()

    async def start_session(self, session_id):
        async with self.lock:
            if session_id in self.sessions:
                raise ValueError("Session already exists")
            session = MeetingSession()
            self.sessions[session_id] = session
            return session

    async def stop_session(self, session_id):
        async with self.lock:
            session = self.sessions.pop(session_id, None)
            if session:
                # Cleanup if needed
                pass

    def get_session(self, session_id):
        return self.sessions.get(session_id, None)
