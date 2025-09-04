from .base_connector import BaseConnector
import asyncio

class HappnConnector(BaseConnector):
    async def connect(self):
        print("Connecting to HappnConnector...")
        await asyncio.sleep(1)
        self.connected = True
        print("Connected to HappnConnector")

    async def disconnect(self):
        print("Disconnecting from HappnConnector...")
        await asyncio.sleep(1)
        self.connected = False
        print("Disconnected from HappnConnector")

    async def join_meeting(self, meeting_link: str):
        if not self.connected:
            await self.connect()
        print(f"Joining HappnConnector meeting: {meeting_link}")

    async def send_message(self, channel_id: str, message: str):
        if not self.connected:
            await self.connect()
        print(f"Sending message to HappnConnector channel {channel_id}: {message}")
