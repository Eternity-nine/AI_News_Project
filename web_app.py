import streamlit as st
import pandas as pd
import os
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime

# 设置网页的标题和图标
st.set_page_config(page_title="AI数据自动分析师", page_icon="🤖")
st.title("🤖 AI数据自动分析师")
st.write("上传你的 Excel 表格，AI 将自动为你生成深度分析报告！")

# 加载密钥
load_dotenv()
api_key = os.getenv("ZHIPU_API_KEY")
client = OpenAI(api_key=api_key, base_url="https://open.bigmodel.cn/api/paas/v4/")

# 网页上的文件上传组件
uploaded_file = st.file_uploader("请上传你的 Excel 文件 (.xlsx)", type=["xlsx"])

# 如果用户上传了文件
if uploaded_file is not None:
    # 1. 读取数据并展示在网页上
    df = pd.read_excel(uploaded_file)
    st.subheader("📊 数据预览：")
    st.dataframe(df) # 直接在网页上画出漂亮的表格
    # 新增：让网页直接展示柱状图
    st.subheader("📈 销售额趋势图：")
    st.bar_chart(data=df, x="产品", y="销售额")
    
    # 2. 用户点击按钮开始分析
    #  if st.button("✨ 开始 AI 分析"):
      # 【新增的逻辑】判断数据行数
if len(df) > 2:
    # 数据太大，先用 Pandas 做汇总压缩！
    # 按产品分组，把销售额加起来，只留两列
    summary_df = df.groupby('产品')['销售额'].sum().reset_index()
    table_text = summary_df.to_string(index=False)
    
    st.warning("⚠️ 检测到数据量较大，已自动使用 Pandas 进行汇总压缩，再把核心指标发给 AI。")
    st.dataframe(summary_df) # 在网页上展示汇总后的迷你表
else:
    # 数据小，直接发原始数据
    table_text = df.to_string(index=False)
            
            # 呼叫大模型
resp = client.chat.completions.create(
                model='glm-4-flash',
                messages=[
                    {'role': 'system', 'content': '你是一个资深的数据分析师。请用 Markdown 格式输出一份数据分析报告。要求包含一级标题、加粗的重点词、以及分点说明的亮点和问题。'},
                    {'role': 'user', 'content': f'以下是最近的销售数据：\n{table_text}'}
                ]
            )
summary = resp.choices[0].message.content
#去掉AI可能返回的markdown代码块标记
summary = summary.replace("```markdown", "")
summary = summary.replace("```", "")
summary = summary.strip()      
            # 3. 在网页上直接展示结果
st.success("✅ 分析完成！")
st.markdown(summary) # 网页会自动渲染 Markdown 格式
            
            # 4. 顺手把报告保存到本地
today = datetime.now().strftime("%Y%m%d_%H%M")
file_name = f"报告_{today}.md"
with open(file_name, 'w', encoding='utf-8') as f:
                f.write(summary)
st.info(f"报告已同步保存到本地文件夹：{file_name}")