# main.spec
# PyInstaller SPEC file untuk membuat build photo2video (one-folder recommended)
# Catatan: letakkan file haarcascade_frontalface_default.xml di folder 'haarcascades' atau biarkan PyInstaller copy dari lokasi cv2

# --- konfigurasi ---
block_cipher = None

import os
import cv2

# Try to locate OpenCV haarcascade file on developer machine
haarcascade_src = None
try:
    # cv2.data.haarcascades usually points to opencv data folder
    haarcascade_src = os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_default.xml")
    if not os.path.exists(haarcascade_src):
        haarcascade_src = None
except Exception:
    haarcascade_src = None

# if you prefer to ship your own cascade, put it in ./haarcascades/haarcascade_frontalface_default.xml
local_haarcascade = os.path.join('haarcascades', 'haarcascade_frontalface_default.xml')
if os.path.exists(local_haarcascade):
    haarcascade_src = local_haarcascade

# If you also provide a ffmpeg.exe inside the project (recommended), set path here:
# e.g. place ffmpeg.exe into ./runtime/ffmpeg/ffmpeg.exe
ffmpeg_local = os.path.join('runtime', 'ffmpeg', 'ffmpeg.exe')
ffmpeg_datas = []
if os.path.exists(ffmpeg_local):
    # copy the whole runtime/ffmpeg folder into dist so MoviePy can use it
    ffmpeg_datas = [(ffmpeg_local, os.path.join('runtime', 'ffmpeg'))]

# Add any other data files you want to include (icons, assets)
datas = [
    ('assets', 'assets'),  # entire assets folder (icons, sample images)
]

# add haarcascade if found
if haarcascade_src:
    # copy into folder named 'haarcascades' inside dist
    datas.append((haarcascade_src, 'haarcascades'))

# add ffmpeg if present
for d in ffmpeg_datas:
    datas.append(d)

# hidden imports often needed for PyQt5 and moviepy/ffmpeg
hiddenimports = [
    'PyQt5',
    'PyQt5.QtCore',
    'PyQt5.QtGui',
    'PyQt5.QtWidgets',
    'sip',
    'moviepy',
    'imageio',
    'imageio_ffmpeg',
    'imageio.plugins.ffmpeg',
    'cv2',
    'numpy',
    'PIL',
    'skimage',  # optional if used
]

# If your project uses other dynamic imports, add them here
# hiddenimports += ['your_module']

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

# Package python bytecode
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Build EXE (we keep exclude_binaries=True then COLLECT copies binaries)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='photo2video',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,  # GUI app: hide console
    icon='assets/icon.ico' if os.path.exists('assets/icon.ico') else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    name='photo2video'
)
