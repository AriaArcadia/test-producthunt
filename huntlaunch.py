import json
import time
import random
import os
from DrissionPage import ChromiumPage, ChromiumOptions

if not os.path.exists("./launches/"):
    os.makedirs("./launches/") 
# --- 配置区域 ---
category_list = [
    {"name": "notion",},
]

SHA256_HASH = "b6d9a2df9579eeada897cd06824673aecd21ebfb5fa4bb99ab4e651574e4d0ae"
BASE_API_URL = "https://www.producthunt.com/frontend/graphql"

def get_api_url(slug, cursor):
    variables = {
        "slug": slug, 
        "cursor": cursor, 
        "order":"DATE"}
    extensions = {"persistedQuery": {"version": 1, "sha256Hash": SHA256_HASH}}
    import urllib.parse
    params = {"operationName": "ProductPageLaunches", "variables": json.dumps(variables), "extensions": json.dumps(extensions)}
    return f"{BASE_API_URL}?{urllib.parse.urlencode(params)}"


def main():
    co = ChromiumOptions()
    # 保持浏览器不立即关闭，方便观察
    co.set_argument('--no-sandbox')
    
    page_obj = ChromiumPage(co)
    
    try:
        for category in category_list:
            slug = category["name"]
            cursor="null"
            page_num=1
            has_nextpage=True
            while True:
                if has_nextpage==False:
                    break
                url = get_api_url(slug, cursor)
                print(f"正在请求: {slug} 第 {page_num} 页...")
                
                page_obj.get(url)
                
                # --- 核心逻辑：循环检查是否通过了 Cloudflare ---
                retry_count = 0
                while retry_count < 10:
                    # 检查页面是否包含 JSON 的特征字符
                    if '"data":' in page_obj.html:
                        break 
                    
                    # 如果没看到数据，说明可能还在验证页
                    print("检测到 Cloudflare 验证，请在浏览器中手动点击（如有必要）...")
                    
                    # 尝试寻找 Cloudflare 的复选框并点击 (有时 DrissionPage 能直接点)
                    if page_obj.ele('@id:cf-turnstile-wrapper', timeout=10):
                        print("尝试点击验证复选框...")
                    
                    page_obj.wait(3) # 每3秒检查一次
                    retry_count += 1
                
                # 尝试获取 JSON
                try:
                    # 使用 wait.ele_displayed 确保 pre 标签出现了再读取
                    res_data = page_obj.json
                    if res_data and 'data' in res_data:
                        print(f"成功获取第 {page_num} 页！")
                        # 保存数据...
                        with open("./launches/"+f"{slug}_page_{page_num}.json", "w") as f:
                            json.dump(res_data, f)
                        cursor=res_data["data"]["product"]["posts"]["pageInfo"]["endCursor"]
                        has_nextpage=res_data["data"]["product"]["posts"]["pageInfo"]["hasNextPage"]
                    else:
                        print(f"第 {page_num} 页返回内容异常。")
                except Exception as e:
                    print(f"解析 JSON 失败: {e}")

                time.sleep(random.uniform(2, 5))
                page_num+=1

    except Exception as e:
        print(f"运行出错: {e}")
    finally:
        # 为了调试方便，报错后不立即关闭，你可以注释掉下面这一行
        # input("按回车键关闭浏览器并结束程序...") 
        page_obj.quit()

if __name__ == "__main__":
    main()