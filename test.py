from time import time
from blive_danmaku.room import Room
from blive_danmaku.config import Room_Config
from bilibili_api import sync
import time

conf = {
    'id': 22634198,
    'nickname': '珈乐',
    'listener': [
        "DANMU_MSG", "COMBO_SEND", "GUARD_BUY", "SUPER_CHAT_MESSAGE",
        "PREPARING", "LIVE", "INTERACT_WORD", "VERIFICATION_SUCCESSFUL"
    ]
}
room = Room(Room_Config(**conf))

room.start()
