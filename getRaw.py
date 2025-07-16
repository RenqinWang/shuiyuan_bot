from utils import *
import re
import sys

def getRaw(url):
    """
    输入Discourse帖子url，解析topic_id和可选楼层号，获取raw内容
    :param url: 形如 https://shuiyuan.sjtu.edu.cn/t/topic/386445?u=周可儿 或 https://shuiyuan.sjtu.edu.cn/t/topic/386445/1234
    :return: raw内容字符串
    """
    # 解析topic_id和可选楼层号
    # 支持 https://shuiyuan.sjtu.edu.cn/t/topic/386445 或 https://shuiyuan.sjtu.edu.cn/t/topic/386445/1234
    match = re.search(r'/t/[^/]+/(\d+)(?:/(\d+))?', url)
    if not match:
        print("无法解析topic_id，请检查url格式！")
        return None
    topic_id = int(match.group(1))
    if match.group(2):
        post_number = int(match.group(2))
    else:
        post_number = 1
    # 获取raw内容
    raw_content = get_post_content_by_number(topic_id, post_number)
    return raw_content

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python getRaw.py <Discourse帖子url>")
        sys.exit(1)
    url = sys.argv[1]
    raw = getRaw(url)
    if raw is not None:
        print(raw)
    else:
        print("未能获取raw内容")
