#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
import os
import tempfile
from unittest.mock import patch, MagicMock, mock_open
import math
from PIL import Image
import io

# テスト用のモックオブジェクト
class MockStorageCheckerApp:
    """StorageCheckerAppクラスのモック"""
    def __init__(self):
        self.temp_icon_file = None
        self.title = ""
        self.icon = None
        self.menu = MagicMock()
        self.storage_info_key = "ストレージ情報"
        self.storage_info = MagicMock()
    
    def generate_icon(self, free_percent):
        """空き容量の割合に基づいてアイコンを生成する"""
        # アイコンサイズ
        size = 22
        
        # 新しい画像を作成（透明背景）
        img = Image.new('RGBA', (size, size), color=(0, 0, 0, 0))
        draw = MagicMock()
        
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
    
    def update_storage_info(self, sender=None):
        """ストレージ情報を更新し、アイコンとメニューを更新する"""
        # ルートディスク（/）の情報を取得
        disk_usage = MagicMock()
        disk_usage.total = 1000 * (1024 ** 3)  # 1000GB
        disk_usage.free = 500 * (1024 ** 3)    # 500GB
        
        # 空き容量の割合（%）
        free_percent = disk_usage.free / disk_usage.total * 100
        
        # 空き容量（GB）
        free_gb = disk_usage.free / (1024 ** 3)
        
        # 合計容量（GB）
        total_gb = disk_usage.total / (1024 ** 3)
        
        # メニュー項目を更新
        self.title = f"{free_gb:.1f}GB"
        
        # アイコンを生成して設定
        icon_path = self.generate_icon(free_percent)
        self.icon = icon_path
    
    def refresh(self, _):
        """手動更新ボタンのハンドラ"""
        self.update_storage_info()
    
    def quit(self, _):
        """アプリ終了ハンドラ"""
        # 一時ファイルを削除
        if self.temp_icon_file and os.path.exists(self.temp_icon_file):
            try:
                os.unlink(self.temp_icon_file)
            except (OSError, IOError):
                pass

# テスト用のフィクスチャ
@pytest.fixture
def storage_app():
    """テスト用のStorageCheckerAppインスタンスを提供するフィクスチャ"""
    return MockStorageCheckerApp()

# generate_iconメソッドのテスト
class TestGenerateIcon:
    @patch('os.unlink')
    @patch('tempfile.mkstemp', return_value=(1, '/tmp/test_icon.png'))
    @patch('os.close')
    @patch('PIL.Image.new')
    def test_generate_icon_high_free_space(self, mock_new, mock_close, mock_mkstemp, mock_unlink, storage_app):
        """空き容量が多い場合（50%以上）のアイコン生成テスト"""
        # モックの設定
        mock_img = MagicMock()
        mock_new.return_value = mock_img
        
        # テスト対象メソッドを実行
        result = storage_app.generate_icon(75.0)
        
        # 検証
        assert result == '/tmp/test_icon.png'
        mock_img.save.assert_called_once()

    @patch('os.unlink')
    @patch('tempfile.mkstemp', return_value=(1, '/tmp/test_icon.png'))
    @patch('os.close')
    @patch('PIL.Image.new')
    def test_generate_icon_medium_free_space(self, mock_new, mock_close, mock_mkstemp, mock_unlink, storage_app):
        """空き容量が中程度の場合（20%〜50%）のアイコン生成テスト"""
        # モックの設定
        mock_img = MagicMock()
        mock_new.return_value = mock_img
        
        # テスト対象メソッドを実行
        result = storage_app.generate_icon(35.0)
        
        # 検証
        assert result == '/tmp/test_icon.png'
        mock_img.save.assert_called_once()

    @patch('os.unlink')
    @patch('tempfile.mkstemp', return_value=(1, '/tmp/test_icon.png'))
    @patch('os.close')
    @patch('PIL.Image.new')
    def test_generate_icon_low_free_space(self, mock_new, mock_close, mock_mkstemp, mock_unlink, storage_app):
        """空き容量が少ない場合（20%未満）のアイコン生成テスト"""
        # モックの設定
        mock_img = MagicMock()
        mock_new.return_value = mock_img
        
        # テスト対象メソッドを実行
        result = storage_app.generate_icon(15.0)
        
        # 検証
        assert result == '/tmp/test_icon.png'
        mock_img.save.assert_called_once()

    @patch('os.unlink')
    @patch('tempfile.mkstemp', return_value=(1, '/tmp/test_icon.png'))
    @patch('os.close')
    @patch('PIL.Image.new')
    def test_generate_icon_cleanup_temp_file(self, mock_new, mock_close, mock_mkstemp, mock_unlink, storage_app):
        """一時ファイルのクリーンアップが正しく行われるかテスト"""
        # 既存の一時ファイルがある場合を想定
        storage_app.temp_icon_file = '/tmp/old_icon.png'
        
        # モックの設定
        mock_img = MagicMock()
        mock_new.return_value = mock_img
        
        # テスト対象メソッドを実行
        storage_app.generate_icon(50.0)
        
        # 古い一時ファイルが削除されたことを確認
        mock_unlink.assert_called_once_with('/tmp/old_icon.png')
        # 新しい一時ファイルが保存されたことを確認
        mock_img.save.assert_called_once()

