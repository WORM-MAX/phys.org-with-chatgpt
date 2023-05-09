import requests
import random
from lxml import etree
import os
import codecs
import json

#Use multiple 'user-agent' to avoid request limit
USER_AGENT_LIST = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
    "Opera/8.0 (Windows NT 5.1; U; en)",
    "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",

]
USER_AGENT = random.choice(USER_AGENT_LIST)

url = 'https://phys.org/physics-news/'

head = {
	"User-Agent": USER_AGENT
}

resp = requests.get(url, headers=head,stream=True)

#get url of articles on the first page
html = etree.HTML(resp.text)
links = html.xpath('/html/body/main/div/div[1]/div/div[1]/div[4]/div/div/article/div[1]/div/h3/a/@href')
resp.close()

#store articles in json
json_file = codecs.open('data.json', 'w+', encoding='UTF-8')
json_file.write('[\n')

#Read information of each article separately
for link in links:
    resp = requests.get(link, headers=head,stream=True)
    html = etree.HTML(resp.text)
    title = html.xpath('/html/body/main/div[1]/div[3]/div[2]/section/div/div[4]/article/h1/text()')
    brief = html.xpath('/html/body/main/div[1]/div[3]/div[2]/section/div/div[4]/article/div[2]/p[1]/text()[1]')
    body = html.xpath('/html/body/main/div[1]/div[3]/div[2]/section/div/div[4]/article/div[2]/p/text()')
    pdf = html.xpath('/html/body/main/div[1]/div[3]/div[2]/section/div/div[2]/ul/li[2]/a/@href')
    dict = {'title' : title, 'brief' : brief, 'body'  : body, 'pdf'   : pdf}
    item_json = json.dumps(dict, ensure_ascii=False)
    json_file.write('\t' + item_json + ',\n')
    resp.close()
    print(link)

#add end to json file
json_file.seek(-2, os.SEEK_END)
json_file.truncate()
json_file.write('\n]')
json_file.close()
