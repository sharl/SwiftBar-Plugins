## SwiftBar-Plugins

[SwiftBar](https://swiftbar.app/) の自作プラグイン

### amedas.10m.py

#### 設定ファイル `~/.amedas` 書式
```
14163
```
[アメダス](https://www.jma.go.jp/bosai/amedas/#area_type=japan&area_code=010000)の観測地点コードを記述します。
`14163` は[札幌](https://www.jma.go.jp/bosai/amedas/#amdno=14163)です。
[東京](https://www.jma.go.jp/bosai/amedas/#amdno=44132)は `44132` です。
*#amdno=数字* が観測地点コードになります。

### hamu.py

#### 設定ファイル `~/.location` 書式
```
https://weather.yahoo.co.jp/weather/zoomradar/?lat=43.06144807&lon=141.35373725&z=8
```
[雨雲レーダー](https://weather.yahoo.co.jp/weather/zoomradar/)で「地名や住所を入力」で検索した地点を中心に表示するため、「URLを表示」で *z=数字* までをコピーします。
数字は拡大率なので適宜調整してください。

### amesh.py

特に設定はありません。
