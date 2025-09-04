class ConnectorBase:
    def __init__(self, user_id: str):
        self.user_id = user_id

    def connect(self):
        raise NotImplementedError

    def status(self) -> bool:
        raise NotImplementedError


# Exemplo Zoom
class ZoomConnector(ConnectorBase):
    connected_users = set()

    def connect(self):
        self.connected_users.add(self.user_id)
        return True

    def status(self) -> bool:
        return self.user_id in self.connected_users


# Você pode adicionar GoogleMeetConnector, TeamsConnector etc do mesmo jeito
