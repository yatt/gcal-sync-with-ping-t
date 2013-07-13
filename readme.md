# gcal sync with ping-t

## whats this
Ping-t (http://www.ping-t.com )の学習履歴をGoogle Calendarと同期するためのソフトウェアです。
日々の学習の実績をiPhoneなどのモバイルデバイスからカレンダーで確認することができ、モチベーションの向上に貢献します。

## インストール方法

```bash
# ソースコードの取得
$ git clone https://github.com/yatt/gcal-sync-with-ping-t.git
$ cd gcal-sync-with-ping-t.git
# アカウント情報マスタファイルの作成
$ sh
$ umask 066
$ cat > master/ping-t # Ping-tのアカウント情報
user-id password
^D
$ cat > master/google # Googleのアカウント情報
user@example.com password
^D
$ cat > master/calendar-id # Google CalendarのカレンダーID情報
hogeafa8asdIjhaliZLf@group.calendar.google.com
^D
$ exit
```


## 使用方法
app.sh をping-t内で使われている資格区分IDを引数にして呼び出すと、設定ファイルからアカウント情報などを読み込み、まだ同期されていない学習履歴を同期します。

また、CSVを出力するだけのオプションを指定することで、学習履歴を単にCSVで取得することもできます。

```bash
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

# LPIC-101(ver 3.5)の学習履歴を標準出力に書き出す
$ ./app.sh -o 22
22,1,2012/10/28 01:03,分野別,20,12,98,2,0
22,2,2012/11/28 10:12,分野別,20,18,95,5,0
22,3,2012/12/28 11:30,分野別,10,10,94,6,0
...

# CCNA(ver 3.5)の学習履歴を同期する
$ ./app.sh 8
$
```

cronやatコマンドなど、定期実行コマンドと合わせる事で、自動で学習履歴が同期される環境を作る事ができます。

例：cronで毎日23時にCCNAの問題集履歴を同期する
```cron
0 23 * * * /home/sync-t/gcal-sync-with-ping-t/app.sh 8
```

## 構成
### ファイル構成
|ファイル/フォルダ  |説明|
|:-----------------|:--|
|● app.sh|アプリケーションの実行シェルスクリプトです。|
|● archive/|取得した学習履歴CSVファイルの出力先です。|
|　○ KK_YYYYMMDD_HHMISS.csv|タイムスタンプYYYY/MM/DD HH:MI:SS時点での資格区分KKの学習履歴CSVファイルです。(例: 09_20130701_0812.csv)|
|● log/|ログファイル出力先です。|
|　○ log.txt|ログファイルです。|
|●master/|各種マスタファイルの置き場所です。|
|　○ ping-t|Ping-tのアカウントマスタです。ユーザIDとパスワードをスペース区切りで保存します。|
|　○ google|Googleのアカウントマスタです。ユーザIDとパスワードをスペース区切りで保存します。|
|　○ calendar_id|Google CalendarのカレンダーIDのアカウントマスタです。カレンダーIDを保存します。|
|　○ kbn.csv|資格区分のマスタファイルです。(資格区分ID,資格名,課金区分(無料:1 有料:2))で構成されます|
|　○ registered.csv|カレンダーに登録済みの予定を保存するファイルです。gcal.pyから読み書きされます。(区分,履歴順)で構成されます。|
|● script/|バッチから呼び出されるPythonアプリケーションを置きます。|
|　○ gcal.py|学習履歴CSVをstdinから読み込み、まだ記録されていない学習履歴をGoogle Calendarに登録します。|
|　○ ping-t.py|学習履歴CSVをstdoutに出力します。|

## ソフトウェア要件
- Python 2.7

## 依存ライブラリ
※ソースに同梱済みのためインストールは不要
- gdata-python-client http://code.google.com/p/gdata-python-client/
- mechanize http://wwwsearch.sourceforge.net/mechanize/
- BeautifulSoup http://www.crummy.com/software/BeautifulSoup/

## その他
### 出力CSV仕様
|項目|型|書式|説明|
|---|:-:|---|---|
|区分|int|-|資格区分|
|履歴順|int|-|資格区分での取組履歴順。 1からの連番|
|タイムスタンプ|timestamp|YYYY/MM/DD HH:MI:SS|問題集に取組み終わった時点でのタイムスタンプ。|
|実行モード|string|-|問題集、模擬問題など実行モード|
|問題数|int|-|取り組んだ問題の数。|
|正答数|int|-|取り組んだ問題のうち、正解した問題の数。|
|銅比率|int|-|区分内の全問題集のうち、銅メダルの数の比率。n%が銅メダル|
|銀比率|int|-|区分内の全問題集のうち、銀メダルの数の比率。n%が銀メダル|
|金比率|int|-|区分内の全問題集のうち、金メダルの数の比率。n%が金メダル|
