from setuptools import setup

APP = ['storage_checker.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'LSUIElement': True,  # メニューバーアプリとして実行（Dockに表示しない）
        'CFBundleName': 'StorageChecker',
        'CFBundleDisplayName': 'Storage Checker',
        'CFBundleIdentifier': 'com.example.storagechecker',
        'CFBundleVersion': '0.1.0',
        'CFBundleShortVersionString': '0.1.0',
    },
    'packages': ['rumps', 'psutil', 'PIL'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    name='StorageChecker',
    version='0.1.0',
    description='macOSのメニューバーにストレージ空き容量を表示するアプリ',
    author='Your Name',
    author_email='your.email@example.com',
) 