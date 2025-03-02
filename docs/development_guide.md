# 開発ガイド

このガイドでは、Storage Checkerアプリケーションの開発環境のセットアップと貢献方法について説明します。

## 開発環境のセットアップ

### 必要条件

- macOS 10.10以降
- Python 3.6以降
- pip（Pythonパッケージマネージャー）
- Git（バージョン管理）

### 開発環境の準備

1. リポジトリをクローンします：

   ```bash
   git clone https://github.com/yourusername/storage_checker.git
   cd storage_checker
   ```

2. 仮想環境を作成して有効化します（推奨）：

   ```bash
   python -m venv venv
   source venv/bin/activate  # macOSの場合
   ```

3. 開発用の依存パッケージをインストールします：

   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

## プロジェクト構造

```plain
storage_checker/
├── storage_checker.py  # メインアプリケーションコード
├── setup.py            # py2appビルド設定
├── requirements.txt    # 依存パッケージリスト
├── requirements-dev.txt # 開発用依存パッケージリスト
├── tests/              # テストコード
├── docs/               # ドキュメント
└── dist/               # ビルド済みアプリケーション（生成される）
```

## 開発ワークフロー

### アプリケーションの実行

開発中にアプリケーションをテストするには：

```bash
python storage_checker.py
```

### テストの実行

単体テストを実行するには：

```bash
pytest
```

### アプリケーションのビルド

アプリケーションをビルドするには：

```bash
python setup.py py2app
```

ビルドが完了すると、`dist`ディレクトリに`StorageChecker.app`が生成されます。

## コーディング規約

- PEP 8スタイルガイドに従ってください。
- コメントは日本語で記述してください。
- 関数やクラスには適切なドキュメンテーション文字列（docstring）を追加してください。

## 貢献方法

1. リポジトリをフォークします。
2. 新しいブランチを作成します：

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. 変更を加えてコミットします：

   ```bash
   git commit -m "機能追加: 新機能の説明"
   ```

4. フォークしたリポジトリにプッシュします：

   ```bash
   git push origin feature/your-feature-name
   ```

5. プルリクエストを作成します。

## 機能拡張のアイデア

Storage Checkerの将来的な拡張アイデア：

1. 複数のディスクやパーティションの監視
2. ディスク使用量の詳細情報（ファイルタイプ別など）の表示
3. 空き容量が少なくなった場合の通知機能
4. ディスク容量の時間的変化のグラフ表示
5. 設定画面の追加（更新間隔、表示形式のカスタマイズなど）

## トラブルシューティング

### 開発中の一般的な問題

1. **依存関係のエラー**：

   ```bash
   pip install -r requirements.txt
   ```

   を実行して依存パッケージが最新であることを確認してください。

2. **アイコン生成の問題**：
   PILライブラリが正しくインストールされていることを確認してください。

3. **py2appビルドエラー**：
   最新バージョンのpy2appを使用していることを確認してください：

   ```bash
   pip install --upgrade py2app
   ```
