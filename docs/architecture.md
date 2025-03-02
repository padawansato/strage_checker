# アーキテクチャ

このドキュメントでは、C4モデルに基づいてStorage Checkerアプリケーションのアーキテクチャを説明します。

## レベル1: コンテキスト図

```mermaid
C4Context
    title Storage Checkerコンテキスト図
    
    Person(user, "macOSユーザー", "アプリケーションを使用してストレージ情報を確認するエンドユーザー")
    System(storageChecker, "Storage Checker", "ストレージ情報を表示するメニューバーアプリケーション")
    System_Ext(macOSFileSystem, "macOSファイルシステム", "ストレージ情報の取得元")
    
    Rel(user, storageChecker, "使用する")
    Rel(storageChecker, macOSFileSystem, "読み取る", "psutil")
```

**説明**:

- **macOSユーザー**: アプリケーションを使用してストレージ情報を確認するエンドユーザー
- **Storage Checker**: ストレージ情報を表示するメニューバーアプリケーション
- **macOSファイルシステム**: ストレージ情報の取得元

## レベル2: コンテナ図

```mermaid
C4Container
    title Storage Checkerコンテナ図
    
    Person(user, "macOSユーザー", "アプリケーションを使用してストレージ情報を確認するエンドユーザー")
    
    System_Boundary(storageChecker, "Storage Checker アプリケーション") {
        Container(menubarInterface, "メニューバーインターフェース", "Python, rumps", "macOSのメニューバーにアイコンと情報を表示")
        Container(storageMonitor, "ストレージ監視モジュール", "Python, psutil", "ファイルシステムの情報を取得")
    }
    
    System_Ext(macOSFileSystem, "macOSファイルシステム", "ストレージ情報の取得元")
    
    Rel(user, menubarInterface, "使用する")
    Rel(menubarInterface, storageMonitor, "情報の取得と表示")
    Rel(storageMonitor, macOSFileSystem, "読み取る", "psutil.disk_usage()")
```

**説明**:

- **メニューバーインターフェース**: rumpsライブラリを使用してmacOSのメニューバーにアイコンと情報を表示
- **ストレージ監視モジュール**: psutilライブラリを使用してファイルシステムの情報を取得

## レベル3: コンポーネント図

```mermaid
C4Component
    title Storage Checkerコンポーネント図
    
    Container_Boundary(storageChecker, "Storage Checker アプリケーション") {
        Component(menubarUI, "メニューバーUI", "Python, rumps", "StorageCheckerApp クラス")
        Component(storageInfo, "ストレージ情報取得", "Python, psutil", "update_storage_info メソッド")
        Component(iconGenerator, "アイコン生成モジュール", "Python, PIL", "generate_icon メソッド")
    }
    
    System_Ext(macOSFileSystem, "macOSファイルシステム", "ストレージ情報の取得元")
    
    Rel(menubarUI, storageInfo, "情報の取得と表示")
    Rel(menubarUI, iconGenerator, "アイコン生成を要求")
    Rel(storageInfo, iconGenerator, "空き容量情報を提供")
    Rel(storageInfo, macOSFileSystem, "読み取る", "psutil.disk_usage()")
```

**説明**:

- **メニューバーUI (StorageCheckerApp)**: rumpsを使用したメニューバーアプリケーションのメインクラス
- **ストレージ情報取得 (update_storage_info)**: psutilを使用してストレージ情報を取得するメソッド
- **アイコン生成モジュール (generate_icon)**: PILを使用して空き容量に応じたアイコンを動的に生成するメソッド

## レベル4: コード図

主要なクラスとメソッドの関係:

```mermaid
classDiagram
    class StorageCheckerApp {
        +__init__()
        +update_storage_info(sender)
        +generate_icon(free_percent)
        +refresh(_)
        +quit(_)
    }
    
    StorageCheckerApp --|> rumps.App
    
    note for StorageCheckerApp "__init__: メニュー項目の初期化と定期的な更新タイマーの設定"
    note for StorageCheckerApp "update_storage_info: ストレージ情報取得、メニュー更新、アイコン更新"
    note for StorageCheckerApp "generate_icon: 空き容量に応じたアイコン生成"
    note for StorageCheckerApp "refresh: 手動更新処理"
    note for StorageCheckerApp "quit: 一時ファイル削除とアプリ終了"
```

**主要なデータフロー**:

1. アプリケーション起動時に`__init__`が実行され、初期設定と定期更新タイマーが設定される
2. `update_storage_info`メソッドが呼び出され、ストレージ情報を取得
3. 取得した情報に基づいて`generate_icon`メソッドがアイコンを生成
4. メニューバーのアイコンとメニュー項目が更新される
5. 以降、タイマーまたは手動更新によって2〜4のプロセスが繰り返される 