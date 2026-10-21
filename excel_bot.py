import os
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime

# 1. 加载密钥
load_dotenv()
api_key = os.getenv("ZHIPU_API_KEY")
client = OpenAI(api_key=api_key, base_url="https://open.bigmodel.cn/api/paas/v4/")

# 2. 读取 Excel 表格数据，并转为字符串
df = pd.read_excel('data.xlsx')
table_text = df.to_string(index=False)

print("正在把表格发给AI大脑分析...")

# 3. 让 AI 分析表格
resp = client.chat.completions.create(
    model='glm-4-flash',
    messages=[
        {'role': 'system', 'content': '你是一个资深的数据分析师。请用 Markdown 格式输出一份数据分析报告。要求包含一级标题、加粗的重点词、以及分点说明的亮点和问题'},
        {'role': 'user', 'content': f'以下是最近的销售数据：\n{table_text}'}
    ]
)

# 4. 保存分析报告
summary = resp.choices[0].message.content
today = datetime.now().strftime("%Y%m%d_%H%M")
file_name = f"销售分析报告_{today}.md"
with open(file_name, 'w', encoding='utf-8') as f:
    f.write(summary)

print(f"✅ 完成！数据报告已保存到 {file_name}")