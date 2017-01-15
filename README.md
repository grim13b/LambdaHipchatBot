# これはなに？
AWS Lambda から Hipchat にメッセージを投げる lambda function です。

# 前提
AWS の SNS と Lambda とその実行に関する IAM を設定する必要があります。 

# パッケージの作成方法
``` 
  $ pip install -r requirements.txt -t ./lib
  $ zip -rq9 lambda.zip * -x@exclude.txt
```
1. requirements.txt で書かれているライブラリを依存関係込みでダウンロードします。
2. ライブラリ一式込みで ZIP します。この時 exclude_files.txt に書かれたファイルは無視されます。

```
  $ ./build.sh
```
でも代用できます。

出来上がった lambda.zip を AWS Lambda にアップロードします。
 
# 設定に必要な環境変数
AWS Lambda では環境変数を設定できます。
これらは HipChat に Request を送るために必要なものです。予め準備してください。

* SENDER_NAME
  * 送信者名 (例 'ApplicationName Notifier')
* AUTH_TOKEN
  * 発言したい Room の HipChat API **V2** Authentication コード
* ROOM_ID
  * 発言したい Room の Room ID
