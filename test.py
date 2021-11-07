from blive_danmaku.room import Room
from blive_danmaku.config import RoomConfig
import time

conf = {
    'id': 7777,
    'nickname': 'Test',
    'listener': [
        "DANMU_MSG", "COMBO_SEND", "GUARD_BUY", "SUPER_CHAT_MESSAGE",
        "PREPARING", "LIVE", "INTERACT_WORD", "VERIFICATION_SUCCESSFUL"
    ]
}
room = Room(RoomConfig(**conf))

print('尝试连接')
room.start()
# room.run()
while room.stream.get_status() != room.stream.STATUS_ESTABLISHED:
    pass
time.sleep(5)
print('尝试断开')
room.cancel()
room.join()
time.sleep(5)
print('尝试连接')
del room
room = Room(RoomConfig(**conf))
room.start()
room.join()
