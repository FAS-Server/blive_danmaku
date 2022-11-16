import os
from os import path
import json
import sys
from bilibili_api import sync

root_dir = path.dirname(path.dirname(__file__))
sys.path.append(root_dir)


from blive_danmaku.room import Room
from blive_danmaku.config import RoomConfig

async def dispatch_event(room: Room, event):
    etpye = event['type']
    try:
        cmd = eval(f'room.on_{str(etpye).lower()}')
        await cmd(event)
    except AttributeError:
        pass

async def main():
    room = Room(RoomConfig(id=114514, nickname='Mock'))
    sample_path = path.join(root_dir, 'sample_events')
    mock_files = map(lambda x: path.join(sample_path, x), os.listdir(sample_path))
    for filepath in mock_files:
        with open(filepath, 'r', encoding='utf8') as f:
            await dispatch_event(room, json.load(f))


if __name__ == '__main__':
    sync(main())
