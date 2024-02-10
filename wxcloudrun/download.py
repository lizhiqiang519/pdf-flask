import requests
from pathlib import Path
import os


def download_file(file_url):
    # 解析文件名
    file_name = file_url.split('/')[-1]
    # 定义文件保存路径，这里假设你有一个名为'downloads'的目录
    save_path = Path('downloads') / file_name
    # 确保目录存在
    save_path.parent.mkdir(parents=True, exist_ok=True)

    # 下载文件
    try:
        response = requests.get(file_url, allow_redirects=True)
        response.raise_for_status()  # 确保请求成功
        # 写入文件
        with open(save_path, 'wb') as f:
            f.write(response.content)
        return str(save_path), file_name
    except requests.RequestException as e:
        return f"An error occurred: {e}", None


# 用法示例
file_url = "http://example.com/path/to/Ajax入门.pdf"  # 替换为实际的文件URL
path, file_name = download_file(file_url)
print(f"File saved to {path} with name {file_name}")


# 调用测试方法
if __name__ == "__main__":
    download_file("https://7064-pdf-8g1671jo5043b0ee-1306680641.tcb.qcloud.la/Ajax%E5%85%A5%E9%97%A8.pdf?sign=e147bf1f8ab03e69720aa353db0154ab&t=1707568478")