from typing import TYPE_CHECKING
from connect_bridge.constants import PLUGIN_ID

if TYPE_CHECKING:
    from connect_core.api.interface import PluginControlInterface
    from mcdreforged.api.types import PluginServerInterface


class PraseMsg(object):

    def __init__(
        self, mcdr: "PluginServerInterface", connectcore: "PluginControlInterface"
    ):
        self._mcdr_server = mcdr
        self._control_interface = connectcore
        self.server_info = {}

    def prase_msg(self, server_id: str, msg: dict):
        # 解析消息并存储到 server_info 字典中
        match msg["type"]:
            case -1:
                self._control_interface.error(
                    f"An Error Occurred From {server_id}: {msg['error']}"
                )
            case 0:
                if (
                    msg["server_name"]
                    == self._control_interface.get_config()["server_name"]
                ):
                    self._control_interface.send_data(
                        server_id,
                        PLUGIN_ID,
                        {"type": -1, "error": "Duplicate Server Name! 重复的服务器名称！"},
                    )
                self.server_info[server_id] = msg["server_name"]
            case 1:
                self._mcdr_server.broadcast(
                    f"§7[{self.server_info[server_id]}][{msg["player_name"]}] {msg["msg"]}"
                )
            case _:
                pass
