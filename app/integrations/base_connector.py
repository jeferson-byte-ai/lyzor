class BaseConnector:
    def __init__(self):
        self.connected = False

    async def connect(self):
        raise NotImplementedError

    async def disconnect(self):
        raise NotImplementedError

    async def join_meeting(self, meeting_link: str):
        raise NotImplementedError

    async def send_message(self, channel_id: str, message: str):
        raise NotImplementedError
