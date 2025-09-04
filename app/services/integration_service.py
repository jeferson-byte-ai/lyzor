from integrations.google_meet_connector import GoogleMeetConnector
from integrations.zoom_connector import ZoomConnector
from integrations.teams_connector import TeamsConnector
from integrations.webex_connector import WebexConnector
from integrations.bluejeans_connector import BlueJeansConnector
from integrations.gotomeeting_connector import GoToMeetingConnector
from integrations.slack_connector import SlackConnector
from integrations.skype_connector import SkypeConnector
from integrations.coursera_connector import CourseraConnector
from integrations.udemy_connector import UdemyConnector
from integrations.moodle_connector import MoodleConnector
from integrations.canvas_connector import CanvasConnector
from integrations.discord_connector import DiscordConnector
from integrations.teamspeak_connector import TeamSpeakConnector
from integrations.steam_connector import SteamConnector
from integrations.twitch_connector import TwitchConnector
from integrations.youtube_connector import YouTubeConnector
from integrations.facebook_gaming_connector import FacebookGamingConnector
from integrations.trovo_connector import TrovoConnector
from integrations.fortnite_connector import FortniteConnector
from integrations.valorant_connector import ValorantConnector
from integrations.lol_connector import LoLConnector
from integrations.gta_rp_connector import GTARPConnector
from integrations.vrchat_connector import VRChatConnector
from integrations.roblox_connector import RobloxConnector
from integrations.tinder_connector import TinderConnector
from integrations.badoo_connector import BadooConnector
from integrations.happn_connector import HappnConnector
from integrations.bumble_connector import BumbleConnector
from integrations.spotify_live_connector import SpotifyLiveConnector
from integrations.clubhouse_connector import ClubhouseConnector
from integrations.horizon_worlds_connector import HorizonWorldsConnector

CONNECTOR_MAP = {
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

class IntegrationService:
    def __init__(self):
        # Cada usuário tem um dicionário de conectores por plataforma
        self.user_connectors = {}

    def add_connector(self, user_id: str, platform: str, credentials: dict):
        connector_class = CONNECTOR_MAP.get(platform)
        if not connector_class:
            raise ValueError(f"Platform {platform} not supported")

        connector_instance = connector_class(**credentials)

        if user_id not in self.user_connectors:
            self.user_connectors[user_id] = {}

        self.user_connectors[user_id][platform] = connector_instance
        return connector_instance

    def get_connector(self, user_id: str, platform: str = None):
        user_platforms = self.user_connectors.get(user_id, {})
        if platform:
            return user_platforms.get(platform)
        return user_platforms  # retorna todos os conectores do usuário
