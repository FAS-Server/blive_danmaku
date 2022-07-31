from bilibili_api import sync
from bilibili_api.live import LiveDanmaku
import json
import time
import os


def check_and_create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


if __name__ == '__main__':
    room_id = 0
    while True:
        try:
            room_id = int(input('请输入房间号码:'))
        except ValueError:
            print('格式错误!')
            continue
        except KeyboardInterrupt:
            exit(0)
        break
    stream = LiveDanmaku(room_display_id=room_id)
    room_path = os.path.join('../output', str(room_id))

    @stream.on('ALL')
    async def on_all_event(event):
        event_type = event["type"]
        print(f'接收到事件: {event_type}')
        file_path = os.path.join(room_path, event_type)
        file_name = f"{event_type}_{time.strftime('%Y%m%d_%H%M%S', time.localtime())}.json5"
        try:
            check_and_create_folder(file_path)
            with open(os.path.join(file_path, file_name).replace('\\', '/'), 'w', encoding='utf8') as f:
                print('已保存至', f.name)
                json.dump(event, f, indent=4, ensure_ascii=False)
        except KeyboardInterrupt:
            pass

    try:
        sync(stream.connect())
    except KeyboardInterrupt:
        exit(0)
