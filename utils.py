import requests

from settings import *

def _get_api_headers():
    """构建API请求头"""
    return {
        "User-Api-Key": DISCOURSE_API_KEY,
        "User-Api-Username": DISCOURSE_API_USERNAME, #还是周可儿？
        # "Content-Type": "application/json",
        # "Accept": "application/json"
    }

def get_post_content_by_number(topic_id, post_number):
    headers = _get_api_headers()

    url = f"{DISCOURSE_BASE_URL}/t/{topic_id}.json"
    post_id = None
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # 如果状态码不是200，则抛出HTTPError异常

        topic_data = response.json()

        # 主楼通常是 post_stream.posts 列表中的第一个帖子，
        # 并且其 post_number 总是 1
        posts = topic_data.get("post_stream", {}).get("posts", [])

        for post in posts:
            if post.get("post_number") == post_number:
                post_id = post.get("id")
                break
    except Exception as e:
        print(e)

    if post_id is not None:
        return get_post_content_by_id(topic_id, post_id)
    else:
        return None

def get_post_content_by_id(topic_id, post_id):
    headers = _get_api_headers()
    url = f"{DISCOURSE_BASE_URL}/posts/{post_id}.json"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json().get("raw", "")
    except Exception as e:
        print(f"通过post_id获取帖子内容时出错: {e}")
        return None

def get_notifications():
    """获取当前用户的通知"""
    url = f"{DISCOURSE_BASE_URL}/notifications.json"
    headers = _get_api_headers()
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # 检查HTTP错误
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"获取通知失败: {e}")
        return None

def post_reply(topic_id, raw_content, reply_to_post_number=None):
    """
    发布回复
    :param topic_id: 主题ID
    :param raw_content: 回复的Markdown内容
    :param reply_to_post_number: 如果是回复某个特定帖子，提供该帖子的post_number
    """
    url = f"{DISCOURSE_BASE_URL}/posts.json"
    headers = _get_api_headers()
    payload = {
        "topic_id": topic_id,
        "raw": raw_content,
    }
    if reply_to_post_number:
        payload["reply_to_post_number"] = reply_to_post_number

    try:
        # 关键：不要用json.dumps，直接传data=payload
        response = requests.post(url, headers=headers, data=payload, timeout=10)
        response.raise_for_status()
        response_data = response.json()
        # Discourse 回复成功时不会有"success"字段，需判断有无"id"
        if response_data.get("id"):
            print(f"成功回复主题 {topic_id}，新帖子ID: {response_data.get('id')}")
            return True
        else:
            print(f"回复主题 {topic_id} 失败！")
            print(f"错误详情: {response_data.get('errors', '未知错误')}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"发布回复请求出错: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"HTTP 状态码: {e.response.status_code}")
            print(f"响应内容: {e.response.text}")
        return False

def mark_read():
    url = f"{DISCOURSE_BASE_URL}/notifications/mark-read.json"
    headers = _get_api_headers()
    try:
        response = requests.put(url, headers=headers, timeout=10)
        response.raise_for_status()  # 检查HTTP错误
        return True
    except requests.exceptions.RequestException as e:
        print(f"获取通知失败: {e}")
        return False