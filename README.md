# VS_Unity_cache_del

## 概要

Visual Studioで作業していたらプロジェクトフォルダの容量の大体を占めてしまうipchやBrowswe.VC.dbを半自動的に削除するプログラムです

オプションで`.vs`フォルダやUnityの一時ファイルも削除できます

Unityプロジェクトの対象物は`Library`, `Temp`, `Obj`, `Build`, `Builds`, `Logs`, `UserSettings`, `.gradle`です。

## 使い方

1. このリポジトリをクローンする

```bash
git clone https://github.com/yuki57-46/Visual_Studio_cache_del.git
```

2. distフォルダにあるexeファイルを実行する
3. Visual Studioを使用したプロジェクトフォルダを選択する
4. 完了

## 注意

- このプログラムはプロジェクトフォルダ内のipchやBrowswe.VC.dbを削除します

## ライセンス

特に無いです。ご自由にお使いください。

## その他

- Python 3.12.8で作成しました
- このプログラムは自己責任でお願いします
- このプログラムを使用したことによるいかなる損害も補償しません
- 改善点や要望があればissueに書いてください
