import glob
import json
import os
import threading
import time
import uuid

import pandas
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS, cross_origin

from utils.Drive import Drive
from utils.PPTX import PPTX
from utils.Slide import Slide

app = Flask(__name__)
CORS(
    app,
    resources={
        r".*": {"origins": ["http://localhost:3000", "http://109.123.229.249:3008"]}
    },
)


@app.route("/convert", methods=["POST"])
@cross_origin()
def upload_files():
    """
    ファイルのアップロードを処理するエンドポイントです。
    リクエストからファイルを取得し、指定のディレクトリに保存します。
    保存したファイルに関する情報をデータフレームに追加し、CSVファイルに保存します。
    その後、指定の形式に変換を行い、変換結果や使用したファイルの情報をレスポンスとして返します。

    Parameters:
        なし

    Returns:
        - 200: ファイルの変換が成功し、変換結果や使用したファイルの情報が含まれるレスポンス
        - 400: リクエストにファイルが含まれていない場合のエラーレスポンス
        - 500: アップロード中にエラーが発生した場合のエラーレスポンス
    """
    try:
        if "file" not in request.files:
            return "ファイルがアップロードされていません", 400

        # リクエストからファイルを取得
        files = request.files.getlist("file")

        result_file_name = str(uuid.uuid4())
        # ファイルに関する情報を格納する辞書を初期化
        file_dict = {
            "id": [],
            "name": [],
            "path": [],
            "result_file": [],
            "date": [],
        }

        # ファイルのアップロードと情報の収集
        for file in files:
            if file.filename == "":
                continue
            file_id = str(uuid.uuid4())
            file.save(f"assets/{file_id}")

            # ファイル情報を辞書に追加
            file_dict["id"].append(file_id)
            file_dict["name"].append(file.filename)
            file_dict["path"].append(f"assets/{file_id}")
            file_dict["result_file"].append(result_file_name)
            file_dict["date"].append(int(time.time()))

        # ファイル情報をデータフレームに変換してCSVファイルに保存
        file_df = pandas.DataFrame(file_dict)
        file_df.to_csv("file_info.csv", header=False, index=False, mode="a")

        # ファイルの変換を実行
        convert_status = PPTX(result_file_name, file_dict["path"]).convert()
        if convert_status:
            return (
                jsonify(
                    {
                        "status": "ok",
                        "result": f"assets/{result_file_name}",
                        "used_info": {
                            "from_files": file_dict["name"],
                            "from_file_ids": file_dict["id"],
                            "from_file_paths": file_dict["path"],
                        },
                    }
                ),
                200,
            )
        else:
            return f"サーバーエラー: {str(e)}", 500

    except Exception as e:
        return f"アップロード中にエラーが発生しました: {str(e)}", 500


@app.route("/download", methods=["GET"])
def download_file():
    """
    ファイルをダウンロードするエンドポイント

    Returns:
        file: ダウンロードするファイル
        str: エラーメッセージ
    """
    try:
        # リクエストからファイル名を取得
        filename = request.args.get("filename")

        if not filename:
            # ファイル名が指定されていない場合はエラーレスポンスを返す
            return "ファイル名がありません", 400

        # ファイルをダウンロードする
        return send_file(filename, as_attachment=True)

    except Exception as e:
        # エラーハンドリング
        return str(e), 404


def remove_all_files(directory):
    """
    指定されたディレクトリからすべてのファイルを削除します。

    Args:
        directory (str): ファイルを削除するディレクトリのパス。

    Returns:
        None
    """

    # ディレクトリ内のファイルのリストを取得します
    file_list = os.listdir(directory)

    for file_name in file_list:
        # ファイルのパスを作成します
        file_path = os.path.join(directory, file_name)
        # ファイルである場合のみ削除します
        if os.path.isfile(file_path):
            # ファイルを削除します
            os.remove(file_path)
    return "deleted all files", 200


@app.route("/delete", methods=["POST"])
def delete_file():
    """
    ファイルを削除するエンドポイント

    Returns:
        str: 処理結果メッセージ
    """
    try:
        all_falg = request.args.get("all")
        print(all_falg)
        if all_falg == "true":
            remove_all_files("assets")
            df = pandas.read_csv("file_info.csv")
            df = df.head(0)
            df.to_csv("file_info.csv", header=True, index=False, mode="w")
        return "remove all files", 200
    except Exception as e:
        print(e)

    # リクエストからファイル名を取得
    filename = request.args.get("filename")

    print(filename)

    if not filename:
        # ファイル名が指定されていない場合はエラーレスポンスを返す
        return "ファイル名がありません", 400

    file_path = f"assets/{filename}"

    try:
        df = pandas.read_csv("file_info.csv")
        # ファイルを削除する
        os.remove(file_path)
        df = df[df["id"] != filename]
        df.to_csv("file_info.csv", index=False, header=False)
        print(f"ファイル '{file_path}' を正常に削除しました。")
        return "ファイルが正常に削除されました"

    except FileNotFoundError:
        # ファイルが存在しない場合のエラーレスポンス
        print(f"ファイル '{file_path}' が存在しません。")
        return "指定されたファイルが存在しません", 400

    except Exception as e:
        # その他のエラーレスポンス
        print(f"ファイル '{file_path}' の削除中にエラーが発生しました: {e}")
        return "ファイルの削除中にエラーが発生しました", 400


@app.route("/retrieve", methods=["GET"])
def retrieve_files():
    """
    'assets' ディレクトリ内のファイルのリストを取得します。

    Returns:
        str: ファイルリストの文字列表現です。
    """
    try:
        folder_id = os.environ.get("SLIDE_FOLDER_ID")
        file_ids = Drive().get_file_ids(folder_id)
        return jsonify(file_ids), 200
    except Exception as e:
        # エラーメッセージを返す (ステータスコード 500)
        print(e)
        return "エラーが発生しました", 500


@app.route("/merge", methods=["POST"])
def merge_files():
    """
    'assets' ディレクトリ内のファイルのリストを取得します。

    Returns:
        str: ファイルリストの文字列表現です。
    """
    try:
        slides = request.json["slides"]
        print(slides)
        slides = json.loads(slides)
        file_name = f"result_{uuid.uuid4()}.pptx"
        threading.Thread(
            target=Slide().merge,
            args=(
                [x["id"] for x in slides],
                file_name,
            ),
        ).start()
        return file_name, 200
    except Exception as e:
        # エラーメッセージを返す (ステータスコード 500)
        print(e)
        return "エラーが発生しました", 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
