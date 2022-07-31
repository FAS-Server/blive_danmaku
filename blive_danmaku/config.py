from typing import List

from mcdreforged.api.types import PluginServerInterface
from mcdreforged.api.utils import Serializable


class RoomConfig(Serializable):
    id: int = 1233654  # 房间id
    listener: List[str] = [
        "DANMU_MSG", "COMBO_SEND", "GUARD_BUY", "SUPER_CHAT_MESSAGE",
        "PREPARING", "LIVE", "INTERACT_WORD", "VERIFICATION_SUCCESSFUL"
    ]
    nickname: str = 'FAS'
    is_login: bool = False
    csrf: str = ''
    sessdata: str = ''


def load_config(server: PluginServerInterface) -> RoomConfig:
    filename = server.get_self_metadata().id + '.json'
    return server.load_config_simple(file_name=filename, target_class=RoomConfig)


def save_config(server: PluginServerInterface, config: RoomConfig):
    filename = server.get_self_metadata().id + '.json'
    server.save_config_simple(config=config, file_name=filename)
