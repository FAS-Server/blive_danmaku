# Blive Danmaku

[![MCDReforged](https://img.shields.io/badge/dynamic/json?label=MCDReforged&query=dependencies.mcdreforged&url=https%3A%2F%2Fraw.githubusercontent.com%2FFAS-Server%2Fblive_danmaku%2Fmaster%2Fmcdreforged.plugin.json&style=plastic)](https://github.com/Fallen-Breath/MCDReforged)
[![license](https://img.shields.io/github/license/FAS-Server/blive_danmaku)](https://github.com/FAS-Server/blive_danmaku/blob/main/LICENSE)
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

| 代码                            | 含义    | 备注          |
|-------------------------------|-------|-------------|
| DANMU_MSG                     | 弹幕信息  |             |
| SEND_GIFT                     | 实时礼物  | 不推荐使用, 可能刷屏 |
| COMBO_SEND                    | 礼物连击  | 响应稍慢, 避免刷屏  |
| GUARD_BUY                     | 续费大航海 |             |
| SUPER_CHAT_MESSAGE            | 醒目留言  |             |
| PREPARING                     | 直播关闭  |             |
| LIVE                          | 直播开始  |             |
| INTERACT_WORD                 | 进入直播间 |             |
| VERIFICATION_SUCCESSFUL       | 成功连接  |             |
| WELCOME                       | 老爷加入  | 未实现         |
| WELCOME_GUARD                 | 房管加入  | 未实现         |
| ENTRY_EFFECT                  | 入场特效  | 未实现         |
| ROOM_RANK                     | 排名更新  | 未实现         |
| ACTIVITY_BANNER_UPDATE_V2     | 小时榜   | 未实现         |
| ROOM_REAL_TIME_MESSAGE_UPDATE | 粉丝数更新 | 未实现         |
| NOTICE_MSG                    | 系统通知  | 未实现         |
| VIEW                          | 人气更新  | 未实现         |

