import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("ZHIPU_API_KEY")

client = OpenAI(api_key=api_key, base_url="https://open.bigmodel.cn/api/paas/v4/")

import sys

# 从 命令行参数获取文件名，如果没有传参数，默认用input.txt
file_name=sys.argv[1] if len (sys.argv)>1 else'input.txt'

with open(file_name, 'r', encoding='utf-8') as f:
    fake_news = f.read()

print("正在呼叫AI大脑，请稍候...")
resp = client.chat.completions.create(
    model='glm-4-flash',
    messages=[
        {'role': 'system', 'content': '你是一个专业的AI新闻编辑，请把搜索结果整理成简洁的今日AI新闻简报，要求分点列出。'},
        {'role': 'user', 'content': f'请阅读以下内容，并总结成一份简报：\n{fake_news}'}
    ]
)

summary = resp.choices[0].message.content
with open('news.txt', 'w', encoding='utf-8') as f:
    f.write(summary)

print("✅ 完成！新闻摘要已保存到 news.txt") 