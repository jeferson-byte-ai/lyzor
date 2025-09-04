from .base_connector import BaseConnector
import asyncio

class TeamSpeakConnector(BaseConnector):
    async def connect(self):
        print("Connecting to TeamSpeakConnector...")
        await asyncio.sleep(1)
        self.connected = True
        print("Connected to TeamSpeakConnector")

    async def disconnect(self):
        print("Disconnecting from TeamSpeakConnector...")
        await asyncio.sleep(1)
        self.connected = False
        print("Disconnected from TeamSpeakConnector")

    async def join_meeting(self, meeting_link: str):
        if not self.connected:
            await self.connect()
        print(f"Joining TeamSpeakConnector meeting: {meeting_link}")

    async def send_message(self, channel_id: str, message: str):
        if not self.connected:
            await self.connect()
        print(f"Sending message to TeamSpeakConnector channel {channel_id}: {message}")
