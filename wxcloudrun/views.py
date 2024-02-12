from datetime import datetime
from flask import render_template, request, jsonify
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response

from pathlib import Path
from openai import OpenAI

from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
import requests

app = Flask(__name__)


@app.route('/')
def index():
    """
    :return: 返回index页面
    """
    return render_template('index.html')


@app.route('/api/count', methods=['POST'])
def count():
    """
    :return:计数结果/清除结果
    """

    # 获取请求体参数
    params = request.get_json()

    # 检查action参数
    if 'action' not in params:
        return make_err_response('缺少action参数')

    # 按照不同的action的值，进行不同的操作
    action = params['action']

    # 执行自增操作
    if action == 'inc':
        counter = query_counterbyid(1)
        if counter is None:
            counter = Counters()
            counter.id = 1
            counter.count = 1
            counter.created_at = datetime.now()
            counter.updated_at = datetime.now()
            insert_counter(counter)
        else:
            counter.id = 1
            counter.count += 1
            counter.updated_at = datetime.now()
            update_counterbyid(counter)
        return make_succ_response(counter.count)

    # 执行清0操作
    elif action == 'clear':
        delete_counterbyid(1)
        return make_succ_empty_response()

    # action参数错误
    else:
        return make_err_response('action参数错误')


@app.route('/api/count', methods=['GET'])
def get_count():
    """
    :return: 计数的值
    """
    counter = Counters.query.filter(Counters.id == 1).first()
    return make_succ_response(0) if counter is None else make_succ_response(counter.count)


@app.route('/file_extraction_and_chat_completion', methods=['POST'])
def file_extraction_and_chat_completion():
    data = request.json
    fileID = data.get('fileID')

    if not fileID:
        return jsonify({"error": "No fileID provided"})

    # 假设get_download_url是获取文件下载链接的函数，你需要根据实际情况实现它
    download_url = get_download_url(fileID)
    if not download_url:
        return jsonify({"error": "Failed to get download URL"})

    # 下载文件
    response = requests.get(download_url)
    if response.status_code != 200:
        return jsonify({"error": "Failed to download file"})

    # 假设保存到临时文件进行处理
    temp_path = f'/tmp/{os.path.basename(download_url)}'
    with open(temp_path, 'wb') as temp_file:
        temp_file.write(response.content)

    # 这里调用OpenAI API进行内容提取，假设已经实现
    extracted_content = extract_content_with_openai(temp_path)

    # 清理临时文件
    os.remove(temp_path)

    return jsonify({"extractedContent": extracted_content})

def get_download_url(fileID):
    # 实现根据fileID获取下载链接的逻辑
    return "https://example.com/path/to/file"

def extract_content_with_openai(file_path):
    # 使用OpenAI进行内容提取的逻辑
    # 返回提取的内容
    return "Extracted content here"