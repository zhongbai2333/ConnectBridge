from mcdreforged.api.all import *
from connect_core.api.mcdr import get_plugin_control_interface
from connect_bridge.constants import PLUGIN_ID

__mcdr_server, _control_interface = None, None


# MCDR Start point
def on_load(server: PluginServerInterface, _):
    global __mcdr_server, _control_interface
    __mcdr_server = server
    _control_interface = get_plugin_control_interface(
        PLUGIN_ID, f"{PLUGIN_ID}.mcdr.entry", server
    )

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
                "whereis": 2,
                "reload": 3,
            },
            "command_name": {
                "tp": "!!tp",
                "here": "!!here",
                "spec": "!!spec",
                "whereis": "!!whereis",
                "reload": "!!ccb reload",
            },
        }
        _control_interface.save_config(config)

    _control_interface.info(_control_interface.tr("mcdr.plugin_loaded", PLUGIN_ID))


def new_connect(server_list):
    """有新的连接"""
    _control_interface.info(server_list)


def del_connect(server_list):
    """有断开连接"""
    _control_interface.info(server_list)


def connected():
    """连接成功"""
    _control_interface.info("Connected!")


def disconnected():
    """断开连接"""
    _control_interface.info("Disconnected!")


def recv_data(server_id: str, data: dict):
    """收到数据包"""
    _control_interface.info(data)


def recv_file(server_id: str, file: str):
    """收到文件"""
    _control_interface.info(file)
