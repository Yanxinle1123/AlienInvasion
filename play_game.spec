# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['play_game.py'],
    pathex=[],
    binaries=[],
    datas=[('images/*.bmp', 'images')],
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
    name='play_game',
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
    bundle_identifier='lele.play_game.app'
)
app = BUNDLE(
    exe,
    name='play_game.app',
    icon='images/alien_invasion_game_img.ico',
    bundle_identifier='lele.play_game.app'
)
