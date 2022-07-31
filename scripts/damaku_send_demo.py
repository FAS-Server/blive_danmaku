from requests import post
import time


def send_dm(room: int, msg: str, csrf: str, sessdata: str):
    payload = post(
        url='https://api.live.bilibili.com/msg/send',
        params={
            'msg': msg,
            'rnd': int(time.time()),
            'color': 16777215,
            'fontsize': 25,
            'mode': 1,
            'roomid': room,
            'bubble': 0,
            'csrf': csrf,
            'csrf_token': csrf
        },
        cookies={
            'SESSDATA': sessdata,
            'bili_jct': csrf
        }
    )
    print(payload.json())


if __name__ == '__main__':
    csrf = ''
    sessdata = ''
    room_id = 21562394
    while True:
        try:
            msg = input(f'{room_id} <- ')
            send_dm(room_id, msg, csrf, sessdata)
        except KeyboardInterrupt:
            exit(0)
