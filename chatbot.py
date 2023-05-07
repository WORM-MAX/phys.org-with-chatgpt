import openai
import json

openai.api_base = "http://23.94.255.47:6666/v1"
openai.api_key  = "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"

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.7, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


#读取scrapy获得的文章数据
with open("data.json","r",encoding = "utf-8") as data:
    data_contents = json.load(data)

#for data_item in data_contents:
data_item = data_contents[0]
title = data_item["title"]
abstract = data_item["brief"]
body = data_item["body"]
prompt = f"""
The following is a title, abstract and text of an news article about physics \
delimited by triple quotes.  \
Tell me the structure and summarize key point.  \
Use the bullet point to separate different parts. \
For the body part, you should offer more detailed information with three sentences.  \
Title: '''{title}''' \
Abstract:'''{abstract}
Text: '''{body}'''
"""
response = get_completion(prompt)
print(response)
