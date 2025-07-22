# Anime_face_detection_api
アニメ顔検出API。フォーク元の [animede/anime_face_detection](https://github.com/animede/anime_face_detection) をDockerに載せてWeb APIとして整備したもの。

# 利用方法
## 1. ビルド
```sh
docker compose build
```

チェックポイントのダウンロードもDockerfileの中で行っている。

## 2. 起動
```sh
docker compose up -d
```

8081番ポートでAPIが待ち受け開始する。

## 3. 動作確認
```sh
$ curl -s "http://localhost:8081/face/" -F "file=@test.png" | jq
{
  "character_count": 1,
  "image_size": [
    1198,
    1800
  ],
  "data": [
    {
      "score": 0.9974053502082825,
      "box": [
        377,
        252,
        697,
        528
      ],
      "label": "girl"
    }
  ]
}
```

画像ファイルだと決め打ちしてOpenCVに渡して処理しているため `Content-Type` の指定は必須ではない。
