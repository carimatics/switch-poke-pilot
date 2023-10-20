ASSETS_DIR = {
    "packed": "assets",
    "unpacked": "../assets",
}


def get_assets_dir(is_packed: bool):
    if is_packed:
        return ASSETS_DIR["packed"]
    else:
        return ASSETS_DIR["unpacked"]
