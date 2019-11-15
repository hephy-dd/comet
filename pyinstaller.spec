# Template for comet applications

import os
import comet

# Application name
name = 'comet'

# Application version
version = '0.1.0'

# Path to comet package
comet_path = os.path.join(os.path.dirname(comet.__file__))

block_cipher = None

# Windows version info template
version_info = """
VSVersionInfo(
    ffi=FixedFileInfo(
        filevers=({version[0]}, {version[1]}, {version[2]}, 0),
        prodvers=({version[0]}, {version[1]}, {version[2]}, 0),
        mask=0x3f,
        flags=0x0,
        OS=0x4,
        fileType=0x1,
        subtype=0x0,
        date=(0, 0)
    ),
    kids=[
        StringFileInfo(
            [
            StringTable(
                u'000004b0',
                [StringStruct(u'CompanyName', u'HEPHY'),
                StringStruct(u'FileDescription', u'{name}'),
                StringStruct(u'FileVersion', u'{version[0]}.{version[1]}.{version[2]}.0'),
                StringStruct(u'InternalName', u'{name}'),
                StringStruct(u'LegalCopyright', u'{license}'),
                StringStruct(u'OriginalFilename', u'{name}.exe'),
                StringStruct(u'ProductName', u'{name}'),
                StringStruct(u'ProductVersion', u'{version[0]}.{version[1]}.{version[2]}.0'),
                ])
            ]),
        VarFileInfo([VarStruct(u'Translation', [0, 1200])])
    ]
)
"""

# Pyinstaller wrapper script
with open('comet.pyw', 'w') as f:
    f.write('from comet import main\n')
    f.write('import sys\n')
    f.write('if __name__ == '__main__':\n')
    f.write('    sys.exit(main.main())\n')

# Windows version info file
with open('version_info.txt', 'w') as f:
    f.write(version_info.format(
         name=name,
         version=version.split('.'),
         license='GPLv3',
    ))

a = Analysis(['comet.pyw'],
    pathex=[
      os.getcwd()
    ],
    binaries=[],
    datas=[
        (os.path.join(comet_path, 'widgets', '*.ui'), os.path.join('comet', 'widgets')),
        (os.path.join(comet_path, 'assets', 'icons', '*.svg'), os.path.join('comet', 'assets', 'icons')),
        # Add your package data here
    ],
    hiddenimports=[
        'pyvisa-sim',
        'pyvisa-py',
        'PyQt5.sip',
        # Add your hidden imports here
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)
pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=name,
    version='version_info.txt',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon=os.path.join(comet_path, 'assets', 'icons', 'comet.ico'),
)
