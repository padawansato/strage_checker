#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rumps
import psutil
import time
import os
import tempfile
import math
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

class StorageCheckerApp(rumps.App):
    def __init__(self):
        super(StorageCheckerApp, self).__init__("Storage", icon=None)
        self.menu = ["更新", "終了"]
        self.update_interval = 60  # 更新間隔（秒）
        self.temp_icon_file = None
        self.storage_info_key = "ストレージ情報"  # メニュー項目のキー
        self.update_storage_info()
        # 定期的な更新を設定
        rumps.Timer(self.update_storage_info, self.update_interval).start()

    def update_storage_info(self, sender=None):
        """ストレージ情報を更新し、アイコンとメニューを更新する"""
        # ルートディスク（/）の情報を取得
        disk_usage = psutil.disk_usage('/')
        
        # 空き容量の割合（%）
        free_percent = disk_usage.free / disk_usage.total * 100
        
        # 空き容量（GB）
        free_gb = disk_usage.free / (1024 ** 3)
        
        # 合計容量（GB）
        total_gb = disk_usage.total / (1024 ** 3)
        
        # メニュー項目を更新
        self.title = f"{free_gb:.1f}GB"
        
        # メニューの詳細情報を更新
        info_text = f"空き: {free_gb:.1f}GB / 合計: {total_gb:.1f}GB ({free_percent:.1f}%)"
        
        # 既存のメニュー項目を削除（存在する場合）
        if self.storage_info_key in self.menu:
            del self.menu[self.storage_info_key]
        
        # 新しいメニュー項目を追加
        self.storage_info = rumps.MenuItem(self.storage_info_key)
        self.storage_info.title = info_text
        self.menu.insert_before("更新", self.storage_info)
        
        # アイコンを生成して設定
        icon_path = self.generate_icon(free_percent)
        self.icon = icon_path
    
    def generate_icon(self, free_percent):
        """空き容量の割合に基づいてアイコンを生成する"""
        # アイコンサイズ
        size = 22
        
        # 新しい画像を作成（透明背景）
        img = Image.new('RGBA', (size, size), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # 円の描画パラメータ
        margin = 2
        x, y = size // 2, size // 2
        r = (size // 2) - margin
        
        # 色の決定（空き容量が少ないほど赤くなる）
        if free_percent > 50:
            color = (0, 128, 0, 255)  # 緑
        elif free_percent > 20:
            color = (255, 165, 0, 255)  # オレンジ
        else:
            color = (255, 0, 0, 255)  # 赤
        
        # 円を描画（空き容量の割合に応じた扇形）
        start_angle = -90  # 上から始める
        end_angle = start_angle + (360 * (100 - free_percent) / 100)
        
        # 背景の円（薄いグレー）
        draw.ellipse([margin, margin, size - margin, size - margin], fill=(200, 200, 200, 128))
        
        # 扇形を描画（使用済み容量を表す）
        for angle in range(int(start_angle), int(end_angle)):
            x1 = x + r * math.cos(math.radians(angle))
            y1 = y + r * math.sin(math.radians(angle))
            draw.line([(x, y), (x1, y1)], fill=color, width=2)
        
        # 一時ファイルに保存
        if self.temp_icon_file:
            try:
                os.unlink(self.temp_icon_file)
            except (OSError, IOError):
                pass
        
        # 新しい一時ファイルを作成
        fd, temp_filename = tempfile.mkstemp(suffix='.png')
        os.close(fd)
        
        # 画像を一時ファイルに保存
        img.save(temp_filename, format='PNG')
        self.temp_icon_file = temp_filename
        
        return temp_filename
    
    @rumps.clicked("更新")
    def refresh(self, _):
        """手動更新ボタンのハンドラ"""
        self.update_storage_info()
    
    @rumps.clicked("終了")
    def quit(self, _):
        """アプリ終了ハンドラ"""
        # 一時ファイルを削除
        if self.temp_icon_file and os.path.exists(self.temp_icon_file):
            try:
                os.unlink(self.temp_icon_file)
            except (OSError, IOError):
                pass
        rumps.quit_application()

if __name__ == '__main__':
    app = StorageCheckerApp()
    app.run() 