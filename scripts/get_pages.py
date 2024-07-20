# coding=utf-8

print("hello, world")

import requests
from bs4 import BeautifulSoup

def fetch_webpage_content(url):
    """发送网络请求并获取网页内容"""
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        return response.text
    except requests.RequestException as e:
        print(f"请求网页时发生错误：{e}")
        return None

def extract_main_content(html):
    """解析HTML并提取正文内容"""
    soup = BeautifulSoup(html, 'html.parser')
    # 假设正文内容在 <div> 标签中，类名为 'main-content'
    main_content = soup.find('div', class_='main-content')
    return main_content.get_text() if main_content else "未找到正文内容"

def main(url):
    """主函数，整合上述功能"""
    html_content = fetch_webpage_content(url)
    if html_content:
        main_text = extract_main_content(html_content)
        print(main_text)
    else:
        print("无法获取网页内容。")

if __name__ == "__main__":
    url = "http://example.com"  # 替换为您要爬取的网页URL
    main(url)
