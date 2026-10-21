import streamlit as st
import os
import base64
from openai import OpenAI
from dotenv import load_dotenv

st.set_page_config(page_title="CAD图纸AI助手", page_icon="🏭")
st.title("🏭 工厂图纸 AI 辅助分析助手")
st.write("上传工厂 CAD 布局图的截图，AI 将自动提取设备信息并生成 3D 建模任务清单！")

# 加载密钥
load_dotenv()
api_key = os.getenv("ZHIPU_API_KEY")
client = OpenAI(api_key=api_key, base_url="https://open.bigmodel.cn/api/paas/v4/")

# 提示用户：不要上传涉密图纸
st.warning("⚠️ 安全提示：请勿上传公司涉密核心图纸，测试请使用打码或公开的示意图。")

# 图片上传组件
uploaded_file = st.file_uploader("请上传 CAD 图纸截图 (.jpg, .png)", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # 1. 在网页上展示用户上传的图片
    st.image(uploaded_file, caption="已上传的图纸", use_column_width=True)
    
    if st.button("✨ 开始 AI 分析图纸"):
        with st.spinner("AI 正在仔细端详图纸，请稍候..."):
            # 2. 将图片转换为 Base64 编码（这是让大模型看懂图片的关键）
            image_bytes = uploaded_file.read()
            base64_image = base64.b64encode(image_bytes).decode('utf-8')
            image_url = f"data:image/jpeg;base64,{base64_image}"
            
            # 3. 调用视觉大模型 GLM-4V
            resp = client.chat.completions.create(
                model='glm-4v', # 这里换成了视觉模型
                messages=[
                    {
                        'role': 'user',
                        'content': [
                            {"type": "text", "text": "你是一个专业的工厂布局规划师和3D建模师。请仔细观察这张图纸，提取图纸中的关键设备、区域划分，并生成一份用于3D建模的详细任务清单（包含需要建哪些模型、大概位置关系）。用 Markdown 格式输出。"},
                            {"type": "image_url", "image_url": {"url": image_url}}
                        ]
                    }
                ]
            )
            
            result = resp.choices[0].message.content
            
            # 4. 在网页展示结果
            st.success("✅ 分析完成！以下是 3D 建模任务清单：")
            st.markdown(result)