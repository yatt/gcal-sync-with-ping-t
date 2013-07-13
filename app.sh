#! /bin/sh

ROOT=$(dirname $0)
# ping-tアカウント
ACCOUNT_PING_T=$ROOT/master/ping_t
# gmailアカウント
ACCOUNT_GOOGLE=$ROOT/master/google
# カレンダーID
ACCOUNT_CAL_ID=$ROOT/master/calendar_id

# 最終更新時刻を出力
TIMESTAMP=$(date "+%Y%m%d_%H%M%S")

# pythonへのパス
PYTHON_PATH=$(which python)
# 履歴出力スクリプトへのパス
SCRIPT_HIST=$ROOT/script/ping_t.py
# カレンダー同期スクリプトへのパス
SCRIPT_GCAL=$ROOT/script/gcal.py

# ログファイル出力先
LOGFILE=$ROOT/log/log.txt


# 引数の解析
OUT_STDOUT_FLG=0
while getopts oh OPT
do
  case $OPT in
    "o" )
        OUT_STDOUT_FLG=1
        shift `expr $OPTIND - 1`
        ;;
    "h" )
        echo "usage: $(basename $0) [-o] kbn"
        echo ""
        # 区分の出力
        echo "\tkbn\tname"
        echo "     ----------------------"
        cat $ROOT/master/kbn.csv | cut -f1,2 -d, | sed -e 's/,/\t/g' -e 's/^/\t/g'
        echo ""
        exit 1
  esac
done

# 区分が与えられなければ終了
if [ $# -lt 1 ]; then
  echo "usage: $(basename $0) [-o] kbn"
  exit 1
fi


KBN=$1
OUTLOG(){
    echo "$TIMESTAMP $KBN (pid $$) $1" >> $LOGFILE
}

# 履歴の出力ファイルパス
ARCHIVE_TO=$ROOT/archive/$(echo $(printf "%02d" $KBN)_$TIMESTAMP).csv
if [ $OUT_STDOUT_FLG -ne 0 ]; then
    ARCHIVE_TO=/dev/stdout
fi

# 処理開始
OUTLOG "start"

# スクリプトを起動
$PYTHON_PATH $SCRIPT_HIST $(cat $ACCOUNT_PING_T) $KBN > $ARCHIVE_TO

# Google Calendar同期
if [ $OUT_STDOUT_FLG -eq 0 ]; then
    OUTLOG "gcal sync"
    $PYTHON_PATH $SCRIPT_GCAL $(cat $ACCOUNT_GOOGLE) $(cat $ACCOUNT_CAL_ID) < $ARCHIVE_TO
fi

# 処理終了
OUTLOG "end"
