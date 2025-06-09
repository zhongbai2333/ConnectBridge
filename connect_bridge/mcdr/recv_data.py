from typing import TYPE_CHECKING, Any, Callable, Dict
from connect_bridge.constants import PLUGIN_ID

from connect_bridge.context import GlobalContext


class MessageParser:
    """
    负责解析来自其它服务器的消息，并维护 server_id → server_name 的映射。
    """

    def __init__(self):
        self._control = GlobalContext.get_control()
        self._config = GlobalContext.get_config()
        # 存储各 server_id 对应的 server_name
        self._server_names: Dict[str, str] = {}

        # 消息类型到处理方法的映射
        self._handlers: Dict[int, Callable[[str, Dict[str, Any]], None]] = {
            -1: self._handle_error,
            0: self._handle_register,
            2: self._handle_register,
            1: self._handle_chat,
            3: self._handle_disconnect,
            4: self._handle_player_list,
        }

    def parse_msg(self, server_id: str, msg: Dict[str, Any]) -> None:
        """
        根据 msg["type"] 分发到不同的处理方法。
        """
        msg_type = msg.get("type")
        handler = self._handlers.get(msg_type, self._handle_default)
        handler(server_id, msg)

    def _handle_error(self, server_id: str, msg: Dict[str, Any]) -> None:
        error_text = msg.get("error", "")
        self._control.error(f"An Error Occurred From {server_id}: {error_text}")

    def _handle_register(self, server_id: str, msg: Dict[str, Any]) -> None:
        """
        处理类型 0（注册请求）和类型 2（注册回应）：
         - 检查是否重复名称，若重复则回报错
         - 存储 server_name
         - 对于类型 0，还要回复类型 2，将本地 server_name 发回
        """
        incoming_name = msg.get("server_name", "")
        local_name = self._config.server_name

        # 重名检查
        if incoming_name == local_name:
            self._send_error(server_id, "Duplicate Server Name! 重复的服务器名称！")
            return

        # 更新映射
        self._server_names[server_id] = incoming_name

        # 如果是类型 0，需要回复类型 2
        if msg["type"] == 0:
            self._control.send_data(
                server_id,
                PLUGIN_ID,
                {"type": 2, "server_name": local_name},
            )

    def _handle_chat(self, server_id: str, msg: Dict[str, Any]) -> None:
        """
        处理类型 1：从其它服务器收到玩家聊天消息，广播到本服。
        """
        server_name = self._server_names.get(server_id, "Unknown")
        player = msg.get("player_name", "")
        text = msg.get("msg", "")
        self._control.mcdr.broadcast(f"§7[{server_name}][{player}] {text}")

    def _handle_disconnect(self, server_id: str, msg: Dict[str, Any]) -> None:
        """
        处理类型 3：对端服务器断开，清理映射。
        """
        self._server_names.pop(server_id, None)

    def _handle_player_list(self, server_id: str, msg: Dict[str, Any]) -> None:
        """
        处理类型 4：玩家列表更新。
        """
        player_list = msg.get("player_list", [])
        GlobalContext.get_player_list().update(player_list)

    def _handle_default(self, server_id: str, msg: Dict[str, Any]) -> None:
        # 未知类型，忽略或记录日志
        pass

    def _send_error(self, server_id: str, error_msg: str) -> None:
        """
        统一发送错误消息。
        """
        self._control.send_data(
            server_id,
            PLUGIN_ID,
            {"type": -1, "error": error_msg},
        )

    def del_server(self, server_id: str) -> None:
        """
        手动删除某个 server_id 的映射（与类型 3 功能类似）。
        """
        self._server_names.pop(server_id, None)
