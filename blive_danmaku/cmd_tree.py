from mcdreforged.api.command import *
from mcdreforged.api.types import PluginServerInterface

from blive_danmaku.constants import PREFIX
from blive_danmaku.user_interface import UserInterface
from blive_danmaku.danmaku_events import all_event_name


def register_command(server: PluginServerInterface, ui: UserInterface):
    def get_admin_node(cmd: str) -> Literal:
        return Literal(cmd).requires(lambda src: src.has_permission(3), lambda src: src.reply(ui.permission_deny))

    def get_conf_node(cmd: str) -> Literal:
        return Literal(cmd).runs(lambda src: ui.get_conf(src, cmd))
    root_node = Literal(PREFIX).runs(ui.help_msg).then(
        get_admin_node('reload').runs(ui.reload)
    ).then(
        get_admin_node('config').runs(ui.conf_menu).then(
            get_conf_node('id').then(
                Integer('id').runs(lambda src, ctx: ui.edit_conf(src, 'id', ctx['id']))
            )
        ).then(
            get_conf_node('nickname').then(
                Text('nickname').runs(lambda src, ctx: ui.edit_conf(src, 'nickname', ctx['nickname']))
            )
        ).then(
            get_conf_node('listener').runs(ui.list_listener).then(
                Literal('add').then(
                    Text('listener').suggests(lambda src, ctx: all_event_name).runs(lambda src, ctx: ui.modify_listener(src, 'add', ctx['listener']))
                )
            ).then(
                Literal('del').then(
                    Text('listener').suggests(lambda src, ctx: all_event_name).runs(lambda src, ctx: ui.modify_listener(src, 'del', ctx['listener']))
                )
            )
        )
    )

    root_node.then(
        get_admin_node('say').then(
            GreedyText('msg').runs(lambda src, ctx: ui.send_danmaku(src, ctx['msg']))
        )
    )
    server.register_command(root_node=root_node)
    server.register_help_message(PREFIX, '将B站直播间弹幕转发至游戏内')
