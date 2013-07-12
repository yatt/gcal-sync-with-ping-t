# gcal sync with ping-t

## whats this
Ping-t (http://www.ping-t.com )の学習履歴をGoogle Calendarと同期するためのソフトウェアです。
日々の学習の実績をiPhoneなどのモバイルデバイスからカレンダーで確認することができ、モチベーションの向上に貢献します。

## 使用方法
app.sh をping-t内で使われている資格区分IDを引数にして呼び出すと、設定ファイルからアカウント情報などを読み込み、まだ同期されていない
学習履歴を同期します。

```sh
$ ./app.sh -h
usage: ./app.sh [-o] kbn

        kbn     name
     ----------------------
        8       CCNA
        25      CCNA-Security
        35      CCNA-Wireless
        38      CCNA-Voice
        20      CCNP-SWITCH
        29      CCNP-ROUTE
        27      CCNP-TSHOOT
        22      LPIC-101
        40      LPIC-102
        41      LPIC-201
        33      LPIC-202
        37      LPIC-301
$ ./app.sh 8   # CCNA(ver 3.5)の学習履歴を同期する
$ ./app.sh 22  # LPIC-101(ver 3.5)の学習履歴を同期する
```

cronやatコマンドなど、定期実行コマンドと合わせる事で、自動で学習履歴が同期される環境を作る事ができます。

例：cronで毎日23時にCCNAの問題集履歴を同期する
```cron
0 23 * * * /home/sync-t/gcal-sync-for-ping-t/app.sh 8
```


# フォルダ構成

app.sh  アプリケーションの実行シェルスクリプトです。
archive 取得した学習履歴CSVファイルの出力先です。
log     ログファイルの出力先です。
master  区分マスタや、登録済予定マスタ、アカウント情報マスタファイルなどを置きます。
script  バッチから呼び出されるPythonアプリケーションを置きます。

# ソフトウェア要件
- Python 2.7
