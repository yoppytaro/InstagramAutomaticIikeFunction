# InstagramAutomaticIikeFunction
 
"InstagramAutomaticIikeFunction"は、Pythonを使用したInstagramの自動いいねボットです。
 
# デモ
 
フォローしているアカウントの投稿に自動でいいねしていきます。
 
<img src="https://user-images.githubusercontent.com/58821058/106837491-ede5d480-66dd-11eb-9ced-cf399ad54a41.gif" width="600px">


# 使用方法

## 必要なもの

* chatworkのAPIキー、ルームキー
* Google Cloud Platformのサービスアカウントのjsonファイル
* 共有者に編集を許可しているスプレットシート
* スプレットシートの構成は、以下のように作成してください。
https://docs.google.com/spreadsheets/d/1VEhYHjI2Yr8edPn5Brc6Ssu4KlB2jKXViL1P3DFKTso/edit?usp=sharing


## 手順

1. このリポジトリーを任意のディレクトリにダウンロードします。
2. ４行目から19行目までのモジュールをインストールします。
3. 25行目にchateorkのルームキーを設定します。
4. 26行目にchateorkのAPIキーを設定します。
5. GCPのjsonファイルをsample.pyと同じディレクトリー内に移動します。
6. 44行目にスプレットシートのキーを設定します。
7. 51行目にjsonファイル名を設定します。
8. シート名「アカウント情報」のB2には、ユーザー名、C2には、パスワード、D2には、一日のマックスのいいね数を記入してください。

# エラー処理

chateorkにメッセージを送信するタイミング

* スプレットシートの処理中にエラーが発生した場合
* Instagramにログインできなかった場合
* いいねをしている時に何らかのエラーが発生した場合（スクリーンショット付きで送信）
 
# 注意事項

* インスタから機能制限を受ける可能性があります。
* 一日のいいね数は、200件、スリープ時間は、30分から60分を推奨しています。

