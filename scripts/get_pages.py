# coding=utf-8

# print("hello, world")
# 1、下载单个页面，返回字符串。
# 2、找到标题
# 3、找到正文（注意：正文中有粗体字）
# 4、写入 markdown 文件。

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

    return soup


def find_links(soup):
    # 假设正文内容在 <div> 标签中，类名为 'main-content'
    ul_content = soup.find('ul', class_='bookList')
    assert ul_content

    # if ul_content:
    base_url = "https://www.ppzuowen.com"
    rs = []
    li_list = ul_content.find_all("li")
    for li_item in li_list:
        a_tag = li_item.find("a")
        rs.append((a_tag.text, base_url + a_tag["href"]))
    
    return rs

def save_page(url):
    html_content = fetch_webpage_content(url)
    assert html_content

    page = extract_main_content(html_content)

    title = page.find("h2", class_="articleH2")
    print(title.text)


def main(url):
    """主函数，整合上述功能"""
    html_content = fetch_webpage_content(url)
    assert html_content

    main_page = extract_main_content(html_content)
    links = find_links(main_page)

    for (text, link) in links:
        print(text, link)

    save_page(links[0][1])


if __name__ == "__main__":
    url = "https://www.ppzuowen.com/book/shaoergushi/zhentanxiaogushi/"  # 替换为您要爬取的网页URL
    main(url)
