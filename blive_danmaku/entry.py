from typing import Optional

from mcdreforged.api.types import PluginServerInterface

from blive_danmaku.config import load_config
from blive_danmaku.room import Room
from blive_danmaku.user_interface import UserInterface
from blive_danmaku.cmd_tree import register_command

ui: Optional[UserInterface] = None


def on_load(server: PluginServerInterface, prev_module):
    global ui
    config = load_config(server)
    room_thread = Room(config)
    ui = UserInterface(server, room_thread, config)
    register_command(server, ui)
    ui.room.start()


def on_unload(server: PluginServerInterface):
    if ui.room.is_alive():
        ui.room.cancel()
        ui.room.join()
