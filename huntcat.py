import json
import time
import random
from DrissionPage import ChromiumPage, ChromiumOptions

# --- 配置区域 ---
category_list = [
    "ai-meeting-notetakers",
    "ai-presentation-software",
    "ad-blockers",
    "app-switcher",
    "cms",
    "calendars",
    "compliance-software",
    "customer-support",
    "e-signature",
    "email-clients",
    "file-storage",
    "hiring-software",
    "knowledge-base",
    "legal-services",
    "meetings",
    "notes-documents",
    "pdf-editor",
    "password-managers",
    "presentation-software",
    "product-demo",
    "project-management",
    "resumes",
    "scheduling",
    "screenshots-and-screen-recording",
    "search",
    "security-software",
    "spreadsheets",
    "team-collaboration",
    "time-tracking",
    "video-conferencing",
    "virtual-office",
    "web-browsers",
    "writing-assistants",
    "a-b-testing",
    "ai-code-editors",
    "ai-code-testing",
    "ai-coding-agents",
    "ai-databases",
    "authentication-identity",
    "automation",
    "browser-automation",
    "cloud-computing-platforms",
    "code-review-tools",
    "code-editors",
    "command-line-tools",
    "databases-and-backend",
    "git-clients",
    "headless-cms",
    "issue-tracking-software",
    "membership",
    "observability-tools",
    "predictive-ai",
    "real-time-collaboration-infra",
    "standup-bots",
    "static-site-generators",
    "terminals",
    "testing-and-qa",
    "unified-api",
    "vpn-client",
    "vibe-coding",
    "video-hosting",
    "web-hosting",
    "website-analytics",
    "website-builders",
    "3d-animation",
    "ai-characters",
    "ai-generative-media",
    "ai-headshot-generators",
    "avatar-generators",
    "background-removal",
    "camera-apps",
    "design-inspiration",
    "design-mockups",
    "design-resources",
    "digital-whiteboards",
    "graphic-design-tools",
    "icon-sets",
    "interface-design-tools",
    "mobile-editing",
    "music-generation",
    "photo-editing",
    "podcasting",
    "social-audio",
    "space-design",
    "stock-photo-sites",
    "ui-frameworks",
    "user-research",
    "video-editing",
    "wallpapers",
    "wireframing",
    "accounting",
    "budgeting-and-expense-tracking",
    "credit-scores",
    "financial-planning",
    "fundraising-resources",
    "investing",
    "invoicing-tools",
    "money-transfer",
    "neobanks",
    "online-banking",
    "payroll",
    "remote-workforce",
    "retirement-planning",
    "savings-apps",
    "startup-financial-planning",
    "startup-incorporation",
    "stock-trading",
    "tax-preparation",
    "treasury-management-platforms",
    "ai-content-detection",
    "blogging-platforms",
    "community-management",
    "dating-apps",
    "link-in-bio",
    "live-streaming",
    "messaging-apps",
    "microblogging",
    "newsletter-platforms",
    "photo-sharing",
    "professional-networking",
    "safety-and-privacy",
    "social-networking",
    "social-bookmarking",
    "video-and-voice-calling",
    "ai-sales-tools",
    "advertising-tools",
    "affiliate-marketing",
    "crm",
    "customer-loyalty",
    "email-marketing",
    "geo-tools",
    "influencer-marketing",
    "keyword-research",
    "landing-page-builders",
    "lead-generation",
    "marketing-automation",
    "seo-tools",
    "sales-enablement",
    "sales-training",
    "social-media-management",
    "social-media-scheduling",
    "survey-and-form-builders",
    "activity-tracking",
    "camping-apps",
    "health-insurance",
    "hiking-apps",
    "medical",
    "meditation",
    "mental-health",
    "senior-care",
    "sleep",
    "therapy-apps",
    "workout-platforms",
    "flight-booking",
    "hotel-booking",
    "maps-and-gps",
    "outdoors",
    "short-term-rentals",
    "travel-insurance",
    "travel-planning",
    "travel-apps",
    "weather-apps",
    "crowdfunding",
    "events",
    "job-boards",
    "language-learning",
    "news",
    "online-learning",
    "real-estate",
    "startup-communities",
    "virtual-events",
    "chrome-extensions",
    "figma-plugins",
    "figma-templates",
    "notion-templates",
    "slack-apps",
    "twitter-apps",
    "wordpress-plugins",
    "wordpress-themes",
    "books",
    "fitness",
    "furniture",
    "games",
    "toys",
    "wearables",
    "webcams",
    "ai-agent-automation",
    "ai-chief-of-staff",
    "ai-data-scientist",
    "ai-designer",
    "ai-engineer",
    "ai-sdr",
    "ai-voice-agents",
    "ai-chatbots",
    "ai-infrastructure",
    "ai-metrics-and-evaluation",
    "foundation-models",
    "llm-developer-tools",
    "llm-fine-tuning",
    "prompt-engineering-tools",
    "crypto-exchanges",
    "crypto-tools",
    "crypto-wallets",
    "daos",
    "defi",
    "nft-creation",
    "nft-marketplaces",
    "ai-dictation-apps",
    "ai-voice-agent-infrastructure",
    "realtime-voice-ai",
    "text-to-speech-software",
    "transcription",
    "translation",
    "ecommerce-platforms",
    "marketplace",
    "payment-processors",
    "shopify-apps",
    "apps-for-kids",
    "family-care",
    "pregnancy",
    "no-code-ai-agent-builder",
    "no-code-app-builder",
    "no-code-website-builder",
    "analytics-databases",
    "business-intelligence",
    "data-visualization",
    "shopping"
    "ad-blockers"
]

SHA256_HASH = "af541f9180b594284c2ded4818df1357f2d773cf5edd9d1fd6684cf8f7353e51"
BASE_API_URL = "https://www.producthunt.com/frontend/graphql"

def get_api_url(slug):
    variables = {"slug":slug,"path":"/categories/ai-meeting-notetakers"}
    extensions = {"persistedQuery": {"version": 1, "sha256Hash": SHA256_HASH}}
    import urllib.parse
    params = {"operationName": "CategoryPageQuery", "variables": json.dumps(variables), "extensions": json.dumps(extensions)}
    return f"{BASE_API_URL}?{urllib.parse.urlencode(params)}"

def main():
    co = ChromiumOptions()
    # 保持浏览器不立即关闭，方便观察
    co.set_argument('--no-sandbox')
    
    page_obj = ChromiumPage(co)
    
    try:
        for category in category_list:
            slug = category
            
            for page_num in range(1,2):# 只有一页
                url = get_api_url(slug)
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
                        with open("./items/"+f"{slug}_page_{page_num}.json", "w") as f:
                            json.dump(res_data, f)
                    else:
                        print(f"第 {page_num} 页返回内容异常。")
                except Exception as e:
                    print(f"解析 JSON 失败: {e}")

                time.sleep(random.uniform(2, 5))

    except Exception as e:
        print(f"运行出错: {e}")
    finally:
        # 为了调试方便，报错后不立即关闭，你可以注释掉下面这一行
        # input("按回车键关闭浏览器并结束程序...") 
        page_obj.quit()

if __name__ == "__main__":
    main()