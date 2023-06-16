import requests


# ファイルのアップロード
def upload_file(url, file_path):
    """
    指定されたURLに指定されたファイルをアップロードします。

    Args:
        url (str): アップロード先のURL
        file_path (str): アップロードするファイルのパス

    Returns:
        None
    """
    # ファイルをバイナリモードで開く
    with open(file_path, "rb") as file:
        # POSTリクエストでファイルを送信
        response = requests.post(url, files={"file": file})

    # レスポンスのステータスコードが200（成功）の場合
    if response.status_code == 200:
        print("ファイルが正常にアップロードされました")
    else:
        # 失敗時のエラーメッセージを出力
        print("ファイルのアップロードに失敗しました:", response.text)


# ファイルのダウンロード
def download_file(url, filename):
    """
    指定されたURLから指定されたファイルをダウンロードします。

    Args:
        url (str): ダウンロード元のURL
        filename (str): ダウンロードしたファイルの保存先ファイル名

    Returns:
        None
    """
    # ダウンロード時にファイル名をパラメータとして指定
    params = {"filename": filename}
    # GETリクエストでファイルをダウンロード
    response = requests.get(url, params=params)

    # レスポンスのステータスコードが200（成功）の場合
    if response.status_code == 200:
        # ファイルをバイナリモードで書き込み用に開く
        with open(f"{filename}.new", "wb") as file:
            # レスポンスのコンテンツをファイルに書き込む
            file.write(response.content)
        print("ファイルが正常にダウンロードされました")
    else:
        # 失敗時のエラーメッセージを出力
        print("ファイルのダウンロードに失敗しました:", response.text)


# 例の使用法
# アップロード用のURL
# upload_url = "https://flask-api-35gspl32ea-uc.a.run.app/upload"
# # ファイルのアップロード
# upload_file(upload_url, "abc")

# ダウンロード用のURL
download_url = "https://flask-api-35gspl32ea-uc.a.run.app/download"
# ファイルのダウンロード
download_file(download_url, "abc")
