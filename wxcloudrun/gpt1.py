from pathlib import Path
from openai import OpenAI

def test_file_extraction_and_chat_completion():
    # 用你的实际 API 密钥替换 "MOONSHOT_API_KEY"
    client = OpenAI(
        api_key="Y2xlNTY0a2JidmRqa2ZqazU3dDA6bXNrLUNSN0dGVmU0UHJvUzlialpGZnVjTzJud3FrNU0=",  # 确保替换为你的 API 密钥
        base_url="https://api.moonshot.cn/v1",
    )

    try:
        # 尝试上传文件并提取内容
        #file_object = client.files.create(file=Path("C:\Users\56881\Desktop\pdf-git\pdf0205\pdf-flask\wxcloudrun\pdf\yinbaodian.pdf"), purpose="file-extract")
        file_object = client.files.create(
            file=Path("C:\\Users\\56881\\Desktop\\pdf-git\\pdf0205\\pdf-flask\\wxcloudrun\\pdf\\Ajax入门.pdf"),
            purpose="file-extract")

        file_content = client.files.content(file_id=file_object.id).text

        # 构建请求消息
        messages=[
            {
                "role": "system",
                "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一些涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。",
            },
            {
                "role": "system",
                "content": file_content,
            },
            {"role": "user", "content": "针对 Ajax入门.pdf，根据里面的知识点，提供50道测试题目，都是选择题目。记得添加序号。返回json格式"},
        ]

        # 调用 chat-completion, 获取 kimi 的回答
        completion = client.chat.completions.create(
          model="moonshot-v1-128k",
          messages=messages,
          temperature=0.3,
        )

        print(completion.choices[0].message)
        print(completion.choices[0])
        print(completion)
    except Exception as e:
        print(f"An error occurred: {e}")

# 调用测试方法
if __name__ == "__main__":
    test_file_extraction_and_chat_completion()

