## SwiftBar-Plugins

[SwiftBar](https://swiftbar.app/) の自作プラグイン

## 動作前提条件

- Python3+
```
pip3 install --upgrade requests bs4 Pillow Pyaudio
```

## プラグイン

### amedas.10m.py

#### 設定ファイル `~/.amedas` 書式
```
14163
```
[アメダス](https://www.jma.go.jp/bosai/amedas/#area_type=japan&area_code=010000)の観測地点コードを記述します。
`14163` は[札幌](https://www.jma.go.jp/bosai/amedas/#amdno=14163)です。
[東京](https://www.jma.go.jp/bosai/amedas/#amdno=44132)は `44132` です。
*#amdno=数字* が観測地点コードになります。

#### 設定ファイル`~/.amedas.settings` 書式
```
{
  "temp": -0.6,
  "snow": 79,
  "vvox": true
}
```
自動で作成され、次回のリフレッシュ時に気温や積雪量を比較して変化したときに [VOICEVOX](https://voicevox.hiroshiba.jp/) でしゃべるようになります。
VOICEVOX Engine と疎通が取れない場合は自動で `vvox` が `false` になるため、再度しゃべらせる場合は この設定ファイルを削除してみてください。

### hamu.py

#### 設定ファイル `~/.location` 書式
```
https://weather.yahoo.co.jp/weather/zoomradar/?lat=43.06144807&lon=141.35373725&z=8
```
[雨雲レーダー](https://weather.yahoo.co.jp/weather/zoomradar/)で「地名や住所を入力」で検索した地点を中心に表示するため、「URLを表示」で *z=数字* までをコピーします。
数字は拡大率なので適宜調整してください。

### amesh.py

特に設定はありません。
