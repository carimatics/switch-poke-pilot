import json
import subprocess

from switchpokepilot.core.utils.os import is_macos, is_windows


def _get_devices_macos():
    command = 'system_profiler SPCameraDataType -json'
    res = subprocess.run(command, stdout=subprocess.PIPE, shell=True)
    res_json = res.stdout.decode('utf-8')
    res_dict = json.loads(res_json)['SPCameraDataType']
    return [{'name': device['_name'], 'id': i} for i, device in enumerate(res_dict)]


def _get_device_windows():
    # XXX: ちゃんとデバイスのリストを取得する
    #      とりあえず現状は10個までのカメラに対応
    return [{'name': f"Camera {i}", 'id': i} for i in range(10)]


def get_devices() -> list[dict[str, str | int]]:
    if is_macos():
        return _get_devices_macos()
    if is_windows():
        return _get_device_windows()
    else:
        return []
