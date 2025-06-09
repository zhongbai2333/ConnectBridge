from connect_core.api.interface import PluginControlInterface
from connect_bridge.mcdr.config import Config


_config: Config = None
_control_interface: PluginControlInterface = None
_player_list: list = []


class GlobalContext(object):
    def __init__(self, control: PluginControlInterface, config: Config):
        global _config, _control_interface
        _control_interface = control
        _config = config

    @staticmethod
    def get_control() -> PluginControlInterface:
        """获取控制接口"""
        return _control_interface

    @staticmethod
    def get_config() -> Config:
        """获取Config"""
        return _config

    @staticmethod
    def get_player_list() -> None:
        """获取玩家列表"""
        return _player_list
