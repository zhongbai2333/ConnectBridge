from typing import TYPE_CHECKING
from connect_bridge.constants import PLUGIN_ID

if TYPE_CHECKING:
    from connect_core.api.interface import PluginControlInterface
    from mcdreforged.api.types import PluginServerInterface


class PraseMsg(object):

    def __init__(
        self, connectcore: "PluginControlInterface"
    ):
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
                self._control_interface.send_data(
                    server_id,
                    PLUGIN_ID,
                    {"type": 2, "server_name": self._control_interface.get_config()["server_name"]},
                )
            case 1:
                self._control_interface.mcdr.broadcast(
                    f"§7[{self.server_info[server_id]}][{msg["player_name"]}] {msg["msg"]}"
                )
            case 2:
                if (
                    msg["server_name"]
                    == self._control_interface.get_config()["server_name"]
                ):
                    self._control_interface.send_data(
                        server_id,
                        PLUGIN_ID,
                        {
                            "type": -1,
                            "error": "Duplicate Server Name! 重复的服务器名称！",
                        },
                    )
                self.server_info[server_id] = msg["server_name"]
            case 3:
                self.server_info.pop(server_id , None)
            case _:
                pass
    
    def del_server(self, server_list: list) -> None:
        """删除服务器信息"""
        for i in set(self.server_info.keys()) - set(server_list):
            self.server_info.pop(i , None)
