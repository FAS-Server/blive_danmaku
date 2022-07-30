from enum import Enum


class Event:
    def __init__(self, code: str, msg: str = '', remark: str = ''):
        self.code = code
        self.msg = msg
        self.remark = remark


class DanmakuEvents(Enum):
    DANMU_MSG = Event('DANMU_MSG', '用户发送弹幕')
    SEND_GIFT = Event('SEND_GIFT', '礼物', '不推荐, 实时性强但易刷屏')
    COMBO_SEND = Event('COMBO_SEND', '礼物连击', '推荐使用, 连击计算稍慢')
    GUARD_BUY = Event('GUARD_BUY', '续费大航海')
    SUPER_CHAT_MESSAGE = Event('SUPER_CHAT_MESSAGE', '醒目留言(SC)')
    # SUPER_CHAT_MESSAGE_JPN = Event('SUPER_CHAT_MESSAGE_JPN', '醒目留言（带日语翻译？）')
    WELCOME = Event('WELCOME', '老爷进入', '未实现')
    WELCOME_GUARD = Event('WELCOME_GUARD', '房管进入', '未实现')
    NOTICE_MSG = Event('NOTICE_MSG', '系统通知', '未实现')  # 全频道广播之类的
    PREPARING = Event('PREPARING', '直播未开始')
    LIVE = Event('LIVE', '直播开始')
    ROOM_REAL_TIME_MESSAGE_UPDATE = Event('ROOM_REAL_TIME_MESSAGE_UPDATE', '粉丝数等更新', '未实现')
    ENTRY_EFFECT = Event('ENTRY_EFFECT', '进场特效', '未实现')
    ROOM_RANK = Event('ROOM_RANK', '排名更新', '未实现')
    INTERACT_WORD = Event('INTERACT_WORD', '用户进入')
    ACTIVITY_BANNER_UPDATE_V2 = Event('ACTIVITY_BANNER_UPDATE_V2', '小时榜', '未实现')
    VIEW = Event('VIEW', '人气更新')
    # DISCONNECT = Event('DISCONNECT', '断开连接', '未实现')
    # TIMEOUT = Event('TIMEOUT', '心跳响应超时', '未实现')
    VERIFICATION_SUCCESSFUL = Event('VERIFICATION_SUCCESSFUL', '连接成功')


all_event_name = list(map(lambda t: t.value.code, DanmakuEvents))
