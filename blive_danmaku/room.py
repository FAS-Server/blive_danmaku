import asyncio
from asyncio import CancelledError
from threading import Thread
from typing import List

from bilibili_api import live
from bilibili_api.exceptions.LiveException import LiveException
from mcdreforged.api.decorator import new_thread
from mcdreforged.api.rtext import RText, RColor, RTextBase, RTextList, RAction, RStyle
from requests import post
import time

from blive_danmaku.config import RoomConfig
from blive_danmaku.danmaku_events import all_event_name
from blive_danmaku.utils import print_msg

def get_user(uid: int, uname: str, warpped: bool = True, color: RColor = RColor.white):
        utext = f'<{uname}> ' if warpped else uname
        url = f'https://space.bilibili.com/{uid}'
        return RText(utext, color).h(url).c(RAction.open_url, url)
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
    def url(self):
        return f"https://live.bilibili.com/{self.id}"

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
        return RText(f'[{self.nickname}] ', RColor.light_purple).h(self.url).c(RAction.open_url, self.url)

    @staticmethod
    def get_user_prefix(uname: str, uid: int, color: RColor = RColor.white, short_prefix: bool = False):
        text = f'{uname}' if short_prefix else f'<{uname}> '
        url = f'https://space.bilibili.com/{uid}'
        return RText(text, color).h(url).c(RAction.open_url, url)

    def build_rtext_list(self, raw: List[RTextBase], sep: str = ', ') -> RTextBase:
        text = RTextList()
        size = len(raw)
        for i in range(size):
            text.append(raw[i])
            if i != size - 1:
                text.append(sep)
        return text

    @new_thread
    def send_danmaku(self, msg: str):
        payload = post(
            url='https://api.live.bilibili.com/msg/send',
            params={
                'msg': msg,
                'rnd': int(time.time()),
                'color': 16777215,
                'fontsize': 25,
                'mode': 1,
                'roomid': self.id,
                'bubble': 0,
                'csrf': self.config.csrf,
                'csrf_token': self.config.csrf
            },
            cookies={
                'SESSDATA': self.config.sessdata,
                'bili_jct': self.config.csrf
            }
        )

    # -------------#
    #  事件监听开始 #
    # -------------#
    async def on_anchor_lot_award(self, event):
        # ANCHOR_LOT_AWARD: 天选时刻中将名单
        users_text = map(lambda x: get_user(x['uid'], x['uname'], False, RColor.red), event['data']['data']['award_users'])
        print_msg(RTextList(
            self.get_room_prefix(),
            RText('[天选时刻] ', RColor.dark_red),
            '恭喜 ',
            # award_users,
            self.build_rtext_list(list(users_text)),
            ' 获得了',
            RText(event['data']['data']['award_name'], RColor.red, RStyle.bold)
        ))

    async def on_anchor_lot_start(self, event):
        data = event['data']['data']
        print_msg(RTextList(
            self.get_room_prefix(),
            f"天选时刻开启！\n",
            f"    奖品: {data['award_name']} x{data['award_num']}\n",
            f"    抽奖口令:{data['danmu']}\n", 
            f"    中奖要求: {data['require_text']}"
        ))

    async def on_combo_send(self, event):
        # COMBO_SEND：礼物连击
        print_msg(RTextList(
            self.get_room_prefix(),
            get_user(
                event['data']['data']['uid'], event['data']['data']['uname'], False),
            '{action}了{gift_name} x{combo_num}'.format(**event['data']['data'])
        ))

    async def on_common_notice_danmaku(self, event):
        # COMMON_NOTICE_DANMAKU: 通用通知弹幕
        for segment in event['data']['data']['content_segments']:
            print_msg(RTextList(
                self.get_room_prefix(),
                segment['text']
            ))

    async def on_danmu_msg(self, event):
        # DANMU_MSG: 用户发送弹幕
        user_data = event['data']['info'][2]
        print_msg(RTextList(
            self.get_room_prefix(),
            get_user(user_data[0], user_data[1]),
            event['data']['info'][1]
        ))

    async def on_entry_effect(self, event):
        # ENTRY_EFFECT
        print_msg(RTextList(
            self.get_room_prefix(),
            str(event['data']['data']['copy_writing']).replace('<%', '').replace('%>', '')
        ))

    async def on_guard_buy(self, event):
        # GUARD_BUY：续费舰长
        print_msg(RTextList(
            self.get_room_prefix(),
            get_user(event['data']['data']['uid'], event['data']['data']['username'], False),
            '续费了 {num}个月 {gift_name}'.format(**event['data']['data'])
        ))

    async def on_hot_rank_changed(self, event):
        # HOT_RANK_CHANGED 限时热门榜
        data = event['data']['data']
        print_msg(
            RTextList(
                self.get_room_prefix(),
                f'当前限时热门榜排名为{data["area_name"]}第{data["rank"]}'
            )
        )
    
    async def on_hot_rank_changed_v2(self, event):
        # HOT_RANK_CHANGED_V2 限时热门榜
        data = event['data']['data']
        print_msg(
            RTextList(
                self.get_room_prefix(),
                f'当前限时热门榜排名为{data["rank_desc"]}'
            )
        )

    async def on_hot_rank_settlement(self, event):
        # HOT_RANK_SETTLEMENT 限时热门榜排名通知
        data = event['data']['data']
        print_msg(RTextList(
            self.get_room_prefix(),
            str(data['dm_msg']).replace('<%', '').replace('%>', '').replace('  ', ' ')
        ))


    async def on_hot_rank_settlement_v2(self, event):
        # HOT_RANK_SETTLEMENT_V2: 限时热门榜排名通知
        await self.on_hot_rank_settlement(event)


    async def on_interact_word(self, event):
        # INTERACT_WORD: 非舰长用户进入直播间
        print_msg(RTextList(
            self.get_room_prefix(),
            get_user(event['data']['data']['uid'], event['data']['data']['uname'], False),
            '加入了直播间'.format(**event['data']['data'])
        ))

    async def on_like_info_v3_click(self, event):
        # LIKE_INFO_V3_CLICK 用户点赞
        data = event['data']['data']
        print_msg(RTextList(
            self.get_room_prefix(),
            get_user(data['uid'], data['uname'], False),
            data['like_text']
        ))

    async def on_like_info_v3_update(self, event):
        # LIKE_INFO_V3_UPDATE: 点赞总数量更新
        print_msg(RTextList(
            self.get_room_prefix(),
            f'被点赞{event["data"]["data"]["click_count"]}次'
        ))

    async def on_live(self, event):
        # LIVE: 直播开始
        print_msg(RTextList(
            self.get_room_prefix(),
            '直播已开启'
        ))

    async def on_online_rank_count(self, event):
        # ONLINE_RANK_COUNT: 高能用户总数量
        print_msg(RTextList(
            self.get_room_prefix(),
            f'高能用户总数为 {event["data"]["data"]["count"]}'
        ))

    async def on_online_rank_top3(self, event):
        # ONLINE_RANK_TOP3: 高能榜前三变化
        data = event['data']['data']
        for rank in data['list']:
            print_msg(RTextList(
                self.get_room_prefix(),
                str(rank['msg']).replace('<%', '').replace('%>', '')
            ))

    async def on_online_rank_v2(self, event):
        # ONLINE_RANK_V2: 高能榜前七名单
        users = map(lambda x: get_user(x['uid'], x['uname'], False, RColor.red), event['data']['data']['list'])
        print_msg(RTextList(
            self.get_room_prefix(),
            '当前高能榜单前七名为: ',
            self.build_rtext_list(list(users))
        ))

    async def on_popularity_red_pocket_new(self, event):
        # POPULARITY_RED_POCKET_NEW
        data = event["data"]["data"]
        print_msg(RTextList(
            self.get_room_prefix(),
            get_user(data["uid"], data["uname"], False),
            RText(f"送出一个红包, 价值{data['price']}电池")
        ))
    
    
    async def on_popularity_red_pocket_start(self, event):
        # POPULARITY_RED_POCKET_START
        data = event["data"]["data"]
        awards = ', '.join(map(lambda x: f'{x["gift_name"]} x{x["num"]}', data['awards']))
        print_msg(RTextList(
            self.get_room_prefix(),
            get_user(data["sender_uid"], data["sender_name"], False),
            "的红包开抢了！奖品有：",
            awards
        ))

    async def on_popularity_red_pocket_winner_list(self, event):
        # POPULARITY_RED_POCKET_WINNER_LIST
        data = event['data']['data']
        awards = []
        for aid in data['awards']:
            _award = data['awards'][aid]
            _winner = map(lambda x: get_user(x[0], x[1], False, RColor.red), filter(lambda x: str(x[3])==aid, data['winner_info']))
            text = f"{self.build_rtext_list(list(_winner))} 抽中了 {_award['award_name']}"
            awards.append(text)
        print_msg(RTextList(
            self.get_room_prefix(),
            "[红包] 恭喜：\n\t",
            self.build_rtext_list(awards, '\n\t')
        ))

    async def on_preparing(self, event):
        # PREPARING: 直播准备中
        # {'data': {'roomid': '22744945'}}
        print_msg(RTextList(
            self.get_room_prefix(),
            '直播已关闭'
        ))

    async def on_room_real_time_message_update(self, event):
        # ROOM_REAL_TIME_MESSAGE_UPDATE
        pass

    async def on_send_gift(self, event):
        # SEND_GIFT: 礼物
        print_msg(RTextList(
            self.get_room_prefix(),
            get_user(
                event['data']['data']['uid'], event['data']['data']['uname'], False),
            '{action}了{num}个{giftName}'.format(**event['data']['data'])
        ))

    async def on_special_gift(self, event):
        # SPECIAL_GIFT
        pass


    async def on_super_chat_message(self, event):
        # SUPER_CHAT_MESSAGE：醒目留言（SC）
        data = event['data']['data']
        print_msg(RTextList(
            self.get_room_prefix(),
            get_user(
                data['uid'], data['user_info']['uname'], False),
            '赠送了价值 §c￥{price}§r的醒目留言:\n\t§5{message}§r'.format(
                **data)
        ))

    async def on_super_chat_message_jpn(self, event):
        # SUPER_CHAT_MESSAGE_JPN：醒目留言,带日语翻译（SC）
        await self.on_super_chat_message(event)

    async def on_user_toast_msg(self, event):
        # USER_TOAST_MSG: 
        print_msg(RTextList(
            self.get_room_prefix(),
            str(event['data']['data']['toast_msg']).replace('<%', '').replace('%>', '')
        ))


    async def on_verification_successful(self, event):
        # VERIFICATION_SUCCESSFUL: 认证成功
        # {'room_display_id': 7777, 'room_real_id': 545068,
        #     'type': 'VERIFICATION_SUCCESSFUL'}
        print_msg(RTextList(
            self.get_room_prefix(),
            '直播间连接成功'
        ))

    async def on_view(self, event):
        # VIEW: 直播间人气更新
        # {'room_display_id': 7777, 'room_real_id': 545068,
        #     'type': 'VIEW', 'data': 6613938}
        print_msg(RTextList(
            self.get_room_prefix(),
            f'人气值为{event["data"]}'
        ))

    async def on_watch_changed(self, event):
        # WATCHED_CHANGE
        pass

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
