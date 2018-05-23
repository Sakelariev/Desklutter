# -*- mode: python -*-

block_cipher = None


a = Analysis(['../../src/main/python/desklutter/main.py'],
             pathex=['/Users/user/Dropbox/Python/Desklutter/Official/target/PyInstaller'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='Desklutter',
          debug=False,
          strip=False,
          upx=False,
          console=False , icon='/Users/user/Dropbox/Python/Desklutter/Official/target/Icon.icns')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='Desklutter')
app = BUNDLE(coll,
             name='Desklutter.app',
             icon='/Users/user/Dropbox/Python/Desklutter/Official/target/Icon.icns',
             bundle_identifier='com.example.tutorial')
