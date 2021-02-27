import os
import shutil
from flask import Flask, request, redirect, url_for, render_template, Markup
from werkzeug.utils import secure_filename
from tensorflow.keras.models import Sequential, load_model
from PIL import Image
import numpy as np
 
# 変数の宣言
UPLOAD_FOLDER = "./static/images/"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
 
labels = ["airplane", "automobile", "bird", "cat",
          "deer", "dog", "frog", "horse", "ship", "truck"]
n_class = 10
img_size = 32
n_result = 5
 
# Flaskのインスタンス化とUPLOAD_FOLDERの定義
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
 
# allowed_file()関数の定義
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
 
# Topページのルーティングとindex()関数の定義
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")
 
# 判定結果ページのルーティングとresult()関数の定義
@app.route("/result", methods=["GET", "POST"])
def result():
    if request.method == "POST":
        # ファイルの存在と形式を確認
        if "file" not in request.files:
            print("File doesn't exist!")
            return redirect(url_for("index"))
        file = request.files["file"]
        if not allowed_file(file.filename):
            print(file.filename + ": File not allowed!")
            return redirect(url_for("index"))
 
        # ファイルの保存
        if os.path.isdir(UPLOAD_FOLDER):
            shutil.rmtree(UPLOAD_FOLDER)
        os.mkdir(UPLOAD_FOLDER)
        filename = secure_filename(file.filename)  # ファイル名を安全なものに
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
 
        # 画像の読み込み
        image = Image.open(filepath)
        image = image.convert("RGB")
        image = image.resize((img_size, img_size))
        x = np.array(image, dtype=float)
        x = x.reshape(1, img_size, img_size, 3) / 255
        # 予測
        try:
            model = load_model("./cifer.h5", compile=False)
        except:
            print('Error:HDF5ファイルの読み込みに失敗しました。')
        # 予測
        y = model.predict(x)[0]
        sorted_idx = np.argsort(y)[::-1]  # 降順でソート
        result = ""
        for i in range(n_result):
            idx = sorted_idx[i]
            ratio = y[idx]
            label = labels[idx]
            result += "<p>" + str(round(ratio*100, 1)) + \
                "%の確率で" + label + "です。</p>"
        return render_template("result.html", result=Markup(result), filepath=filepath)
    else:
        return redirect(url_for("index"))
 
 
if __name__ == "__main__":
    app.run(debug=False)