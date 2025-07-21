# Anime_face_detection
高精度アニメ顔検出SSD

### ビルド
```sh
$ docker compose build
```

### checkpointのダウンロード
[UZUKI/webapp1 at main](https://huggingface.co/UZUKI/anime-face-detection/tree/main) から `ssd_best8.pth` をダウンロードして `weights/` に配置。

このディレクトリはコンテナに含まれずマウントするだけなので他のコンテナ等と使い回せる。

### 起動
```sh
$ docker compose up -d
```

8081番ポートで待ち受け開始

### テスト
（ここはそのうち直す）

```
$ docker compose exec web python face_d_api_client_test.py --test 3 --filename image/test1.jpg
```

これで結果が返ってくればOK
