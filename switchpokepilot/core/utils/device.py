import json
import subprocess

from switchpokepilot.core.utils.os import is_macos, is_windows, is_linux


def _get_camera_devices_default():
    # 適当にid 0から9までのカメラを返しておく
    return [{'name': f"Camera {i}", 'id': i} for i in range(10)]


def _get_camera_devices_macos():
    command = 'system_profiler SPCameraDataType -json'
    res = subprocess.run(command, stdout=subprocess.PIPE, shell=True)
    res_json = res.stdout.decode('utf-8')
    res_dict = json.loads(res_json)['SPCameraDataType']
    return [{'name': device['_name'], 'id': i} for i, device in enumerate(res_dict)]


def _get_camera_devices_windows():
    # XXX: ちゃんとデバイスのリストを取得する
    return _get_camera_devices_default()


def _get_camera_devices_linux():
    # XXX: ちゃんとデバイスのリストを取得する
    return _get_camera_devices_default()


def get_camera_devices() -> list[dict[str, str | int]]:
    if is_macos():
        return _get_camera_devices_macos()
    if is_windows():
        return _get_camera_devices_windows()
    if is_linux():
        return _get_camera_devices_linux()
    else:
        return _get_camera_devices_default()
