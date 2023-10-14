import json
import subprocess

from switchpokepilot.utils.os import is_macos


def __get_devices_macos():
    command = 'system_profiler SPCameraDataType -json'
    res = subprocess.run(command, stdout=subprocess.PIPE, shell=True)
    res_json = res.stdout.decode('utf-8')
    res_dict = json.loads(res_json)['SPCameraDataType']
    return [{'name': device['_name'], 'id': i} for i, device in enumerate(res_dict)]


def get_devices() -> list[dict[str, str | int]]:
    if is_macos():
        return __get_devices_macos()
    else:
        return []
