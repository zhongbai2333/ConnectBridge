from zhongbais_data_api import zbDataAPI

from connect_bridge.context import GlobalContext
from connect_bridge.constants import PLUGIN_ID

class PlayerInfo(object):
    def __init__(self) -> None:
        self.config = GlobalContext.get_config()
        self.control = GlobalContext.get_control()

        zbDataAPI.register_player_list_callback(self.player_list_change)

    def player_list_change(self, player_name: str, player_list: list) -> None:
        GlobalContext.get_player_list().update(player_list)
        self.control.send_data("all", PLUGIN_ID, {"type": 4, "player_name": player_name, "player_list": player_list})
