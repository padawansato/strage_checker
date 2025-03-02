# インストールガイド

このガイドでは、Storage Checkerアプリケーションのインストール方法と設定方法について説明します。

## 必要条件

Storage Checkerを使用するには、以下の環境が必要です：

- macOS 10.10以降
- Python 3.6以降
- pip（Pythonパッケージマネージャー）

## インストール方法

### 方法1: ビルド済みアプリケーションを使用する場合

1. [リリースページ](https://github.com/yourusername/storage_checker/releases)から最新のビルド済みアプリケーション（`StorageChecker.app.zip`）をダウンロードします。
2. ダウンロードしたZIPファイルを解凍します。
3. 解凍した`StorageChecker.app`をApplicationsフォルダにドラッグ＆ドロップします。
4. Finderからアプリケーションを起動します。

### 方法2: ソースコードからビルドする場合

1. リポジトリをクローンまたはダウンロードします：

   ```bash
   git clone https://github.com/yourusername/storage_checker.git
   cd storage_checker
   ```

2. 依存パッケージをインストールします：

   ```bash
   pip install -r requirements.txt
   pip install py2app
   ```

3. アプリケーションをビルドします：

   ```bash
   python setup.py py2app
   ```

4. ビルドが完了すると、`dist`ディレクトリに`StorageChecker.app`が生成されます。
5. 生成された`StorageChecker.app`をApplicationsフォルダにコピーするか、そのまま実行できます。

## 開発環境での実行方法

依存パッケージをインストールした後、以下のコマンドで直接実行できます：

```bash
python storage_checker.py
```

## ログイン時の自動起動設定

macOSにログインする際に自動的にStorage Checkerを起動するように設定するには：

1. macOSの「システム環境設定」を開きます。
2. 「ユーザとグループ」を選択します。
3. 「ログイン項目」タブを選択します。
4. 「+」ボタンをクリックします。
5. `StorageChecker.app`を選択して「追加」をクリックします。

これにより、次回のログイン時からStorage Checkerが自動的に起動します。

## トラブルシューティング

### アプリケーションが起動しない場合

1. macOSのセキュリティ設定を確認してください。「システム環境設定」→「セキュリティとプライバシー」で、アプリケーションの実行を許可する必要がある場合があります。

2. ターミナルからアプリケーションを実行して、エラーメッセージを確認してください：

   ```bash
   open /Applications/StorageChecker.app
   ```

### その他の問題

問題が解決しない場合は、[Issueページ](https://github.com/yourusername/storage_checker/issues)で報告してください。
