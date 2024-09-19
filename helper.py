import os
import requests
import json
import re
from urllib.parse import unquote
import os

# 获取页面内容
def get_page_content(url):
    headers={
      "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
      "accept-encoding": "gzip, deflate, br, zstd",
      "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
      "cache-control": "max-age=0",
      "priority": "u=0, i",
      "referer": "https://www.luogu.com.cn/training/113",
      "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Microsoft Edge\";v=\"128\"",
      "sec-ch-ua-mobile": "?0",
      "sec-ch-ua-platform": "\"Windows\"",
      "sec-fetch-dest": "document",
      "sec-fetch-mode": "navigate",
      "sec-fetch-site": "same-origin",
      "sec-fetch-user": "?1",
      "upgrade-insecure-requests": "1",
      "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0"
    }
    response = requests.get(url,headers=headers)
    return response.text

def decode_json(encoded_str):
    # 解码URL编码的字符串
    decoded_str = unquote(encoded_str)
    return decoded_str

def analys_page_content():
    match = re.search(r'window._feInjection = JSON.parse\(decodeURIComponent\("([^"]+)"\)\);', get_page_content(url))
    a=decode_json(match.group(1))
    decoded_text = a.encode('utf-8').decode('unicode_escape')
    clean_text = decoded_text.replace('\n', '\\n').replace('\r', '\\r')
    clean_text = clean_text.replace('\\', '\\\\')
    #print(clean_text)
    data = json.loads(clean_text)

    return data


def problem_to_md(data):
    # 提取problem字段
    problem = data.get('currentData', {}).get('problem', {})
    
    # 获取标题、描述、输入格式、输出格式和示例等信息
    title = problem.get('title', '无标题')
    description = problem.get('description', '').replace('\\n\\n', '\n\n')  # 替换为 Markdown 段落分隔符
    input_format = problem.get('inputFormat', '').replace('\\n\\n', '\n\n')  # 替换为 Markdown 段落分隔符
    output_format = problem.get('outputFormat', '').replace('\\n\\n', '\n\n')  # 替换为 Markdown 段落分隔符
    samples = problem.get('samples', [])
    hint = problem.get('hint', '').replace('\\n\\n', '\n\n')  # 替换为 Markdown 段落分隔符

    # 构造Markdown格式
    md = f"# {title}\n\n"
    md += f"## 题目描述\n\n{description}\n\n"
    md += f"## 输入格式\n\n{input_format}\n\n"
    md += f"## 输出格式\n\n{output_format}\n\n"

    # 添加示例
    if samples:
        md += "## 示例\n\n"
        for i, sample in enumerate(samples):
            input_sample = sample[0].replace('\\n\\n', '\n\n').replace('\\n', '\n')
            output_sample = sample[1].replace('\\n\\n', '\n\n').replace('\\n', '\n')
            md += f"### 示例 {i + 1}:\n\n"
            md += f"**输入**:\n```\n{input_sample}\n```\n"
            md += f"**输出**:\n```\n{output_sample}\n```\n\n"

    # 提示部分
    if hint:
        md += f"## 提示\n\n{hint}\n\n"

    return md




if __name__ == '__main__':
    while True:
        url=input("请输入洛谷题目链接：")
        raw_data = get_page_content(url)
        data = analys_page_content()
        problem_info = data['currentData']['problem']
        pid = problem_info['pid']
        difficulty_raw = problem_info['difficulty']
        if difficulty_raw == 1:
            difficulty = '入门'
        elif difficulty_raw == 2:
            difficulty = '普及−'
        elif difficulty_raw == 3:
            difficulty = '普及 提高−'
        elif difficulty_raw == 4:
            difficulty = '普及+ 提高'
        elif difficulty_raw == 5:
            difficulty = '提高+ 省选−'
        elif difficulty_raw == 6:
            difficulty = '省选 NOI−'
        elif difficulty_raw == 7:
            difficulty = 'NOI NOI+ CTSC'
        elif difficulty_raw == 8:
            difficulty = '暂无评定'
        title = problem_info['title']
        folder_name = f"{pid} {difficulty} {title}"
        os.makedirs(folder_name, exist_ok=True)
        # 创建main.cpp
        main_cpp_path = os.path.join(folder_name, 'main.cpp')
        with open(main_cpp_path, 'w') as f:
            pass  # 创建空文件

        # 创建README.md
        description = problem_to_md(data)
        readme_md_path = os.path.join(folder_name, 'README.md')
        readme_content = f"# {title}\n\n{description}\n"
        with open(readme_md_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print(f"已生成 {folder_name} 文件夹")