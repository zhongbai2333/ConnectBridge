from mcdreforged.api.types import PluginServerInterface

class CoreControlInterface:
    def __init__(self):
        pass

    # =============
    #  Json Editer
    # =============
    def get_config(
        self,
        key: str = "all",
        default: any = None,
        config_path: str = None,
    ) -> dict:
        """
        获取配置文件

        Args:
            config_path (str): 配置文件目录, 默认为插件或服务器默认 config 路径
            key (str): 配置项名称, 默认为 "all", 表示读取所有配置项
            default (any): 默认值, 如果配置项不存在则返回默认值且写入到配置文件中

        Returns:
            dict: 配置文件字典
        """
        pass

    def save_config(self, config_data: dict, config_path: str = None) -> None:
        """
        写入配置文件

        Args:
            config_data (dict): 新的配置项字典
            config_path (str): 配置文件目录, 默认为插件或服务器默认 config 路径
        """
        pass

    # =============
    #   Translate
    # =============
    def translate(self, key: str, *args) -> str:
        """
        获取翻译项

        Args:
            key (str): 翻译文件关键字
            *args (tuple): 字段插入内容

        Returns:
            str: 翻译文本
        """
        pass

    def tr(self, key: str, *args) -> str:
        """
        获取翻译项 | `translate函数的别称`

        Args:
            key (str): 翻译文件关键字
            *args (tuple): 字段插入内容

        Returns:
            str: 翻译文本
        """
        pass

    # =============
    #   Log Print
    # =============
    def info(self, msg: any) -> None:
        """
        输出INFO级别的日志信息。

        Args:
            msg (any): 日志消息内容。
        """
        pass

    def warn(self, msg: any) -> None:
        """
        输出WARN级别的日志信息。

        Args:
            msg (any): 日志消息内容。
        """
        pass

    def error(self, msg: any) -> None:
        """
        输出ERROR级别的日志信息。

        Args:
            msg (any): 日志消息内容。
        """
        pass

    def debug(self, msg: any) -> None:
        """
        输出DEBUG级别的日志信息。

        Args:
            msg (any): 日志消息内容。
        """
        pass

    # ============
    #   Command
    # ============
    def add_command(self, command: str, func: callable) -> None:
        """
        添加命令到命令行界面中。

        Args:
            command (str): 命令名称。
            func (callable): 命令对应的函数。
        """
        pass

    def remove_command(self, command: str) -> None:
        """
        移除命令从命令行界面中。

        Args:
            command (str): 命令名称。
        """
        pass

    def set_prompt(self, prompt: str) -> None:
        """
        设置命令行提示符。

        Args:
            prompt (str): 命令行提示符内容。
        """
        pass

    def set_completer_words(self, words: dict) -> None:
        """
        设置命令行补全词典。

        Args:
            words (dict): 命令行补全词典内容。
        """
        pass

    def flush_cli(self) -> None:
        """
        刷新命令行补全词典。
        """
        pass

    # =========
    #   Tools
    # =========
    def is_server(self) -> bool:
        """
        判断是否为服务器

        Returns:
            bool: 是/否
        """
        pass

    def get_server_list(self) -> list:
        """
        获取服务器列表

        Returns:
            list: 服务器列表
        """
        pass

    def get_server_id(self) -> str:
        """
        客户端反馈服务器ID

        Returns:
            str: 服务器ID
        """
        pass

class PluginControlInterface(CoreControlInterface):
    def __init__(
        self,
        sid: str,
        self_path: str,
        config_path: str,
        mcdr: PluginServerInterface = None,
    ):
        """
        插件控制接口

        Args:
            sid (str): 插件ID
            self_path (str): 自身路径
            config_path (str): 配置文件路径
        """
        # 导入
        super().__init__()

        pass

    # ========
    #   Send
    # ========
    def send_data(self, server_id: str, plugin_id: str, data: dict) -> None:
        """
        向指定的服务器发送消息。

        Args:
            server_id (str): 目标服务器的唯一标识符。
            plugin_id (str): 目标服务器插件的唯一标识符
            data (str): 要发送的数据。
        """
        pass

    def send_file(
        self, server_id: str, plugin_id: str, file_path: str, save_path: str
    ) -> None:
        """
        向指定的服务器发送文件。

        Args:
            server_id (str): 目标服务器的唯一标识符。
            plugin_id (str): 目标服务器插件的唯一标识符
            file_path (str): 要发送的文件目录。
            save_path (str): 要保存的位置。
        """
        pass

    # =========
    #   Tools
    # =========
    def get_history_packet(self, server_id: str = None) -> list | None:
        """
        获取历史数据包，客户端无需参数

        Args:
            server_id (str): 服务器ID

        Returns:
            dict: 数据包
        """
        pass
