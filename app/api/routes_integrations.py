from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse

# Import all connectors
from app.integrations.google_meet_connector import GoogleMeetConnector
from app.integrations.zoom_connector import ZoomConnector
from app.integrations.teams_connector import TeamsConnector
from app.integrations.webex_connector import WebexConnector
from app.integrations.bluejeans_connector import BlueJeansConnector
from app.integrations.gotomeeting_connector import GoToMeetingConnector
from app.integrations.slack_connector import SlackConnector
from app.integrations.skype_connector import SkypeConnector
from app.integrations.coursera_connector import CourseraConnector
from app.integrations.udemy_connector import UdemyConnector
from app.integrations.moodle_connector import MoodleConnector
from app.integrations.canvas_connector import CanvasConnector
from app.integrations.discord_connector import DiscordConnector
from app.integrations.teamspeak_connector import TeamSpeakConnector
from app.integrations.steam_connector import SteamConnector
from app.integrations.twitch_connector import TwitchConnector
from app.integrations.youtube_connector import YouTubeConnector
from app.integrations.facebook_gaming_connector import FacebookGamingConnector
from app.integrations.trovo_connector import TrovoConnector
from app.integrations.fortnite_connector import FortniteConnector
from app.integrations.valorant_connector import ValorantConnector
from app.integrations.lol_connector import LoLConnector
from app.integrations.gta_rp_connector import GTARPConnector
from app.integrations.vrchat_connector import VRChatConnector
from app.integrations.roblox_connector import RobloxConnector
from app.integrations.tinder_connector import TinderConnector
from app.integrations.badoo_connector import BadooConnector
from app.integrations.happn_connector import HappnConnector
from app.integrations.bumble_connector import BumbleConnector
from app.integrations.spotify_live_connector import SpotifyLiveConnector
from app.integrations.clubhouse_connector import ClubhouseConnector
from app.integrations.horizon_worlds_connector import HorizonWorldsConnector


router = APIRouter()

# Store user connectors
user_connectors = {}

# Mapping platform names to connector classes
connector_map = {
    "google_meet": GoogleMeetConnector,
    "zoom": ZoomConnector,
    "teams": TeamsConnector,
    "webex": WebexConnector,
    "bluejeans": BlueJeansConnector,
    "gotomeeting": GoToMeetingConnector,
    "slack": SlackConnector,
    "skype": SkypeConnector,
    "coursera": CourseraConnector,
    "udemy": UdemyConnector,
    "moodle": MoodleConnector,
    "canvas": CanvasConnector,
    "discord": DiscordConnector,
    "teamspeak": TeamSpeakConnector,
    "steam": SteamConnector,
    "twitch": TwitchConnector,
    "youtube": YouTubeConnector,
    "facebook_gaming": FacebookGamingConnector,
    "trovo": TrovoConnector,
    "fortnite": FortniteConnector,
    "valorant": ValorantConnector,
    "lol": LoLConnector,
    "gta_rp": GTARPConnector,
    "vrchat": VRChatConnector,
    "roblox": RobloxConnector,
    "tinder": TinderConnector,
    "badoo": BadooConnector,
    "happn": HappnConnector,
    "bumble": BumbleConnector,
    "spotify_live": SpotifyLiveConnector,
    "clubhouse": ClubhouseConnector,
    "horizon_worlds": HorizonWorldsConnector
}

@router.post("/integration/connect")
async def connect_platform(user_id: str = Form(...), platform: str = Form(...)):
    platform_key = platform.lower()
    if platform_key not in connector_map:
        return JSONResponse({"message": "Platform not supported."}, status_code=400)

    if user_id not in user_connectors:
        user_connectors[user_id] = {}

    if platform_key in user_connectors[user_id]:
        return JSONResponse({"message": f"{platform} already connected."}, status_code=400)

    connector_instance = connector_map[platform_key]()
    await connector_instance.connect()
    user_connectors[user_id][platform_key] = connector_instance

    return {"message": f"{platform} connected for user {user_id}"}

@router.post("/integration/disconnect")
async def disconnect_platform(user_id: str = Form(...), platform: str = Form(...)):
    platform_key = platform.lower()
    if user_id not in user_connectors or platform_key not in user_connectors[user_id]:
        return JSONResponse({"message": f"{platform} not connected."}, status_code=404)

    connector_instance = user_connectors[user_id][platform_key]
    await connector_instance.disconnect()
    del user_connectors[user_id][platform_key]

    return {"message": f"{platform} disconnected for user {user_id}"}

@router.post("/integration/join_meeting")
async def join_meeting(user_id: str = Form(...), platform: str = Form(...), meeting_link: str = Form(...)):
    platform_key = platform.lower()
    if user_id not in user_connectors or platform_key not in user_connectors[user_id]:
        return JSONResponse({"message": f"{platform} not connected."}, status_code=404)

    connector_instance = user_connectors[user_id][platform_key]
    await connector_instance.join_meeting(meeting_link)
    return {"message": f"Joined meeting on {platform}"}

@router.post("/integration/send_message")
async def send_message(user_id: str = Form(...), platform: str = Form(...), channel_id: str = Form(...), message: str = Form(...)):
    platform_key = platform.lower()
    if user_id not in user_connectors or platform_key not in user_connectors[user_id]:
        return JSONResponse({"message": f"{platform} not connected."}, status_code=404)

    connector_instance = user_connectors[user_id][platform_key]
    await connector_instance.send_message(channel_id, message)
    return {"message": f"Message sent to {platform} channel {channel_id}"}
