import json
import time
import random
from DrissionPage import ChromiumPage, ChromiumOptions

# --- 配置区域 ---
category_list = [
    {"name": "3d-animation", "max_page": 18},
    {"name": "a-b-testing", "max_page": 6},
    {"name": "accounting", "max_page": 10},
    {"name": "activity-tracking", "max_page": 32},
    {"name": "Ad-blockers", "max_page": 6},
    {"name": "advertising-tools", "max_page": 31},
    {"name": "affiliate-marketing", "max_page": 9},
    {"name": "ai-agent-automation", "max_page": 6},
    {"name": "ai-characters", "max_page": 8},
    {"name": "ai-chatbots", "max_page": 98},
    {"name": "ai-chief-of-staff", "max_page": 1},
    {"name": "ai-code-editors", "max_page": 3},
    {"name": "ai-code-testing", "max_page": 3},
    {"name": "ai-coding-agents", "max_page": 30},
    {"name": "ai-content-detection", "max_page": 9},
    {"name": "ai-data-scientist", "max_page": 2},
    {"name": "ai-databases", "max_page": 3},
    {"name": "ai-designer", "max_page": 2},
    {"name": "ai-dictation-apps", "max_page": 2},
    {"name": "ai-engineer", "max_page": 2},
    {"name": "ai-generative-media", "max_page": 59},
    {"name": "ai-headshot-generators", "max_page": 3},
    {"name": "ai-infrastructure", "max_page": 33},
    {"name": "ai-meeting-notetakers", "max_page": 8},
    {"name": "ai-metrics-and-evaluation", "max_page": 10},
    {"name": "AI-notetakers", "max_page": 8},
    {"name": "AI-Presentation-Software", "max_page": 1},
    {"name": "ai-sales-tools", "max_page": 5},
    {"name": "ai-sdr", "max_page": 1},
    {"name": "ai-voice-agent-infrastructure", "max_page": 2},
    {"name": "ai-voice-agents", "max_page": 14},
    {"name": "analytics-databases", "max_page": 1},
    {"name": "App-switcher", "max_page": 11},
    {"name": "apps-for-kids", "max_page": 22},
    {"name": "authentication-identity", "max_page": 11},
    {"name": "automation", "max_page": 98},
    {"name": "avatar-generators", "max_page": 14},
    {"name": "background-removal", "max_page": 7},
    {"name": "blogging-platforms", "max_page": 14},
    {"name": "books", "max_page": 13},
    {"name": "browser-automation", "max_page": 1},
    {"name": "budgeting-and-expense-tracking", "max_page": 21},
    {"name": "business-intelligence", "max_page": 28},
    {"name": "calendars", "max_page": 22},
    {"name": "camera-apps", "max_page": 19},
    {"name": "camping-apps", "max_page": 2},
    {"name": "chrome-extensions", "max_page": 46},
    {"name": "cloud-computing-platforms", "max_page": 21},
    {"name": "cms", "max_page": 11},
    {"name": "code-editors", "max_page": 17},
    {"name": "code-review-tools", "max_page": 8},
    {"name": "command-line-tools", "max_page": 12},
    {"name": "community-management", "max_page": 31},
    {"name": "compliance-software", "max_page": 7},
    {"name": "credit-scores", "max_page": 3},
    {"name": "crm", "max_page": 25},
    {"name": "crowdfunding", "max_page": 5},
    {"name": "crypto-exchanges", "max_page": 6},
    {"name": "crypto-tools", "max_page": 23},
    {"name": "crypto-wallets", "max_page": 9},
    {"name": "customer-loyalty", "max_page": 10},
    {"name": "customer-support", "max_page": 37},
    {"name": "daos", "max_page": 3},
    {"name": "data-visualization", "max_page": 25},
    {"name": "databases-and-backend", "max_page": 19},
    {"name": "dating-apps", "max_page": 8},
    {"name": "defi", "max_page": 7},
    {"name": "design-inspiration", "max_page": 24},
    {"name": "design-mockups", "max_page": 18},
    {"name": "design-resources", "max_page": 91},
    {"name": "digital-whiteboards", "max_page": 7},
    {"name": "e-signature", "max_page": 6},
    {"name": "ecommerce-platforms", "max_page": 31},
    {"name": "email-clients", "max_page": 17},
    {"name": "email-marketing", "max_page": 32},
    {"name": "events", "max_page": 11},
    {"name": "family-care", "max_page": 9},
    {"name": "figma-plugins", "max_page": 14},
    {"name": "figma-templates", "max_page": 6},
    {"name": "file-storage", "max_page": 23},
    {"name": "financial-planning", "max_page": 21},
    {"name": "fitness", "max_page": 10},
    {"name": "flight-booking", "max_page": 5},
    {"name": "foundation-models", "max_page": 2},
    {"name": "fundraising-resources", "max_page": 23},
    {"name": "furniture", "max_page": 4},
    {"name": "games", "max_page": 24},
    {"name": "geo-tools", "max_page": 1},
    {"name": "git-clients", "max_page": 8},
    {"name": "graphic-design-tools", "max_page": 45},
    {"name": "headless-cms", "max_page": 5},
    {"name": "health-insurance", "max_page": 3},
    {"name": "hiking-apps", "max_page": 2},
    {"name": "hiring-software", "max_page": 28},
    {"name": "hotel-booking", "max_page": 4},
    {"name": "icon-sets", "max_page": 18},
    {"name": "influencer-marketing", "max_page": 10},
    {"name": "interface-design-tools", "max_page": 35},
    {"name": "investing", "max_page": 25},
    {"name": "invoicing-tools", "max_page": 11},
    {"name": "issue-tracking-software", "max_page": 10},
    {"name": "job-boards", "max_page": 20},
    {"name": "keyword-research", "max_page": 12},
    {"name": "knowledge-base", "max_page": 43},
    {"name": "landing-page-builders", "max_page": 16},
    {"name": "language-learning", "max_page": 15},
    {"name": "lead-generation", "max_page": 51},
    {"name": "legal-services", "max_page": 11},
    {"name": "link-in-bio", "max_page": 12},
    {"name": "live-streaming", "max_page": 8},
    {"name": "llm-developer-tools", "max_page": 2},
    {"name": "llm-fine-tuning", "max_page": 1},
    {"name": "maps-and-gps", "max_page": 13},
    {"name": "marketing-automation", "max_page": 63},
    {"name": "marketplace", "max_page": 28},
    {"name": "medical", "max_page": 10},
    {"name": "meditation", "max_page": 16},
    {"name": "meetings", "max_page": 19},
    {"name": "membership", "max_page": 5},
    {"name": "mental-health", "max_page": 23},
    {"name": "messaging-apps", "max_page": 33},
    {"name": "microblogging", "max_page": 6},
    {"name": "mobile-editing", "max_page": 36},
    {"name": "money-transfer", "max_page": 9},
    {"name": "music-generation", "max_page": 3},
    {"name": "neobanks", "max_page": 5},
    {"name": "news", "max_page": 23},
    {"name": "newsletter-platforms", "max_page": 14},
    {"name": "nft-creation", "max_page": 5},
    {"name": "nft-marketplaces", "max_page": 5},
    {"name": "no-code-ai-agent-builder", "max_page": 3},
    {"name": "no-code-app-builder", "max_page": 2},
    {"name": "no-code-website-builder", "max_page": 2},
    {"name": "notes-documents", "max_page": 67},
    {"name": "notion-templates", "max_page": 19},
    {"name": "observability-tools", "max_page": 4},
    {"name": "online-banking", "max_page": 4},
    {"name": "online-learning", "max_page": 61},
    {"name": "outdoors", "max_page": 9},
    {"name": "password-managers", "max_page": 5},
    {"name": "payment-processors", "max_page": 13},
    {"name": "payroll", "max_page": 4},
    {"name": "pdf-editor", "max_page": 7},
    {"name": "photo-editing", "max_page": 28},
    {"name": "photo-sharing", "max_page": 14},
    {"name": "podcasting", "max_page": 16},
    {"name": "predictive-ai", "max_page": 12},
    {"name": "pregnancy", "max_page": 2},
    {"name": "presentation-software", "max_page": 14},
    {"name": "product-demo", "max_page": 4},
    {"name": "professional-networking", "max_page": 35},
    {"name": "project-management", "max_page": 64},
    {"name": "prompt-engineering-tools", "max_page": 28},
    {"name": "real-estate", "max_page": 7},
    {"name": "real-time-collaboration-infra", "max_page": 1},
    {"name": "realtime-voice-ai", "max_page": 2},
    {"name": "remote-workforce", "max_page": 28},
    {"name": "resumes", "max_page": 13},
    {"name": "retirement-planning", "max_page": 2},
    {"name": "safety-and-privacy", "max_page": 24},
    {"name": "sales-enablement", "max_page": 4},
    {"name": "sales-training", "max_page": 5},
    {"name": "savings-apps", "max_page": 8},
    {"name": "scheduling", "max_page": 28},
    {"name": "screenshots-and-screen-recording", "max_page": 19},
    {"name": "search", "max_page": 31},
    {"name": "security-software", "max_page": 11},
    {"name": "senior-care", "max_page": 1},
    {"name": "seo-tools", "max_page": 21},
    {"name": "shopify-apps", "max_page": 12},
    {"name": "shopping", "max_page": 22},
    {"name": "short-term-rentals", "max_page": 5},
    {"name": "slack-apps", "max_page": 19},
    {"name": "sleep", "max_page": 12},
    {"name": "social-audio", "max_page": 8},
    {"name": "social-bookmarking", "max_page": 15},
    {"name": "social-media-management", "max_page": 39},
    {"name": "social-media-scheduling", "max_page": 7},
    {"name": "social-networking", "max_page": 75},
    {"name": "space-design", "max_page": 5},
    {"name": "spreadsheets", "max_page": 9},
    {"name": "standup-bots", "max_page": 3},
    {"name": "startup-communities", "max_page": 41},
    {"name": "startup-financial-planning", "max_page": 9},
    {"name": "startup-incorporation", "max_page": 1},
    {"name": "static-site-generators", "max_page": 6},
    {"name": "stock-photo-sites", "max_page": 6},
    {"name": "stock-trading", "max_page": 6},
    {"name": "survey-and-form-builders", "max_page": 16},
    {"name": "tax-preparation", "max_page": 6},
    {"name": "team-collaboration", "max_page": 83},
    {"name": "terminals", "max_page": 2},
    {"name": "testing-and-qa", "max_page": 18},
    {"name": "text-to-speech-software", "max_page": 8},
    {"name": "therapy-apps", "max_page": 13},
    {"name": "time-tracking", "max_page": 20},
    {"name": "toys", "max_page": 4},
    {"name": "transcription", "max_page": 2},
    {"name": "translation", "max_page": 2},
    {"name": "travel-apps", "max_page": 24},
    {"name": "travel-insurance", "max_page": 1},
    {"name": "travel-planning", "max_page": 28},
    {"name": "treasury-management-platforms", "max_page": 1},
    {"name": "twitter-apps", "max_page": 13},
    {"name": "ui-frameworks", "max_page": 28},
    {"name": "unified-api", "max_page": 21},
    {"name": "user-research", "max_page": 18},
    {"name": "vibe-coding", "max_page": 4},
    {"name": "video-and-voice-calling", "max_page": 17},
    {"name": "video-conferencing", "max_page": 10},
    {"name": "video-editing", "max_page": 34},
    {"name": "video-hosting", "max_page": 15},
    {"name": "virtual-events", "max_page": 7},
    {"name": "virtual-office", "max_page": 11},
    {"name": "vpn-client", "max_page": 4},
    {"name": "wallpapers", "max_page": 7},
    {"name": "wearables", "max_page": 9},
    {"name": "weather-apps", "max_page": 7},
    {"name": "web-browsers", "max_page": 15},
    {"name": "web-hosting", "max_page": 8},
    {"name": "webcams", "max_page": 2},
    {"name": "website-analytics", "max_page": 17},
    {"name": "website-builders", "max_page": 38},
    {"name": "wireframing", "max_page": 6},
    {"name": "wordpress-plugins", "max_page": 8},
    {"name": "wordpress-themes", "max_page": 4},
    {"name": "workout-platforms", "max_page": 12},
    {"name": "writing-assistants", "max_page": 42},
]

