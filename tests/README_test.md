# Storage Checker テスト

このドキュメントでは、Storage Checkerアプリケーションのテスト方法について説明します。

## テスト戦略

Storage Checkerアプリケーションのテストは、以下の戦略に基づいて設計されています：

1. **ユニットテスト**: 個々のメソッドの機能を分離してテスト
   - `generate_icon`メソッド: 異なる空き容量の割合に対して正しいアイコンを生成するか
   - `update_storage_info`メソッド: ストレージ情報が正しく更新されるか
   - `refresh`メソッド: 手動更新ボタンが正しく機能するか
   - `quit`メソッド: アプリケーションの終了処理が正しく行われるか

2. **モックの活用**: 外部依存（psutil、ファイルシステム、rumps）をモック化
   - psutilのdisk_usage関数をモック化して様々なディスク使用状況をシミュレート
   - ファイル操作をモック化
   - rumpsライブラリをモック化（macOS専用のため）

## テスト実行方法

### 前提条件

テストを実行するには、以下のパッケージが必要です：

```
pytest
pytest-mock
pillow
psutil
```

これらのパッケージは、以下のコマンドでインストールできます：

```bash
pip install -r requirements-dev.txt
```

### テストの実行

テストを実行するには、プロジェクトのルートディレクトリで以下のコマンドを実行します：

```bash
pytest test_storage_checker.py -v
```

`-v`オプションを使用すると、詳細なテスト結果が表示されます。

### テストカバレッジの確認

テストカバレッジを確認するには、以下のコマンドを実行します：

```bash
pytest test_storage_checker.py --cov=storage_checker
```

このコマンドを実行するには、`pytest-cov`パッケージが必要です：

```bash
pip install pytest-cov
```

## テスト内容

### TestGenerateIcon

- `test_generate_icon_high_free_space`: 空き容量が多い場合（50%以上）のアイコン生成をテスト
- `test_generate_icon_medium_free_space`: 空き容量が中程度の場合（20%〜50%）のアイコン生成をテスト
- `test_generate_icon_low_free_space`: 空き容量が少ない場合（20%未満）のアイコン生成をテスト
- `test_generate_icon_cleanup_temp_file`: 一時ファイルのクリーンアップが正しく行われるかテスト

### TestUpdateStorageInfo

- `test_update_storage_info`: 通常のストレージ情報更新をテスト
- `test_update_storage_info_low_space`: 空き容量が少ない場合のストレージ情報更新をテスト

### TestRefresh

- `test_refresh_button`: 手動更新ボタンが正しく機能するかテスト

### TestAppQuit

- `test_quit_with_temp_file`: 一時ファイルがある場合の終了処理をテスト
- `test_quit_without_temp_file`: 一時ファイルがない場合の終了処理をテスト 