# coding=utf-8

print("hello, world")

import requests
from bs4 import BeautifulSoup

def fetch_webpage_content(url):
    """发送网络请求并获取网页内容"""
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        response.encoding = response.apparent_encoding
        return response.text
    except requests.RequestException as e:
        print(f"请求网页时发生错误：{e}")
        return None

def extract_main_content(html):
    """解析HTML并提取正文内容"""
    soup = BeautifulSoup(html, 'html.parser')
    # 假设正文内容在 <div> 标签中，类名为 'main-content'
    ul_content = soup.find('ul', class_='bookList')

    if ul_content:
        li_list = ul_content.find_all("li")
        for li_item in li_list:
            a_tag = li_item.find("a")
            print(a_tag.text)
            print(a_tag["href"])

    # return main_content.get_text() if main_content else "未找到正文内容"

def main(url):
    """主函数，整合上述功能"""
    html_content = fetch_webpage_content(url)
    # with open("aaa.html", "w", encoding="utf-8") as f:
    #     f.write(html_content)
    #print(html_content)
    if html_content:
        main_text = extract_main_content(html_content)
        # print(main_text)
    else:
        print("无法获取网页内容。")

if __name__ == "__main__":
    url = "https://www.ppzuowen.com/book/shaoergushi/zhentanxiaogushi/"  # 替换为您要爬取的网页URL
    main(url)
