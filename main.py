from utils import *
import requests

url = 'https://phys.org/physics-news/'

head = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
	"Referer":"https://phys.org/news/2023-05-highly-device-polariton-based-coherent-microwave.html",
}

resp = requests.get(url, headers=head)

print(resp.text)
resp.close()
/html/body/main/div/div[1]/div/div[1]/div[4]/div/div/article/div[1]/div/h3/a/@href