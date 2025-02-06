from mcdreforged.api.all import *
from connect_core.api.mcdr import get_plugin_control_interface
from auto_msg_title.api import get_player_info
from connect_bridge.constants import PLUGIN_ID
from connect_bridge.mcdr.recv_data import PraseMsg

__mcdr_server, _control_interface, _prase_msg = None, None, None


# MCDR Start point
def on_load(server: PluginServerInterface, _):
    global __mcdr_server, _control_interface, _prase_msg
    __mcdr_server = server
    _control_interface = get_plugin_control_interface(
        PLUGIN_ID, f"{PLUGIN_ID}.mcdr.entry", server
    )
    if not _control_interface:
        return
    _prase_msg = PraseMsg(__mcdr_server, _control_interface)

    if not _control_interface.get_config():
        config = {
            "server_name": "Survival",
            "allow_tp": False,
            "allow_spectator_tp": True,
            "auto_spectator_tp": True,
            "premission": {
                "tp": 1,
                "here": 1,
                "spec": 1,
                "back": 1,
                "whereis": 2,
                "reload": 3,
            },
            "command_name": {
                "tp": "!!tp",
                "here": "!!here",
                "spec": "!!spec",
                "back": "!!back",
                "whereis": "!!whereis",
                "reload": "!!ccb reload",
            },
        }
        _control_interface.save_config(config)

    _control_interface.info(_control_interface.tr("mcdr.plugin_loaded", PLUGIN_ID))


def new_connect(server_list):
    """有新的连接"""
    pass


def del_connect(server_list):
    """有断开连接"""
    pass


def on_user_info(_, info):
    """用户信息变化"""
    if info.is_player and _control_interface.get_server_id():
        _control_interface.send_data(
            "all",
            PLUGIN_ID,
            {
                "type": 1,
                "player_name": info.player,
                "msg": info.content,
            },
        )


def connected():
    """连接成功"""
    _control_interface.send_data(
        "all",
        PLUGIN_ID,
        {
            "type": 0,
            "server_name": _control_interface.get_config()["server_name"],
            "port": __mcdr_server.get_server_information().port,
        },
    )


def disconnected():
    """断开连接"""
    pass


def recv_data(server_id: str, data: dict):
    """收到数据包"""
    _prase_msg.prase_msg(server_id, data)


def recv_file(server_id: str, file: str):
    """收到文件"""
    _control_interface.info(file)
