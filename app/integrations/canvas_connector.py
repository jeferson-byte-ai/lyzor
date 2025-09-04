from .base_connector import BaseConnector
import asyncio

class CanvasConnector(BaseConnector):
    async def connect(self):
        print("Connecting to CanvasConnector...")
        await asyncio.sleep(1)
        self.connected = True
        print("Connected to CanvasConnector")

    async def disconnect(self):
        print("Disconnecting from CanvasConnector...")
        await asyncio.sleep(1)
        self.connected = False
        print("Disconnected from CanvasConnector")

    async def join_meeting(self, meeting_link: str):
        if not self.connected:
            await self.connect()
        print(f"Joining CanvasConnector meeting: {meeting_link}")

    async def send_message(self, channel_id: str, message: str):
        if not self.connected:
            await self.connect()
        print(f"Sending message to CanvasConnector channel {channel_id}: {message}")
