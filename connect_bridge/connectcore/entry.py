global _control_interface

def on_load(control_interface):
    """加载"""
    global _control_interface
    _control_interface = control_interface
    _control_interface.info("Hello World! This is Plugin!!!!!!")


def on_unload():
    """卸载"""
    _control_interface.info("Bye!")


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
