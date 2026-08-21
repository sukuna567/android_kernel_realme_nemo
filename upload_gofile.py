import sys
import json
import urllib.request
import requests

def upload_to_gofile(file_path):
    # 1. Get best server
    resp = requests.get('https://api.gofile.io/servers')
    data = resp.json()
    if data['status'] != 'ok':
        raise Exception(f"Failed to get Gofile server: {data}")
    
    server = data['data']['servers'][0]['name']
    upload_url = f"https://{server}.gofile.io/contents/uploadfile"
    print(f"Uploading {file_path} to {upload_url}...")

    with open(file_path, 'rb') as f:
        files = {'file': f}
        upload_resp = requests.post(upload_url, files=files)
        res_data = upload_resp.json()
        if res_data['status'] == 'ok':
            download_page = res_data['data']['downloadPage']
            print(f"SUCCESS: {download_page}")
            return download_page
        else:
            raise Exception(f"Upload failed: {res_data}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 upload_gofile.py <path_to_file>")
        sys.exit(1)
    file_path = sys.argv[1]
    url = upload_to_gofile(file_path)
    print(f"Gofile Link: {url}")
