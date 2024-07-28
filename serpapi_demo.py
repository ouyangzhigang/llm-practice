from serpapi import Client

api_key = ""

# 定义搜索参数
search_params = {
    "q": "Coffee",
    "location": "New York, New York",
    "hl": "en",
    "gl": "us",
    "google_domain": "google.com",
    "api_key": api_key
}

# 创建SerpAPI客户端
client = Client()

# 发送搜索请求并获取结果
results = client.search(search_params)

# 输出搜索结果
print(results)
