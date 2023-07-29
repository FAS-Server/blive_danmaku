# Blive Danmaku

[![MCDReforged](https://img.shields.io/badge/dynamic/json?label=MCDReforged&query=dependencies.mcdreforged&url=https%3A%2F%2Fraw.githubusercontent.com%2FFAS-Server%2Fblive_danmaku%2Fmaster%2Fmcdreforged.plugin.json&style=plastic)](https://github.com/Fallen-Breath/MCDReforged)
[![license](https://img.shields.io/github/license/FAS-Server/blive_danmaku)](https://github.com/FAS-Server/blive_danmaku/blob/master/LICENSE)
[![build status](https://img.shields.io/github/workflow/status/FAS-Server/blive_danmaku/CI%20for%20MCDR%20Plugin?label=build&style=plastic)](https://github.com/FAS-Server/blive_danmaku/actions)
[![Release](https://img.shields.io/github/v/release/FAS-Server/blive_danmaku?style=plastic)](https://github.com/FAS-Server/blive_danmaku/releases/latest)
![total download](https://img.shields.io/github/downloads/FAS-Server/blive_danmaku/total?label=total%20download&style=plastic)

> 一个简易的的Bilibili直播弹幕插件

安装后在游戏内输入 `!!blive` 获取帮助信息.

配置文件: 默认存储于 `config/blive_danmaku/blive_danmaku.json` 中

```json5
{
    "id": 1233654,      // 直播间ID
    "nickname": "FAS",  // 直播间昵称, 会作为前缀出现
    "listener": [       // 正在监听的事件
        "DANMU_MSG",
        "COMBO_SEND",
        "GUARD_BUY",
        "SUPER_CHAT_MESSAGE",
        "PREPARING",
        "LIVE",
        "VERIFICATION_SUCCESSFUL"
    ]
}
```

监听事件对照表:

| 代码                            | 支持  | 含义    | 备注          |
|-------------------------------|-------|-------------|-------------|
| ANCHOR_LOT_AWARD | ✅ | 天选时刻中奖名单 |  |
| ANCHOR_LOT_CHECKSTATUS | ❌ | 天选时刻检查状态 | 未实现 |
| ANCHOR_LOT_END | ❌ | 天选时刻抽奖结束 | 未实现 |
| ANCHOR_LOT_START | ✅ | 天选时刻抽奖开始 |  |
| COMBO_SEND | ✅ | 礼物连击 |  |
| COMMON_NOTICE_DANMAKU | ✅ | 通用通知 | 含红包礼物涨粉、直播活动信息等 |
| DANMU_AGGREGATION | ❌ | 抽奖弹幕 | 未实现，包含天选抽奖弹幕、红包抽奖弹幕等 |
| DANMU_MSG | ✅ | 弹幕信息 |  |
| ENTRY_EFFECT | ✅ | 入场特效 | 会压缩过长的用户名（用...表示） |
| GUARD_BUY            | ✅ | 续费舰长 |             |
| HOT_RANK_CHANGED | ✅ | 限时热门榜排名 | 包含榜单名、具体排名 |
| HOT_RANK_CHANGED_V2 | ✅ | 限时热门榜排名V2 | 包含榜单名、具体排名和模糊排名（如 虚拟主播top50） |
| HOT_RANK_SETTLEMENT | ✅ | 限时热门榜排名通知 | 例：恭喜主播 <% 主播名称 %> 荣登限时热门榜总榜榜首! 即将获得热门流量推荐哦！ |
| HOT_RANK_SETTLEMENT_V2 | ❌ | 限时热门榜排名通知V2 | 未实现，因信息同上 |
| INTERACT_WORD | ✅ | 进入直播间 | 只包含非舰长用户的进入 |
| LIKE_INFO_V3_CLICK | ✅ | 用户点赞 | |
| LIKE_INFO_V3_UPDATE | ✅ | 点赞总数量更新 | |
| LIVE | ✅ | 直播开始 | |
| NOTICE_MSG | ❌ | 通知横幅 | 未实现，无计划，包含舰长续费跑马灯、直播任务情况、此房间和**其他房间**的大额礼物等 |
| ONLINE_RANK_COUNT | ✅ | 高能用户总数量 | |
| ONLINE_RANK_TOP3 | ✅ | 高能榜前三变化 | |
| ONLINE_RANK_V2 | ✅ | 高能榜前七名单 | |
| POPULARITY_RED_POCKET_NEW | ✅ | 红包礼物 |  |
| POPULARITY_RED_POCKET_START | ✅ | 红包开抢 |  |
| POPULARITY_RED_POCKET_WINNER_LIST | ✅ | 红包中奖 |  |
| PREPARING | ✅ | 直播关闭 | |
| ROOM_REAL_TIME_MESSAGE_UPDATE | ❌ | 粉丝数、粉丝团更新 | 未实现 |
| SEND_GIFT                     | ✅ | 实时礼物  |            |
| SPECIAL_GIFT | ✅ | 特殊礼物 | 未实现, 节奏风暴类礼物但已经在其他礼物事件触发，故无必要 |
| STOP_LIVE_ROOM_LIST | ❌ | 停播房间列表 | 未实现，无计划 |
| SUPER_CHAT_MESSAGE            | ✅ | 醒目留言  |             |
| SUPER_CHAT_MESSAGE_JPN | ✅ | 醒目留言(日) | 带有日语翻译 |
| USER_TOAST_MSG | ✅ | 用户toast | 包含舰长续费（附陪伴时长） |
| VERIFICATION_SUCCESSFUL | ✅ | 成功连接 | |
| VIEW | ✅ | 人气更新 | |
| WATCHED_CHANGE | ✅ | 看过人数 | |
| WIDGET_BANNER | ❌ | 小部件横幅 | 未实现，活动信息展示 |
