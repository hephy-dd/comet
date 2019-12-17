# Template for comet applications
#
# Copy this file to your custom COMET project and adjust application
# name, organization, version and package name. Also add additional
# package data and hidden imports to the analysis object.
#

import os
import comet

# Application name
name = 'comet'

# Application organization
organization = 'HEPHY'

# Application version
version = '0.4.0'

# Application package
package = 'comet'

# Paths
comet_root = os.path.join(os.path.dirname(comet.__file__))
comet_icon = os.path.join(comet_root, 'assets', 'icons', 'comet.ico')

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
                [StringStruct(u'CompanyName', u'{organization}'),
                StringStruct(u'FileDescription', u'{name}'),
                StringStruct(u'FileVersion', u'{version[0]}.{version[1]}.{version[2]}.0'),
                StringStruct(u'InternalName', u'{name}'),
                StringStruct(u'LegalCopyright', u'GPLv3'),
                StringStruct(u'OriginalFilename', u'{name}.exe'),
                StringStruct(u'ProductName', u'{name}'),
                StringStruct(u'ProductVersion', u'{version[0]}.{version[1]}.{version[2]}.0'),
                ])
            ]),
        VarFileInfo([VarStruct(u'Translation', [0, 1200])])
    ]
)
"""

# Pyinstaller entry point template
entry_point = """
from {package} import main
import sys
if __name__ == '__main__':
    sys.exit(main.main())
"""

# Create pyinstaller entry point
with open('entry_point.pyw', 'w') as f:
    f.write(entry_point.format(
        package=package,
    ))

# Create windows version info
with open('version_info.txt', 'w') as f:
    f.write(version_info.format(
        name=name,
        organization=organization
        version=version.split('.'),
        license='GPLv3',
    ))

a = Analysis(['entry_point.pyw'],
    pathex=[
      os.getcwd()
    ],
    binaries=[],
    datas=[
        (os.path.join(comet_root, 'widgets', '*.ui'), os.path.join('comet', 'widgets')),
        (os.path.join(comet_root, 'assets', 'icons', '*.svg'), os.path.join('comet', 'assets', 'icons')),
        (os.path.join(comet_root, 'assets', 'icons', '*.ico'), os.path.join('comet', 'assets', 'icons')),
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
    cipher=None,
    noarchive=False
)
pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=None
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
    icon=comet_icon,
)
