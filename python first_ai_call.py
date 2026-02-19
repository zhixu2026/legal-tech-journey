# AI API调用学习笔记 - 2026.2.18

## 1. 环境搭建过程
- 使用的API平台：SiliconFlow（国内可用）
- 模型选择：Qwen/Qwen2.5-7B-Instruct（通义千问）

## 2. 代码核心逻辑
- 导入requests库发送HTTP请求
- 设置headers包含API密钥
- 构建payload包含模型参数和用户提示
- 解析JSON响应获取AI回答

## 3. 遇到的问题及解决
[pip命令无法使用，通过创建pip.bat包装器解决。]

## 4. 思考：AI在法律场景的应用
[这种调用方式可以用于自动生成法律文书摘要、初步法律咨询、合同审查等。]