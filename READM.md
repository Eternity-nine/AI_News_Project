# 🤖 AI 数据与图纸自动分析平台

本项目是基于 Python 和智谱大模型（GLM-4 / GLM-4V）开发的综合 AI 应用作品。

## 🌟 核心功能
1. **数据分析模块 (Streamlit + Pandas)**：
   - 支持在网页端上传 Excel 文件。
   - 内置数据降维逻辑，超大表格自动使用 Pandas 汇总压缩，防止大模型 Token 超限。
   - 自动生成柱状图，并调用大模型生成 Markdown 格式的商业分析报告。
2. **CAD 图纸多模态识别**：
   - 上传工厂 CAD 布局图截图。
   - 调用视觉大模型（GLM-4V）提取设备信息，自动生成 3D 建模任务清单。

## 🛠️ 技术栈
- 前端交互：Streamlit
- 数据处理：Pandas, Openpyxl
- AI 大模型：智谱 GLM-4 (文本), GLM-4V (视觉)
- 安全：python-dotenv 环境变量隔离