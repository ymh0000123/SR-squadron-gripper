import os
from dotenv import load_dotenv
import requests
import json

# 加载环境变量
load_dotenv()

# 获取环境变量
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", "your_default_access_token")
REPOS = os.getenv("REPOS", "owner/repo")  # 确保 REPOS 的格式是 "owner/repo"

# 构建 GitHub API 请求 URL
issuesurl = f"https://api.github.com/repos/{REPOS}/issues"

# 请求参数
params = {
    'page': '1',
    'per_page': '100'
}

# 发起 GET 请求
try:
    response = requests.get(
        issuesurl,
        params=params,
        headers={
            'Authorization': f'Bearer {ACCESS_TOKEN}'
        }
    )
    
    # 检查请求是否成功
    response.raise_for_status()
    
    # 解析 JSON 响应
    issues = response.json()
    
    # 处理数据：检查 labels 中是否包含 '显示'
    processed_issues = []
    for issue in issues:
        labels = [label['name'] for label in issue.get('labels', [])]
        if '显示' in labels:
            # 获取 timeline_url
            timeline_url = issue.get('timeline_url')
            if timeline_url:
                try:
                    # 请求 timeline_url
                    timeline_response = requests.get(
                        timeline_url,
                        headers={
                            'Authorization': f'Bearer {ACCESS_TOKEN}'
                        }
                    )
                    timeline_response.raise_for_status()
                    timeline_events = timeline_response.json()

                    # 提取时间线中的信息
                    timeline_data = []
                    for event in timeline_events:
                        timeline_data.append({
                            'created_at': event.get('created_at', '没有创建日期'),
                            'body': event.get('body', '没有正文'),
                            'actor_login': event.get('actor', {}).get('login', '没有作者登录名')
                        })

                except requests.exceptions.RequestException as e:
                    print(f"获取时间线数据时发生错误: {e}")
                    timeline_data = []

            else:
                timeline_data = []

            processed_issues.append({
                'title': issue.get('title', '没有标题'),
                'body': issue.get('body', '没有正文'),
                'id': issue.get('id', '没有ID'),
                'labels': labels,
                'user_login': issue.get('user', {}).get('login', '没有作者登录名'),
                'created_at': issue.get('created_at', '没有创建日期'),
                'timeline': timeline_data
            })
    
    # 将处理后的数据转换为 JSON
    processed_issues_json = json.dumps(processed_issues, ensure_ascii=False, indent=4)
    
    # 保存 JSON 数据到文件
    with open("interactivity.json", "w", encoding='utf-8') as file:
        file.write(processed_issues_json)
        
    print("数据已写入到 interactivity.json")

except requests.exceptions.RequestException as e:
    print(f"发生错误: {e}")
