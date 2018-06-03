# Our Toot Suite

```
$ robo

  cleanup – 抽出したTootにはゴミ(HTMLタグなど)がふくまれているので除去する
  corpus – わかちがきしてmarkovで利用しやすいデータにする
  dec – NG_WORDSとEND_WORDSを解凍
  enc – NG_WORDSとEND_WORDSを圧縮
  export – MongoDBからTootを抽出してtextファイルに出力します
  help – Display usage
  learn – markovを用いて学習させる
  sentence – 文章を生成
  serve – APIサーバ起動
```


robo: https://github.com/tj/robo
