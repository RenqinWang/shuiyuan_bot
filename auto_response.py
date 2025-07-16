import requests
import time
from utils import *
from LLM import call_llm

# --- 配置信息 ---
# 自动回复的内容
AUTO_REPLY_CONTENT = "感谢您的提及！周可儿收到啦！"
# 匹配的字符串
SPECIAL_CONTENT = "@周可儿 楼主是不是joker"

# 轮询间隔（秒）
POLLING_INTERVAL_SECONDS = 180

# 用于存储已处理的通知ID，避免重复回复
processed_notification_ids = set()

# 预设prompt
PRESET_PROMPT = "你是饮水思源论坛的活跃用户，请根据主楼内容，结合自己的风格，简要回复：\n"

def process_notifications(notifications):
    """处理获取到的通知"""
    global processed_notification_ids # 声明使用全局变量

    for notification in notifications:
        notification_id = notification.get("id")
        notification_type = notification.get("notification_type")
        is_read = notification.get("read")

        # 检查是否是未读的 @提及 (notification_type_id = 1)
        if notification_type == 1 and not is_read:
            if notification_id in processed_notification_ids:
                continue # 已经处理过，跳过

            topic_id = notification.get("topic_id")
            post_number = notification.get("post_number")

            print(f"\n--- 新的 @提及 (ID: {notification_id}) ---")
            print(f"  主题ID: {topic_id}, 帖子号: {post_number}")

            # 读取被@楼层内容
            post_id = notification.get("data", {}).get("original_post_id")
            at_content = get_post_content_by_id(topic_id, post_id)
            print(f"  被@楼层内容: {at_content}")

            # 判断内容是否为特殊指令
            if at_content and at_content.strip() == SPECIAL_CONTENT:
                print("检测到joker指令，调用process_joker...")
                reply_joker(topic_id, post_number)
                processed_notification_ids.add(notification_id)
                continue

            # 正常自动回复
            # if topic_id and post_number:
            #     print(f"  尝试回复主题 {topic_id} 的帖子 {post_number}...")
            #     reply_success = post_reply(
            #         topic_id=topic_id,
            #         raw_content=AUTO_REPLY_CONTENT,
            #         reply_to_post_number=post_number
            #     )
            #     if reply_success:
            #         processed_notification_ids.add(notification_id)
            #         print(f"  成功回复并标记通知 {notification_id} 为已处理。")
            #     else:
            #         print(f"  回复失败，通知 {notification_id} 将在下次轮询时重试。")
            # else:
            #     print(f"  无法获取主题ID或帖子号，跳过回复。")
        # 您可以在这里添加其他 notification_type_id 的处理逻辑，例如：
        # elif notification_type_id == 3 and not is_read: # 引用
        #     print(f"新引用通知: {notification.get('data', {}).get('original_post_id')}")

    # 将通知标记为已读
    if mark_read():
        return
    else:
        print(f"无法清除通知")

def reply_joker(topic_id, post_number):
    """
    处理joker指令：读取主楼内容，拼接prompt，调用大模型生成回复
    """
    try:
        main_content_raw = get_post_content_by_number(topic_id, 1)
        if not main_content_raw:
            reply_content = "未能获取主楼内容，无法生成智能回复。"
        else:
            # 调用大模型
            llm_reply = call_llm(main_content_raw)
            reply_content = f"大模型回复：{llm_reply}"

        reply_content += '''
        
        ------
        
        以上内容由AI自动生成，如有冒犯请多见谅🥺或联系我删除
        '''

        # 回复到当前@的楼层
        post_reply(
            topic_id=topic_id,
            raw_content=reply_content,
            reply_to_post_number=post_number
        )
        print("已完成joker指令回复。\n" + reply_content)
    except Exception as e:
        print(f"处理joker指令时出错: {e}")

def main_listener():
    print("Discourse @提及自动回复监听脚本启动...")
    print(f"当前用户: {DISCOURSE_API_USERNAME}")
    print(f"轮询间隔: {POLLING_INTERVAL_SECONDS} 秒")

    # 初始加载已处理的通知ID，避免重启后重复处理
    # 实际应用中，您可能需要将 processed_notification_ids 存储到文件或数据库中
    # 这里为了简单，每次启动都从空集合开始

    while True:
        print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] 正在检查新通知...")
        notifications_data = get_notifications()

        if notifications_data and "notifications" in notifications_data:
            # Discourse API 返回的通知是按时间倒序排列的，通常最新的在前面
            # 为了确保处理顺序，可以反转列表，或者只处理未读的
            process_notifications(notifications_data["notifications"])
        else:
            print("未能获取通知或没有新通知。")

        time.sleep(POLLING_INTERVAL_SECONDS)

if __name__ == "__main__":
    # 在运行前，请确保 DISCOURSE_API_KEY 已被替换为您的实际密钥
    if DISCOURSE_API_KEY == "YOUR_GENERATED_API_KEY_HERE":
        print("错误：请将 DISCOURSE_API_KEY 替换为您的实际 API 密钥！")
    else:
        main_listener()