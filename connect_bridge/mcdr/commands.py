from mcdreforged.api.all import *
from typing import Dict

from connect_bridge.context import GlobalContext


class CommandAction(object):
    def __init__(self):
        self.config = GlobalContext.get_config()
        self.names = self.config.command_name
        self.perms = self.config.premission
        self.message = self.config.command_message
        self._control_interface = GlobalContext.get_control()
        self.apply(self._control_interface.mcdr)

    def apply(self, server: PluginServerInterface):
        for name in self.names.keys():
            server.register_help_message(
                self.names[name], self.message[name], self.perms[name]
            )

        builder = SimpleCommandBuilder()

        builder.command(f"{self.names['list']}", self._handle_list)
        builder.command(f"{self.names['tp']} <player>", self._handle_tp)
        builder.command(f"{self.names['tp']} allow", self._handle_tp_allow)
        builder.command(f"{self.names['tp']} deny", self._handle_tp_deny)
        builder.command(f"{self.names['here']}", self._handle_here)
        builder.command(f"{self.names['spec']}", self._handle_spec)
        builder.command(f"{self.names['back']}", self._handle_back)
        builder.command(f"{self.names['whereis']} <player>", self._handle_whereis)
        builder.command(F"{self.names['setname']} <server_name>", self._handle_setname)
        builder.command(f"{self.names['reload']}", self._handle_reload)

        builder.arg("player", Text)
        builder.arg("server_name", Text)

        builder.register(server)

    def _handle_list(self, source: CommandSource, context: CommandContext) -> None:
        if source.has_permission_higher_than(self.perms["list"]):
            source.reply("你没有权限使用此命令")
            return
        player_list = GlobalContext.get_player_list()
        player_list_str = ", ".join(player_list)
        if not player_list_str:
            source.reply("当前没有在线玩家")
        else:
            source.reply(f"当前在线玩家：{player_list_str}")

    def _handle_tp(self, source: CommandSource, context: CommandContext) -> None:
        """
        对应命令: tp <player>
        """
        target = context["player"]
        # TODO: 在这里调用 connect_core 的传送方法
        source.reply(f"正在将你传送到：{target}")

    def _handle_tp_allow(self, source: CommandSource, context: CommandContext) -> None:
        """
        对应命令: tp allow
        """
        # TODO: 在这里实现允许 TP 的逻辑
        source.reply("已允许 TP")

    def _handle_tp_deny(self, source: CommandSource, context: CommandContext) -> None:
        """
        对应命令: tp deny
        """
        # TODO: 在这里实现禁止 TP 的逻辑
        source.reply("已禁止 TP")

    def _handle_here(self, source: CommandSource, context: CommandContext) -> None:
        """
        对应命令: here
        """
        # TODO: 实现将其他玩家传送到自己身边
        source.reply("正在将目标玩家传送到你身边")

    def _handle_spec(self, source: CommandSource, context: CommandContext) -> None:
        """
        对应命令: spec
        """
        # TODO: 实现传送到观众模式
        source.reply("正在将目标玩家传送到观众模式")

    def _handle_back(self, source: CommandSource, context: CommandContext) -> None:
        """
        对应命令: back
        """
        # TODO: 实现返回上一个位置
        source.reply("正在将你返回上一个位置")

    def _handle_whereis(self, source: CommandSource, context: CommandContext) -> None:
        """
        对应命令: whereis <player>
        """
        target = context["player"]
        # TODO: 查询 target 的位置
        source.reply(f"玩家 {target} 当前在 X,Y,Z 坐标")

    def _handle_setname(self, source: CommandSource, context: CommandContext) -> None:
        """
        对应命令: setname <server_name>
        """
        new_name = context["server_name"]
        self.config.server_name = new_name
        self._control_interface.mcdr.save_config_simple(self.config)
        source.reply(f"已将 server_name 设置为：{new_name}")

    def _handle_reload(self, source: CommandSource, context: CommandContext) -> None:
        """
        对应命令: reload
        """
        source.reply("配置已重新加载")
        self._control_interface.mcdr.reload_plugin("connect_bridge")
