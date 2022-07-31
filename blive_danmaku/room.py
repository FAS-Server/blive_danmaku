import asyncio
from asyncio import CancelledError

from bilibili_api import live
from bilibili_api.exceptions.LiveException import LiveException
from mcdreforged.minecraft.rtext import RTextBase, RTextList
from blive_danmaku.config import RoomConfig
from threading import Thread
from typing import List
from mcdreforged.api.rtext import RText, RColor

from blive_danmaku.utils import print_msg
from blive_danmaku.danmaku_events import all_event_name


class Room(Thread):
    def __init__(self, config: RoomConfig):
        Thread.__init__(self, name=f'BliveThread-{config.id}')
        self.listener_list = None
        self.config = config
        self.stream = live.LiveDanmaku(self.id)
        self._init_listener()
        self.event_loop = None
        self.task = None

    @property
    def id(self):
        return self.config.id

    @property
    def nickname(self):
        return self.config.nickname

    @nickname.setter
    def nickname(self, nick_name: str):
        self.config.nickname = nick_name

    @property
    def listener(self):
        return self.config.listener

    @listener.setter
    def listener(self, listener: List[str]):
        self.config.listener = listener

    def get_room_prefix(self) -> RTextBase:
        return RText(f'[{self.nickname}] ', RColor.light_purple)

    @staticmethod
    def get_user_prefix(uname: str, uid: int, color: RColor = RColor.white, short_prefix: bool = False):
        text = f'{uname}' if short_prefix else f'<{uname}>'
        return RText(text, color)

        # -------------#
        #  事件监听开始 #
        # -------------#

    async def on_danmu_msg(self, event):
        # DANMU_MSG: 用户发送弹幕
        # {
        #     'data':
        #     {
        #         'info': [
        #             [0, 1, 25, 16777215, 1635831657114, 1635830791, 0, 'be1cd984',
        #                 0, 0, 0, '', 0, '{}', '{}', {'mode': 0, 'extra': ''}],
        #             '花花看过崩坏3嘛，剧情可甜了',
        #             [270908318, '火云wizard', 0, 0, 0, 10000, 1, ''],
        #             [1, '粉丝团', '哔哩哔哩番剧', 544614, 6067854, '', 0,
        #                 12632256, 12632256, 12632256, 0, 0, 928123],
        #             [13, 0, 6406234, '>50000', 0],
        #             ['', ''], 0, 0, None, {
        #                 'ts': 1635831657, 'ct': '2D706B56'}, 0, 0, None, None, 0, 14
        #         ]
        #     }
        # }
        user_data = event['data']['info'][2]
        print_msg(RTextList(
            self.get_room_prefix(),
            self.get_user_prefix(user_data[1], user_data[0]),
            event['data']['info'][1]
        ))

    async def on_send_gift(self, event):
        # SEND_GIFT: 礼物 不建议使用, 可能造成消息刷屏; 建议使用 on_combo_send
        # {
        #     'data': {
        #         'data': {
        #             'action': '投喂', 'batch_combo_id': 'batch:gift:combo_id:193775874:269415357:30607:1635831689.2308',
        #             'batch_combo_send': None, 'beatId': '', 'biz_source': 'live', 'blind_gift': None,
        #             'broadcast_id': 0, 'coin_type': 'silver', 'combo_resources_id': 1, 'combo_send': None,
        #             'combo_stay_time': 3, 'combo_total_coin': 1, 'crit_prob': 0, 'demarcation': 1,
        #             'discount_price': 0, 'dmscore': 24, 'draw': 0, 'effect': 0, 'effect_block': 1,
        #             'float_sc_resource_id': 0,
        #             'giftId': 30607, 'giftName': '小心心', 'giftType': 5, 'gold': 0, 'guard_level': 0,
        #             'is_first': False, 'is_special_batch': 0, 'magnification': 1,
        #             'medal_info': {
        #                 'anchor_roomid': 0, 'anchor_uname': '', 'guard_level': 0, 'icon_id': 0, 'is_lighted': 1,
        #                 'medal_color': 9272486, 'medal_color_border': 9272486, 'medal_color_end': 9272486,
        #                 'medal_color_start': 9272486, 'medal_level': 10, 'medal_name': '德云色', 'special': '',
        #                 'target_id': 8739477
        #             },
        #             'num': 1, 'price': 0, 'rcost': 58907141, 'remain': 1, 'rnd': '1931396080', 'send_master': None,
        #             'silver': 0, 'super': 0, 'super_batch_gift_num': 2, 'super_gift_num': 2, 'svga_block': 0,
        #             'tag_image': '', 'tid': '1635831689120400002', 'timestamp': 1635831689, 'top_list': None,
        #             'total_coin': 0, 'uid': 193775874, 'uname': '浪里白条哈赛ki'
        #         }
        #     }
        # }
        print_msg(RTextList(
            self.get_room_prefix(),
            self.get_user_prefix(
                event['data']['data']['uname'], event['data']['data']['uid'], short_prefix=True),
            '{action}了{num}个{giftName}'.format(**event['data']['data'])
        ))

    async def on_combo_send(self, event):
        # COMBO_SEND：礼物连击
        # {
        #     'data':
        #     {
        #         'data':
        #         {
        #             'action': '投喂', 'batch_combo_id': 'batch:gift:combo_id:6992678:8739477:30607:1635836133.2648',
        #             'batch_combo_num': 24, 'combo_id': 'gift:combo_id:6992678:8739477:30607:1635836131.4221',
        #             'combo_num': 24, 'combo_total_coin': 0, 'dmscore': 56, 'gift_id': 30607, 'gift_name': '小心心',
        #             'gift_num': 0, 'is_show': 1,
        #             'medal_info': {'anchor_roomid': 0, 'anchor_uname': '', 'guard_level': 0, 'icon_id': 0,
        #             'is_lighted': 1, 'medal_color': 9272486, 'medal_color_border': 9272486,
        #             'medal_color_end': 9272486, 'medal_color_start': 9272486, 'medal_level': 12, 'medal_name': '德云色',
        #             'special': '', 'target_id': 8739477},
        #             'name_color': '', 'r_uname': '老实憨厚的笑笑', 'ruid': 8739477, 'send_master': None, 'total_num': 24,
        #             'uid': 6992678, 'uname': 'GalahaD_GY'
        #         }
        #     }
        # }
        print_msg(RTextList(
            self.get_room_prefix(),
            self.get_user_prefix(
                event['data']['data']['uname'], event['data']['data']['uid'], short_prefix=True),
            '{action}了{gift_name} x{combo_num}'.format(**event['data']['data'])
        ))

    async def on_guard_buy(self, event):
        # GUARD_BUY：续费大航海
        # {
        #     'data':
        #     {
        #         'data':
        #         {
        #             'uid': 90432317, 'username': '大明湖畔的郭胖子',
        #             'guard_level': 3, 'num': 1, 'price': 198000, 'gift_id': 10003, 'gift_name': '舰长',
        #             'start_time': 1635843126, 'end_time': 1635843126}}}
        print_msg(RTextList(
            self.get_room_prefix(),
            self.get_user_prefix(
                event['data']['data']['username'], event['data']['data']['uid'], short_prefix=True),
            '续费了{gift_name}'.format(**event['data']['data'])
        ))

    async def on_super_chat_message(self, event):
        # SUPER_CHAT_MESSAGE：醒目留言（SC）
        # {'data': {'data': {
        #     'dmscore': 80, 'end_time': 1635839132,
        #     'gift': {'gift_id': 12000, 'gift_name': '醒目留言', 'num': 1},
        #     'id': 2579512, 'is_ranked': 0, 'is_send_audit': 1,
        #     'medal_info': {'anchor_roomid': 7777, 'anchor_uname': '老实憨厚的笑笑', 'guard_level': 0, 'icon_id': 0,
        #     'is_lighted': 1, 'medal_color': '#5d7b9e', 'medal_color_border': 6126494, 'medal_color_end': 6126494,
        #     'medal_color_start': 6126494, 'medal_level': 5, 'medal_name': '德云色', 'special': '', 'target_id': 8739477},
        #     'message': '好听，主播别害羞，继续继续', 'price': 30, 'rate': 1000, 'start_time': 1635839072, 'time': 60,
        #     'token': '41648C03', 'trans_mark': 0, 'ts': 1635839072, 'uid': 3438425,
        #     'user_info': {'face_frame': '', 'guard_level': 0, 'is_main_vip': 1, 'is_svip': 0, 'is_vip': 0,
        #     'level_color': '#61c05a', 'manager': 0, 'name_color': '#666666', 'title': '0', 'uname': '北枳南笙mazarine',
        #     'user_level': 13}
        # }}}
        print_msg(RTextList(
            self.get_room_prefix(),
            self.get_user_prefix(
                event['data']['data']['user_info']['uname'], event['data']['data']['uid'], short_prefix=True),
            '赠送了价值 §c￥{price}§r的醒目留言:\n§5> {message}§r\n'.format(
                **event['data']['data'])
        ))

    async def on_welcome(self, event):
        # WELCOME: 老爷进入房间
        pass

    async def on_welcome_guard(self, event):
        # WELCOME_GUARD: 房管进入房间
        pass

    async def on_preparing(self, event):
        # PREPARING: 直播准备中
        # {'data': {'roomid': '22744945'}}
        print_msg(RTextList(
            self.get_room_prefix(),
            '直播已关闭'
        ))

    async def on_live(self, event):
        # LIVE: 直播开始
        # {
        #     'data':
        #     {
        #         'cmd': 'LIVE', 'live_key': '190125605077585777', 'voice_background': '',
        #         'sub_session_key': '190125605077585777sub_time:1635850495', 'live_platform': 'pc_link',
        #         'live_model': 0, 'roomid': 22744945
        #     }
        # }
        print_msg(RTextList(
            self.get_room_prefix(),
            '直播已开启'
        ))

    async def on_room_real_time_message_update(self, event):
        # ROOM_REAL_TIME_MESSAGE_UPDATE: 粉丝数等更新
        # {
        #     'data':
        #     {
        #         'data':
        #         {
        #             'fans': 1383249, 'red_notice': -1, 'fans_club': 49189
        #         }
        #     }
        # }
        pass

    async def on_entry_effect(self, event):
        # ENTRY_EFFECT: 进场特效
        # {
        #     'data':
        #     {
        #         'data':
        #         {
        #             'id': 4, 'uid': 356336867, 'target_id': 8739477, 'mock_effect': 0,
        #             'privilege_type': 3, 'copy_writing': '欢迎舰长 <%黑暗女王的泪%> 进入直播间', 'priority': 1,
        #             'show_avatar': 1, 'effective_time': 2, 'web_basemap_url': '', 'web_effective_time': 0,
        #             'web_effect_close': 0, 'web_close_time': 0, 'business': 1,
        #             'copy_writing_v2': '欢迎舰长 <%黑暗女王的泪%> 进入直播间', 'icon_list': [], 'max_delay_time': 7,
        #             'trigger_time': 1635840589630651228, 'identities': 6
        #         }
        #     }
        # }
        pass

    async def on_room_rank(self, event):
        # ROOM_RANK: 房间排名更新
        pass

    async def on_interact_word(self, event):
        # INTERACT_WORD: 用户进入直播间
        # {
        #     'data':
        #     {
        #         'data':
        #         {
        #             'contribution':
        #             {'grade': 0}, 'dmscore': 16, 'fans_medal':
        #             {'anchor_roomid': 57687, 'guard_level': 0, 'icon_id': 0, 'is_lighted': 0, 'medal_color': 1725515,
        #             'medal_color_border': 12632256,
        #                 'medal_color_end': 12632256, 'medal_color_start': 12632256, 'medal_level': 22,
        #                 'medal_name': '判判', 'score': 50002362, 'special': '', 'target_id': 4191996},
        #             'identities': [1], 'is_spread': 0, 'msg_type': 1, 'roomid': 545068, 'score': 1635837793687,
        #             'spread_desc': '', 'spread_info': '', 'tail_icon': 0, 'timestamp': 1635837793,
        #             'trigger_time': 1635837792648484600,
        #             'uid': 6168928, 'uname': '老攻ャ', 'uname_color': ''
        #         }
        #     }
        # }
        print_msg(RTextList(
            self.get_room_prefix(),
            self.get_user_prefix(
                event['data']['data']['uname'], event['data']['data']['uid'], short_prefix=True),
            '加入了直播间'.format(**event['data']['data'])
        ))

    async def on_activity_banner_update_v2(self, event):
        # ACTIVITY_BANNER_UPDATE_V2: 好像是房间名旁边那个xx小时榜
        pass

    async def on_notice_msg(self, event):
        # 系统通知
        pass

    async def on_view(self, event):
        # VIEW: 直播间人气更新
        # {'room_display_id': 7777, 'room_real_id': 545068,
        #     'type': 'VIEW', 'data': 6613938}
        print_msg(RTextList(
            self.get_room_prefix(),
            f'人气值为{event["data"]}'
        ))

    async def on_verification_successful(self, event):
        # VERIFICATION_SUCCESSFUL: 认证成功
        # {'room_display_id': 7777, 'room_real_id': 545068,
        #     'type': 'VERIFICATION_SUCCESSFUL'}
        print_msg(RTextList(
            self.get_room_prefix(),
            '直播间连接成功'
        ))

    # -------------#
    # 事件监听结束 #
    # -------------#

    def _init_listener(self):
        default_listener = ["DANMU_MSG", "SEND_GIFT", "COMBO_SEND", "GUARD_BUY", "SUPER_CHAT_MESSAGE", "PREPARING",
                            "LIVE",
                            "INTERACT_WORD", "VERIFICATION_SUCCESSFUL"]
        listener = []
        if len(self.listener) == 0:
            listener = default_listener
        else:
            for i in self.listener:
                if i in all_event_name:
                    listener.append(i)
        self.config.listener = listener
        # save_config()
        for e in listener:
            self.stream.add_event_listener(e, eval(f"self.on_{e.lower()}"))
            # self.stream.on(e)(eval(f"self.on_{e.lower()}"))
            # print('绑定事件: ' + e)

    async def connect(self):
        self.task = asyncio.create_task(self.stream.connect())
        try:
            await self.task
        except CancelledError:
            await self.stream.disconnect()

    def run(self):
        self.event_loop = asyncio.new_event_loop()
        self.event_loop.run_until_complete(self.connect())

    def cancel(self):
        try:
            self.task.cancel()
        except LiveException as e:
            print('错误! ' + e.msg)


if __name__ == '__main__':
    import time
    try:
        room_id = int(input('输入房间id: '))
        conf = {
            'id': room_id,
            'nickname': 'Test',
            'listener': [
                "DANMU_MSG", "COMBO_SEND", "GUARD_BUY", "SUPER_CHAT_MESSAGE",
                "PREPARING", "LIVE", "VERIFICATION_SUCCESSFUL"
            ]
        }
        room = Room(RoomConfig(**conf))

        print('尝试连接')
        room.start()
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
    except ValueError:
        print('输入格式错误!')
    except KeyboardInterrupt:
        exit(0)
    exit(0)
