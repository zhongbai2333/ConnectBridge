import os
import time
from mcdreforged.api.all import *
from connect_core.api.mcdr import get_plugin_control_interface

from connect_bridge.constants import PLUGIN_ID
from connect_bridge.mcdr.recv_data import MessageParser
from connect_bridge.mcdr.commands import CommandAction
from connect_bridge.mcdr.config import Config
from connect_bridge.context import GlobalContext

_config, _control_interface, _parse_msg = None, None, None


# MCDR Start point
def on_load(server: PluginServerInterface, _):
    global _control_interface, _parse_msg, _config
    _control_interface = get_plugin_control_interface(
        PLUGIN_ID, f"{PLUGIN_ID}.mcdr.entry", server
    )
    if not _control_interface:
        return

    _config = server.load_config_simple(target_class=Config)

    GlobalContext(_control_interface, _config)

    _parse_msg = MessageParser()

    CommandAction()

    _control_interface.info(_control_interface.tr("mcdr.plugin_loaded", PLUGIN_ID))

def on_unload(_):
    try:
        _control_interface.send_data("all", PLUGIN_ID, {"type": 3})
    except Exception as e:
        pass

def new_connect(server_id):
    """有新的连接"""
    pass


def del_connect(server_id):
    """有断开连接"""
    _parse_msg.del_server(server_id)


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
    if not _config.server_name:
        _config.server_name = _control_interface.get_server_id()
    os.system(f"title [{_control_interface.get_server_id()}]{_config.server_name}")
    _control_interface.send_data(
        "all",
        PLUGIN_ID,
        {
            "type": 0,
            "server_name": _config.server_name,
            "port": _control_interface.mcdr.get_server_information().port,
        },
    )


def disconnected():
    """断开连接"""
    pass


@new_thread("wait_onload")
def websockets_started():
    while not _control_interface:
        time.sleep(0.5)
    if not _config.server_name:
        _config.server_name = _control_interface.get_server_id()


def recv_data(server_id: str, data: dict):
    """收到数据包"""
    _parse_msg.parse_msg(server_id, data)


def recv_file(server_id: str, file: str):
    """收到文件"""
    _control_interface.info(file)
