# Shuiyuan Bot

本项目主要用于与上海交通大学“水源社区”论坛（Discourse）进行自动化交互，包含自动回复、内容获取、API密钥生成等功能，并集成了大语言模型（LLM）用于智能回复。

## LLM.py
封装了调用 OpenAI/DeepSeek 大语言模型的接口，主要用于根据特定 prompt 生成模拟“水源社区”风格的智能回复。
## settings.py
存放所有项目用到的配置参数，包括 Discourse 论坛和 LLM 的 API 密钥、模型、URL 及部分示例 prompt 内容。
## auto_response.py
自动监听 Discourse 论坛 @通知，并根据特定规则自动回复。此脚本可部署于服务器。
## utils.py
工具函数集合，封装了与 Discourse 论坛的 API 交互，包括获取帖子内容、获取通知、发布回复、标记通知已读等功能。

# 手动运行工具：
## getRaw.py
命令行工具，输入 Discourse 帖子 URL，自动解析 topic_id 和楼层号，获取并输出原始内容（raw）。
## testLLM.py
用于测试 LLM 智能回复功能的脚本，包含大量 prompt 示例和测试用例，便于调试和验证回复效果。
## script.py
用于生成 Discourse 用户 API Key 的脚本。代码来源：https://shuiyuan.sjtu.edu.cn/t/topic/123808

# 快速开始
* 运行 script.py 可生成并测试 Discourse 用户 API Key。
* 配置 settings.py 中的 API 密钥和参数。
* 通过 testLLM.py 测试 LLM 智能回复效果。
