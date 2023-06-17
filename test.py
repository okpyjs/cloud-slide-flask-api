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


def upload_multiple_file(url, file_path_list):
    """
    指定したURLのエンドポイントに複数のファイルをアップロードする関数

    Parameters:
        url (str): APIエンドポイントのURL
        file_path_list (list): アップロードするファイルのパスが含まれるリスト

    Returns:
        None

    Raises:
        requests.exceptions.RequestException: リクエストエラーが発生した場合にスローされる例外
    """
    try:
        # ファイルパスリストからファイルオブジェクトのリストを作成
        files = [("file", open(x, "rb")) for x in file_path_list]

        # アップロードするファイルを含んだPOSTリクエストを送信
        response = requests.post(url, files=files)

        # レスポンスのステータスコードを確認して処理結果を出力
        if response.status_code == 200:
            print("ファイルが正常にアップロードされました。")
        else:
            print("ファイルのアップロードに失敗しました。ステータスコード:", response.status_code)
        return response.text

    except requests.exceptions.RequestException as e:
        # リクエストエラーが発生した場合のエラーハンドリング
        print("リクエストの送信中にエラーが発生しました:", e)


def delete_file(url, filename):
    """
    指定したURLのエンドポイントに対して、指定したファイルを削除する関数

    Parameters:
        url (str): APIエンドポイントのURL
        filename (str): 削除するファイルの名前

    Returns:
        None

    Raises:
        requests.exceptions.RequestException: リクエストエラーが発生した場合にスローされる例外
    """
    try:
        # 削除するファイル名をクエリパラメータとして設定
        params = {"filename": filename}

        # POSTリクエストを送信してファイルを削除
        response = requests.post(url, params=params)

        # レスポンスのステータスコードを確認して処理結果を出力
        if response.status_code == 200:
            print("ファイルが正常に削除されました。")
        else:
            print("ファイルの削除に失敗しました。ステータスコード:", response.status_code)

    except requests.exceptions.RequestException as e:
        # リクエストエラーが発生した場合のエラーハンドリング
        print("リクエストの送信中にエラーが発生しました:", e)


def retrieve_file(url):
    """
    指定されたURLからファイルを取得します。

    Args:
        url (str): 取得するファイルのURL。

    Returns:
        str: 取得したファイルのテキストデータ。
    """
    response = requests.get(url)  # URLにGETリクエストを送信してファイルを取得します
    print(response.text)  # 取得したファイルのテキストデータを表示します
    return response.text  # ファイルのテキストデータを返します


# 例の使用法
# アップロード用のURL
upload_url = "https://flask-api-35gspl32ea-uc.a.run.app/convert"
# upload_url = "http://localhost:8080/convert"
# ファイルのアップロード
print(upload_multiple_file(upload_url, ["assets_test/a", "assets_test/b"]))

# ダウンロード用のURL
# download_url = "https://flask-api-35gspl32ea-uc.a.run.app/download"
# download_url = "http://localhost:8080/download"
# # ファイルのダウンロード
# download_file(download_url, "abc")

# delete_url = "http://localhost:8080/delete"
# delete_file(delete_url, "assets/a")

# retrieve_url = "http://localhost:8080/retrieve"
# retrieve_file(retrieve_url)

# resp = requests.post(delete_url, params={"all": "true"})
# print(resp)

# import pandas
# df = pandas.read_csv("file_info.csv")
# df = df.head(0)
# df.to_csv("file_info.csv", header=True, index=False)
