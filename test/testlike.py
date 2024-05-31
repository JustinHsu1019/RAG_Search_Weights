import requests

def upload_and_download(file_path, download_path):
    with open(file_path, 'rb') as file:
        files = {'file': file}
        response = requests.post('http://127.0.0.1:5000/llmautotest', files=files)

        if response.status_code == 200:
            with open(download_path, 'wb') as f:
                f.write(response.content)
            print("檔案處理完成並下載至：", download_path)
        else:
            print("發生錯誤:", response.status_code)

if __name__ == "__main__":
    file_path = "test_60.xlsx"
    download_path = "final_0531.xlsx"
    upload_and_download(file_path, download_path)
