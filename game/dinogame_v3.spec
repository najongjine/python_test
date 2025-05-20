# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['dinogame_v3.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('dino_walk_1.png', '.'),
        ('dino_walk_2.png', '.'),
        ('dino_jump_1.png', '.'),
        ('dino_jump_2.png', '.'),
        ('obstacle.png', '.')
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='dinogame_v3',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='dinogame_v3',
)
