from mcdreforged.api.types import PluginServerInterface


def on_load(server: PluginServerInterface, prev_module):
    pass


def on_unload(server: PluginServerInterface):
    pass


def on_server_startup(server: PluginServerInterface):
    pass


def on_server_stop(server: PluginServerInterface, server_return_code: int):
    pass
