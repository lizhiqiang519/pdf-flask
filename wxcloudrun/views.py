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
    app.logger.info("Processing new request")

    # 检查是否有文件在请求中
    if 'file' not in request.files:
        app.logger.error("No file part in the request")
        return jsonify({"error": "No file part"})

    file = request.files['file']
    role_content = request.form.get('roleContent', '')  # 从表单数据中获取roleContent
    app.logger.info(f"Received file: {file.filename} and roleContent: {role_content}")

    # 保存文件到临时目录
    filename = secure_filename(file.filename)
    file_path = os.path.join('/tmp', filename)
    file.save(file_path)
    app.logger.info(f"File saved to temporary path: {file_path}")

    # 使用你的实际API密钥替换下方字符串
    client = OpenAI(
        api_key="Y2xlNTY0a2JidmRqa2ZqazU3dDA6bXNrLUNSN0dGVmU0UHJvUzlialpGZnVjTzJud3FrNU0=",
        base_url="https://api.moonshot.cn/v1",
    )

    try:
        # 尝试上传文件并提取内容
        with open(file_path, 'rb') as f:
            file_object = client.files.create(
                file=f,
                purpose="file-extract")
            app.logger.info("File uploaded successfully for content extraction")

        file_content = client.files.content(file_id=file_object.id).text
        app.logger.info("Content extracted successfully")

        # 构建请求消息
        messages = [
            {"role": "system", "content": role_content},
            {"role": "system", "content": file_content},
            {"role": "user", "content": "针对文件内容，根据里面的知识点，提供相关测试题目。记得添加序号。返回json格式"},
        ]

        # 调用chat-completion，获取回答
        completion = client.chat.completions.create(
            model="moonshot-v1-128k",
            messages=messages,
            temperature=0.3,
        )
        app.logger.info("Chat completion successful")

        # 清理：删除服务器上的临时文件
        os.remove(file_path)
        app.logger.info("Temporary file removed")

        # 返回处理结果的字符串
        return jsonify(completion.choices[0].message['content'])

    except Exception as e:
        # 清理：删除服务器上的临时文件
        os.remove(file_path)
        app.logger.error(f"An error occurred: {e}")
        return jsonify({"error": str(e)})