SHA256_HASH = "286726a8f1e788ece1f7214488cecd46e64b244ff190934bfa043ee14e5c106d"
BASE_API_URL = "https://www.producthunt.com/frontend/graphql"


def get_api_url(slug, page):
    variables = {"featuredOnly": True, 
                 "slug": slug,
                 "order": "recent_launches", 
                 "page": page, 
                 "pageSize": 15, 
                 "tags": None}
    extensions = {"persistedQuery": {"version": 1, "sha256Hash": SHA256_HASH}}
    import urllib.parse
    params = {"operationName": "CategoryPageListQuery", "variables": json.dumps(
        variables), "extensions": json.dumps(extensions)}
    return f"{BASE_API_URL}?{urllib.parse.urlencode(params)}"


def main():
    co = ChromiumOptions()
    # 保持浏览器不立即关闭，方便观察
    co.set_argument('--no-sandbox')

    page_obj = ChromiumPage(co)

    try:
        for category in category_list:
            slug = category["name"]
            max_page = category["max_page"]

            for page_num in range(1, max_page + 1):
                url = get_api_url(slug, page_num)
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

                    page_obj.wait(3)  # 每3秒检查一次
                    retry_count += 1

                # 尝试获取 JSON
                try:
                    # 使用 wait.ele_displayed 确保 pre 标签出现了再读取
                    res_data = page_obj.json
                    if res_data and 'data' in res_data:
                        print(f"成功获取第 {page_num} 页！")
                        # 保存数据...
                        with open("./apps/"+f"{slug}_page_{page_num}.json", "w") as f:
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
