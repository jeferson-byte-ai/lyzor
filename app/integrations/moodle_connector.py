from .base_connector import BaseConnector
import asyncio

class MoodleConnector(BaseConnector):
    async def connect(self):
        print("Connecting to MoodleConnector...")
        await asyncio.sleep(1)
        self.connected = True
        print("Connected to MoodleConnector")

    async def disconnect(self):
        print("Disconnecting from MoodleConnector...")
        await asyncio.sleep(1)
        self.connected = False
        print("Disconnected from MoodleConnector")

    async def join_meeting(self, meeting_link: str):
        if not self.connected:
            await self.connect()
        print(f"Joining MoodleConnector meeting: {meeting_link}")

    async def send_message(self, channel_id: str, message: str):
        if not self.connected:
            await self.connect()
        print(f"Sending message to MoodleConnector channel {channel_id}: {message}")
