from mcdreforged.api.all import Serializable
from typing import Dict


class Config(Serializable):
    server_name: str = ""
    allow_tp: bool = False
    allow_spectator_tp: bool = True
    auto_spectator_tp: bool = True
    permission: Dict[str, int] = {
        "list": 1,
        "tp": 1,
        "here": 1,
        "spec": 1,
        "back": 1,
        "whereis": 2,
        "setname": 3,
        "reload": 3,
    }
    command_name: Dict[str, str] = {
        "list": "!!list",
        "tp": "!!tp",
        "here": "!!here",
        "spec": "!!spec",
        "back": "!!back",
        "whereis": "!!whereis",
        "setname": "!!ccb setname",
        "reload": "!!ccb reload",
    }
    command_message: Dict[str, str] = {
        "list": "所有服务器玩家列表",
        "tp": "传送至玩家",
        "here": "公开自己的位置",
        "spec": "切换第三人称",
        "back": "返回传送前/死亡/第三人称前的位置",
        "whereis": "查询玩家位置",
        "setname": "设置ConnectBridge服务器名称",
        "reload": "重载ConnectBridge插件",
    }
