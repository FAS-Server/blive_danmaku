from typing import Union

from mcdreforged.api.rtext import *
from mcdreforged.api.types import PluginServerInterface, CommandSource, PlayerCommandSource

from blive_danmaku.config import RoomConfig, save_config, load_config
from blive_danmaku.constants import PREFIX
from blive_danmaku.danmaku_events import DanmakuEvents, all_event_name, Event
from blive_danmaku.room import Room
from blive_danmaku.utils import Singleton


class UserInterface(Singleton):
    def __init__(self, server: PluginServerInterface, room_thread: Room, config: RoomConfig):
        self.need_reload = False
        self.permission_deny = RText('权限不足!', color=RColor.red)
        self.room = room_thread
        self.server = server
        self.config = config
        self.metadata = self.server.get_self_metadata()

    def conf_menu(self, src: CommandSource):
        self.get_conf(src, 'id')
        self.get_conf(src, 'nickname')
        self.get_conf(src, 'listener')
        if self.need_reload:
            self.reload_tips(src=src)

    def get_conf(self, src: CommandSource, conf_name):
        if conf_name == 'id':
            src.reply(RText(f'§b房间号§r: {self.room.id}').h('点击修改')
                      .c(RAction.suggest_command, f'{PREFIX} config id <房间号>'))
        elif conf_name == 'nickname':
            src.reply(RText(f'§b房间名称§r: {self.room.nickname}').h('点击修改')
                      .c(RAction.suggest_command, f'{PREFIX} config nickname <房间名称>'))
        elif conf_name == 'listener':
            src.reply(RText(f'§b事件监听§r:  {len(self.room.listener)} / {len(all_event_name)}')
                      .h('点击编辑').c(RAction.run_command, f'{PREFIX} config listener'))

    def help_msg(self, src: CommandSource):
        def command_rtext(cmd, help_msg):
            full_cmd = f'{PREFIX} {cmd}'.strip()
            return RText(f'\n§b{full_cmd}§r {help_msg}').h(f'点击填入{full_cmd}').c(RAction.suggest_command, full_cmd)

        msg = RTextList(
            RText(f'-------- §d{self.metadata.name}§a v{self.metadata.version}§r --------'),
            command_rtext('', '显示此条帮助'),
            command_rtext('reload', '重新加载直播转发线程'),
            command_rtext('config', '查看/修改直播间配置'),
        )
        src.reply(msg)

    def reload(self, src: CommandSource, *args):
        src.reply('正在重载直播间...')
        self.room.cancel()
        self.room.join()
        self.config = load_config(self.server)
        self.room = Room(self.config)
        self.room.start()
        src.reply('重载完毕!')
        self.need_reload = False

    def edit_conf(self, src: CommandSource, key: str, value: Union[int, str]):
        ok = False
        if key == 'id':
            if isinstance(value, int) or value.isdigit():
                self.config.id = int(value)
                self.need_reload = True
                ok = True
        elif key == 'nickname':
            self.config.nickname = str(value)
            ok = True

        if ok:
            save_config(self.server, self.config)
            src.reply(f'配置项{key}的值已设定为{value}')
            if self.need_reload:
                self.reload_tips(src)

    def list_listener(self, src: CommandSource):
        def get_color(key) -> RColor:
            if key in self.config.listener and key in self.room.listener:
                return RColor.green
            elif key not in self.config.listener and key not in self.room.listener:
                return RColor.gray
            else:
                return RColor.yellow

        def generate(key) -> RTextBase:
            event: Event = DanmakuEvents[key].value
            return RTextList(
                '-',
                RText(' [↑]', color=RColor.green).h('启用').c(RAction.run_command,
                                                              f'{PREFIX} config listener add {key}'),
                RText(' [↓]  ', color=RColor.red).h('禁用').c(RAction.run_command,
                                                              f'{PREFIX} config listener del {key}'),
                RText(event.msg, color=get_color(key)).h(f'{event.code}  {event.remark}'),
            )

        list(map(lambda key: src.reply(generate(key)), all_event_name))

    def modify_listener(self, src: CommandSource, action: str, key: str):
        action_map = {'add': self.config.listener.append, 'del': self.config.listener.remove}
        if action in action_map:
            action_map.get(action)(key)
            save_config(self.server, self.config)
            self.reload_tips(src, '事件监听器已更新')

    def reload_tips(self, src: CommandSource, reason: str = '检测到配置更改'):
        self.need_reload = True
        src.reply(RTextList(
            reason,
            ', 可能需要',
            RText('重载房间', color=RColor.green, styles=RStyle.bold).h('点击重载')
            .c(RAction.suggest_command, f'{PREFIX} reload'),
            '以同步配置'
        ))

    def color_panel(self, src: CommandSource):
        panel = RTextList(
            RText("来点颜色:\n"),
            RText("⬛ ", RColor.black),
            RText("⬛ ", RColor.dark_blue),
            RText("⬛ ", RColor.dark_green),
            RText("⬛ \n", RColor.dark_aqua),
            RText("⬛ ", RColor.dark_red),
            RText("⬛ ", RColor.dark_purple),
            RText("⬛ ", RColor.gold),
            RText("⬛ \n", RColor.gray),
            RText("⬛ ", RColor.dark_gray),
            RText("⬛ ", RColor.blue),
            RText("⬛ ", RColor.green),
            RText("⬛ \n", RColor.aqua),
            RText("⬛ ", RColor.red),
            RText("⬛ ", RColor.light_purple),
            RText("⬛ ", RColor.yellow),
            RText("⬛ ", RColor.white)
        )
        src.reply(panel)

    def send_danmaku(self, src: CommandSource, msg: str):
        self.room.send_danmaku(msg)
