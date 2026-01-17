import time
import random
import os
from DrissionPage import ChromiumPage, ChromiumOptions

# --- 配置区域 ---
# 想要抓取的分类 slug 列表
slugs = [
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
]
BASE_URL = "https://www.producthunt.com/categories/"
SAVE_DIR = "ph_pages"

# 创建保存文件夹
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def main():
    # 配置浏览器
    co = ChromiumOptions()
    page = ChromiumPage(co)
    
    try:
        for slug in slugs:
            url = f"{BASE_URL}{slug}"
            print(f"正在访问: {url}")
            
            page.get(url)
            
            # --- 等待 Cloudflare 验证 ---
            # 逻辑：只要页面里还包含验证字样，就持续等待
            # 如果你看到浏览器卡在验证码，请手动点一下
            while True:
                if "Verify you are human" in page.html or "Checking your browser" in page.html:
                    print("等待 Cloudflare 验证中...")
                    page.wait(2)
                else:
                    # 检查是否出现了 Product Hunt 的特征元素（例如页面标题或主体内容）
                    if page.ele('t:main', timeout=2): 
                        break
                    page.wait(1)
            
            # --- 保存网页 ---
            file_path = os.path.join(SAVE_DIR, f"{slug}.html")
            # 直接保存当前页面的 HTML 源码
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(page.html)
            
            print(f"成功保存: {file_path}")
            
            # 随机休眠，防止被封 IP
            time.sleep(random.uniform(3, 6))

    except Exception as e:
        print(f"运行出错: {e}")
    finally:
        print("所有任务处理完毕。")
        page.quit()

if __name__ == "__main__":
    main()