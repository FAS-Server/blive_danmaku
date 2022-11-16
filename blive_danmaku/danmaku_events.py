from enum import Enum


class Event:
    def __init__(self, code: str, msg: str = '', remark: str = ''):
        self.code = code
        self.msg = msg
        self.remark = remark


class DanmakuEvents(Enum):
    ANCHOR_LOT_AWARD = Event('ANCHOR_LOT_AWARD', '天选时刻中奖名单')
    # ANCHOR_LOT_CHECKSTATUS = Event('ANCHOR_LOT_CHECKSTATUS', '天选时刻检查状态', '未实现')
    # ANCHOR_LOT_END = Event('ANCHOR_LOT_END', "天选时刻抽奖结束", '未实现')
    ANCHOR_LOT_START = Event('ANCHOR_LOT_START', '天选时刻抽奖开始')
    COMBO_SEND = Event('COMBO_SEND', '礼物连击')
    COMMON_NOTICE_DANMAKU = Event('COMMON_NOTICE_DANMAKU', '通用通知', '含红包礼物涨粉、直播活动信息等')
    # DANMU_AGGREGATION = Event('DANMU_AGGREGATION', '抽奖弹幕', '未实现，包含天选抽奖弹幕、红包抽奖弹幕等')
    DANMU_MSG = Event('DANMU_MSG', '用户弹幕')
    # DISCONNECT = Event('DISCONNECT', '断开连接', '未实现')
    ENTRY_EFFECT = Event('ENTRY_EFFECT', '进场特效', '会压缩过长的用户名（用...表示）')
    GUARD_BUY = Event('GUARD_BUY', '续费大航海')
    HOT_RANK_CHANGED = Event('HOT_RANK_CHANGED', '限时热门榜排名', '包含榜单名、具体排名')
    HOT_RANK_CHANGED_V2 = Event('HOT_RANK_CHANGED_V2', '限时热门榜排名V2', '包含榜单名、具体排名和模糊排名（如 虚拟主播top50）')
    HOT_RANK_SETTLEMENT = Event('HOT_RANK_SETTLEMENT', '限时热门榜排名通知', '例：恭喜主播 主播名称 荣登限时热门榜总榜榜首! 即将获得热门流量推荐哦！')
    # HOT_RANK_SETTLEMENT_V2 = Event('HOT_RANK_SETTLEMENT_V2', '限时热门榜排名通知V2', '未实现，因信息同上')
    INTERACT_WORD = Event('INTERACT_WORD', '用户进入直播间', '只包含非舰长用户')
    LIKE_INFO_V3_CLICK = Event('LIKE_INFO_V3_CLICK', '用户点赞')
    LIKE_INFO_V3_UPDATE = Event('LIKE_INFO_V3_UPDATE', '点赞总数量更新')
    LIVE = Event('LIVE', '直播开始')
    # NOTICE_MSG = Event('NOTICE_MSG', '系统通知', '未实现，无计划，包含舰长续费跑马灯、直播任务情况、此房间和其他房间的大额礼物等')
    ONLINE_RANK_COUNT = Event('ONLINE_RANK_COUNT', '高能用户总数量')
    ONLINE_RANK_TOP3 = Event('ONLINE_RANK_TOP3', '高能榜前三变化')
    ONLINE_RANK_V2 = Event('ONLINE_RANK_V2', '高能榜前七列表')
    POPULARITY_RED_POCKET_NEW = Event('POPULARITY_RED_POCKET_NEW', '红包礼物')
    POPULARITY_RED_POCKET_START = Event('POPULARITY_RED_POCKET_START', '红包开抢')
    POPULARITY_RED_POCKET_WINNER_LIST = Event('POPULARITY_RED_POCKET_WINNER_LIST', '红包中奖')
    PREPARING = Event('PREPARING', '直播关闭')
    ROOM_REAL_TIME_MESSAGE_UPDATE = Event('ROOM_REAL_TIME_MESSAGE_UPDATE', '粉丝数等更新', '未实现')
    SEND_GIFT = Event('SEND_GIFT', '实时礼物')
    # SPECIAL_GIFT = Event('SPECIAL_GIFT', '特殊礼物', '未实现, 为节奏风暴类礼物但已经在其他事件中触发, 无必要')
    # STOP_LIVE_ROOM_LIST = Event('STOP_LIVE_ROOM_LIST', '停播房间列表', '未实现，无计划')
    SUPER_CHAT_MESSAGE = Event('SUPER_CHAT_MESSAGE', '醒目留言(SC)')
    SUPER_CHAT_MESSAGE_JPN = Event('SUPER_CHAT_MESSAGE_JPN', '醒目留言（带日语翻译）')
    # TIMEOUT = Event('TIMEOUT', '心跳响应超时', '未实现')
    USER_TOAST_MSG = Event('USER_TOAST_MSG', '用户toast', '包含舰长续费（附陪伴时长）')
    VERIFICATION_SUCCESSFUL = Event('VERIFICATION_SUCCESSFUL', '连接成功')
    VIEW = Event('VIEW', '人气更新')
    WATCHED_CHANGE = Event('WATCHED_CHANGE', '看过人数')
    # WIDGET_BANNER = Event('WIDGET_BANNER', '小部件横幅', '未实现, 活动信息展示')


all_event_name = list(map(lambda t: t.value.code, DanmakuEvents))