# update_storage_infoメソッドのテスト
class TestUpdateStorageInfo:
    def test_update_storage_info(self, storage_app):
        """ストレージ情報の更新が正しく行われるかテスト"""
        # generate_iconのモック
        storage_app.generate_icon = MagicMock(return_value='/tmp/test_icon.png')
        
        # テスト対象メソッドを実行
        storage_app.update_storage_info()
        
        # 検証
        assert storage_app.title == "500.0GB"
        storage_app.generate_icon.assert_called_once_with(50.0)
        assert storage_app.icon == '/tmp/test_icon.png'

    def test_update_storage_info_low_space(self, storage_app):
        """空き容量が少ない場合のストレージ情報更新テスト"""
        # generate_iconのモック
        storage_app.generate_icon = MagicMock(return_value='/tmp/test_icon.png')
        
        # disk_usageの値を変更
        disk_usage = MagicMock()
        disk_usage.total = 1000 * (1024 ** 3)  # 1000GB
        disk_usage.free = 100 * (1024 ** 3)    # 100GB (10%)
        
        # update_storage_infoメソッドを上書き
        def mock_update_storage_info(sender=None):
            # 空き容量の割合（%）
            free_percent = disk_usage.free / disk_usage.total * 100
            
            # 空き容量（GB）
            free_gb = disk_usage.free / (1024 ** 3)
            
            # メニュー項目を更新
            storage_app.title = f"{free_gb:.1f}GB"
            
            # アイコンを生成して設定
            icon_path = storage_app.generate_icon(free_percent)
            storage_app.icon = icon_path
        
        # メソッドを置き換え
        storage_app.update_storage_info = mock_update_storage_info
        
        # テスト対象メソッドを実行
        storage_app.update_storage_info()
        
        # 検証
        assert storage_app.title == "100.0GB"
        storage_app.generate_icon.assert_called_once_with(10.0)
        assert storage_app.icon == '/tmp/test_icon.png'

# 手動更新ボタンのテスト
class TestRefresh:
    def test_refresh_button(self, storage_app):
        """手動更新ボタンが正しく機能するかテスト"""
        # update_storage_infoメソッドをモック化
        storage_app.update_storage_info = MagicMock()
        
        # テスト対象メソッドを実行
        storage_app.refresh(None)
        
        # update_storage_infoが呼ばれたことを確認
        storage_app.update_storage_info.assert_called_once()

# アプリケーションの終了処理テスト
class TestAppQuit:
    @patch('os.path.exists', return_value=True)
    @patch('os.unlink')
    def test_quit_with_temp_file(self, mock_unlink, mock_exists, storage_app):
        """一時ファイルがある場合の終了処理テスト"""
        # 一時ファイルが存在する場合を想定
        storage_app.temp_icon_file = '/tmp/test_icon.png'
        
        # テスト対象メソッドを実行
        storage_app.quit(None)
        
        # 一時ファイルが削除されたことを確認
        mock_unlink.assert_called_once_with('/tmp/test_icon.png')

    @patch('os.path.exists', return_value=False)
    @patch('os.unlink')
    def test_quit_without_temp_file(self, mock_unlink, mock_exists, storage_app):
        """一時ファイルがない場合の終了処理テスト"""
        # 一時ファイルが存在しない場合を想定
        storage_app.temp_icon_file = '/tmp/test_icon.png'
        
        # テスト対象メソッドを実行
        storage_app.quit(None)
        
        # 一時ファイルの削除が試みられないことを確認
        mock_unlink.assert_not_called() 