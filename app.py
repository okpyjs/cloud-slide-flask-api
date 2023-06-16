import glob
import os
import uuid

from flask import Flask, request, send_file

from utils.PPTX import PPTX

app = Flask(__name__)


@app.route("/convert", methods=["POST"])
def upload_files():
    """
    ファイルをアップロードするエンドポイント

    Returns:
        str: レスポンスメッセージ
    """
    try:
        if "file" not in request.files:
            # リクエスト内に 'file' が含まれていない場合はエラーレスポンスを返す
            return "ファイルがアップロードされていません", 400

        files = request.files.getlist("file")

        for file in files:
            if file.filename == "":
                # ファイル名が空の場合は無視する
                continue

            file.save(file.filename + "new")

        return "ファイルが正常にアップロードされました"
    except Exception as e:
        # エラーハンドリング
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
    return


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
        return "remove all files", 200
    except Exception as e:
        print(e)

    # リクエストからファイル名を取得
    filename = request.args.get("filename")

    print(filename)

    if not filename:
        # ファイル名が指定されていない場合はエラーレスポンスを返す
        return "ファイル名がありません", 400

    file_path = filename

    try:
        # ファイルを削除する
        os.remove(file_path)
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
        file_list = glob.glob("assets" + "/**/*", recursive=True)
        # ファイルリストを文字列として返す (ステータスコード 200)
        return str(file_list), 200
    except Exception as e:
        # エラーメッセージを返す (ステータスコード 500)
        return "エラーが発生しました", 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
