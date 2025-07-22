import argparse
import cv2
import numpy as np
import glob
from fastapi import FastAPI, File, UploadFile, Form
from starlette.responses import Response
from face_d_api_class import AnimeFaceDetect
import json
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# FastAPIアプリケーションの初期化
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)

# AnimeFace_detectクラスのインスタンス生成
AF = AnimeFaceDetect()

# コマンドライン引数の設定
parser = argparse.ArgumentParser(description='顔検出サーバー設定')
parser.add_argument("--host", type=str, default="0.0.0.0", help="サービスを提供するIPアドレスを指定")
parser.add_argument("--port", type=int, default=80, help="サービスを提供するポートを指定")
args = parser.parse_args()

# IPアドレスとポートの表示
print(f"IP={args.host}, PORT={args.port}")

# 顔検出を行うエンドポイント
@app.post("/face/")
async def face_det(file: UploadFile = File(...), confidence_level: float = 0.5, method: str = "standard", ratio:float = 1.72, shift:float = 0.32) -> JSONResponse:
    file_contents = await file.read()
    print(len(file_contents), " bytes received")
    print("confidence_level: ", confidence_level)
    print("method: ", method)
    print("ratio: ", ratio)
    print("shift: ", shift)
    
    nparr = np.frombuffer(file_contents, np.uint8)
    img_data = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img_data is None:
        return Response(content="Invalid image file", status_code=400)

    if method == "standard":
        dnum, rgb_img, predict_bbox, pre_dict_label_index, scores = AF.face_det(img_data, confidence_level)
    elif method == "square":
        dnum, rgb_img, predict_bbox, pre_dict_label_index, scores = AF.face_det_sq(img_data, confidence_level)
    elif method == "head":
        dnum, rgb_img, predict_bbox, pre_dict_label_index, scores = AF.face_det_head(img_data, ratio, shift, confidence_level)
    else:
        return Response(content='{"error": Invalid method parameter"}', status_code=400)

    print("predict_bbox: ", predict_bbox)
    height, width, _ = img_data.shape
    print(f"Image dimensions: {width} x {height}")

    labels = ["girl", "girl_low", "man", "man_low"]

    result = {"character_count": int(dnum), "image_size": [width, height], "data": []}
    for i in range(dnum):
        label_index = int(pre_dict_label_index[i])
        if label_index < 0 or label_index >= len(labels):
            label = "unknown"
        else:
            label = labels[label_index]

        result["data"].append({
            "score": float(scores[i]),
            "box": [int(x) for x in predict_bbox[i].astype(int)],
            "label": label
        })
    return Response(content=json.dumps(result), media_type="application/json; charset=utf-8")

# メイン関数
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=args.host, port=args.port)
