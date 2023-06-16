from flask import Flask, request, send_file

app = Flask(__name__)


@app.route("/upload", methods=["POST"])
def upload_file():
    """
    ファイルをアップロードするエンドポイント
    """
    if "file" not in request.files:
        # リクエスト内に 'file' が含まれていない場合はエラーレスポンスを返す
        return "ファイルがアップロードされていません", 400

    file = request.files["file"]
    file.save(file.filename)

    return "ファイルが正常にアップロードされました"


@app.route("/download", methods=["GET"])
def download_file():
    """
    ファイルをダウンロードするエンドポイント
    """
    filename = request.args.get("filename")
    if not filename:
        # リクエスト内に 'filename' が含まれていない場合はエラーレスポンスを返す
        return "ファイル名がありません", 400

    try:
        return send_file(filename, as_attachment=True)
    except Exception as e:
        # ファイルが見つからない場合やエラーが発生した場合はエラーレスポンスを返す
        return str(e), 404


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
