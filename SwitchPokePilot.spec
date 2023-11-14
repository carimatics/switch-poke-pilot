# -*- mode: python ; coding: utf-8 -*-

version = '0.1.8'
added_data = []

a = Analysis(
    ['switchpokepilot/__main__.py'],
    pathex=[],
    binaries=[],
    datas=added_data,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='SwitchPokePilot',
    icon='assets\icon\icon.ico',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
app = BUNDLE(
    exe,
    name='SwitchPokePilot.app',
    icon='assets/icon/icon.icns',
    bundle_identifier=None,
    version=version,
    info_plist={
        'NSCameraUsageDescription': 'This app requires camera to capture your switch game screen',
        'NSMicrophoneUsageDescription': 'This app requires microphone to capture your switch game screen',
    },
)
