# coding=utf-8

# print("hello, world")
# 1、下载单个页面，返回字符串。
# 2、找到标题
# 3、找到正文（注意：正文中有粗体字）
# 4、写入 markdown 文件。

import os
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

def save_page(url, file_name):
    html_content = fetch_webpage_content(url)
    assert html_content

    page = extract_main_content(html_content)

    title = page.find("h2", class_="articleH2").text
    # print(title.text)

    content = page.find("div", class_="articleContent")
    paragraphs = content.find_all("p")
    ps = [p.text for p in paragraphs]
    # for p in paragraphs:
    #     print(p.text)

    # print(title.text)
    with open(file_name, "w", encoding="utf-8") as f:
        f.write("%s\n" % title)
        f.write("%s\n\n" % ('=' * (len(title)*2)))
        for p in ps:
            f.write("%s\n\n" % p.strip())


def main(url):
    """主函数，整合上述功能"""
    html_content = fetch_webpage_content(url)
    assert html_content

    main_page = extract_main_content(html_content)
    links = find_links(main_page)

    for (text, link) in links:
        print(text, link)

    base_dir = os.path.join("..", "docs", "source")
    file_names = []
    for i, (text, link) in enumerate(links, 1):
        file_name = "story_{:03}".format(i)
        file_names.append(file_name)
        save_page(link, os.path.join(base_dir, file_name + ".rst"))

    with open(os.path.join(base_dir, "index.rst"), "a", encoding="utf-8") as f:
        for file_name in file_names:
            f.write("   %s\n" % file_name)


if __name__ == "__main__":
    url = "https://www.ppzuowen.com/book/shaoergushi/zhentanxiaogushi/"  # 替换为您要爬取的网页URL
    main(url)
