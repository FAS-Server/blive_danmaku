from mcdreforged.api.utils import Serializable
from typing import List, Dict, Optional
from mcdreforged.api.types import PluginServerInterface
from blive_danmaku.utils import Singleton


class Room_Config(Serializable):
    id: int = 1233654  # 房间id
    listener: List[str] = [
        "DANMU_MSG", "COMBO_SEND", "GUARD_BUY", "SUPER_CHAT_MESSAGE",
        "PREPARING", "LIVE", "INTERACT_WORD", "VERIFICATION_SUCCESSFUL"
    ]
    nickname: str = 'FAS'


class Config(Serializable, Singleton):
    switch: bool = True
    default_listener: List[str] = ['DANMU_MSG', 'COMBO_SEND']
    room_map: Dict[str, Room_Config] = {'1233654': Room_Config()}

    def save(self):
        server = PluginServerInterface.get_instance().as_plugin_server_interface()
        filename = server.get_self_metadata().id + '.json'
        server.save_config_simple(
            self, file_name=filename, in_data_folder=False)
        PluginServerInterface.get_instance(
        ).as_plugin_server_interface().save_config_simple(self)


def save_config():
    config = Config.get_instance()
    config.save()
