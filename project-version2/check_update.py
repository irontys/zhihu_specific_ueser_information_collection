import requests
import time
while True:
    url = 'http://127.0.0.1:5002?update=1'
    response = requests.get(url)
    if response.status_code == 200:
        print('请求成功')
    time.sleep(5 * 60)  # 5分钟