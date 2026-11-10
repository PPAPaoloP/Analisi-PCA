# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['AnalisiPCA_main.py'],                 # Il Cuore ed entry point della logica 
    pathex=[],
    binaries=[],
    datas=[],                               # Eventuali cartelle assets nel futuro 
    # Salvagenti vitali per nascondigli delle librerie data-science Windows base compilate!
    hiddenimports=[
        'openpyxl', 
        'sklearn',
        'sklearn.utils._typedefs', 
        'sklearn.neighbors._partition_nodes'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AnalisiPCA',                      # Nome puro che assumerà .EXE (es. AnalisiPCA.exe)
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,                    # Il package diventerà "Standalone".
    console=False,                          # Cruciale! Impedisce alle fastidiose GUI prompt nero (CMD) di avvilire dietro e le log!  
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None                               # Previsione per custom windows icons (.ico future)
)