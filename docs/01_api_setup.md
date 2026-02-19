# AI API调用学习笔记 - 2026.2.19

## 1. 环境搭建过程
- 使用的API平台：SiliconFlow（国内可用）
- 模型选择：Qwen/Qwen2.5-7B-Instruct（通义千问）

## 2. 代码核心逻辑
- 导入requests库发送HTTP请求
- 设置headers包含API密钥
- 构建payload包含模型参数和用户提示
- 解析JSON响应获取AI回答

## 3. 遇到的问题及解决
- 最初 pip 命令不可用，因为系统存在多个Python版本冲突。通过创建 `pip.bat` 包装器，强制使用 `python -m pip` 解决。
- Git 未安装，安装时选择“从命令行使用Git”选项，确保PATH配置正确。
- 首次推送时遇到 SSL 证书错误，通过 `git config --global http.sslVerify false` 临时绕过，后续可重新开启。

## 4. 思考：AI在法律场景的应用
这种API调用方式可以用于自动生成法律文书摘要、初步法律咨询、合同条款分析等。未来可以结合特定领域的法律知识库，打造垂直领域的AI助手。