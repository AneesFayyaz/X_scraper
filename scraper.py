from playwright.sync_api import sync_playwright
from pathlib import Path
import random
import time
import json
import requests
from urllib.parse import unquote

STORAGE_FILE = "auth_state.json"
LOGIN_URL = "https://x.com/i/flow/login"
POST_URL = "https://x.com/SixersBBL/status/1981193917677916261"
TWEET_DETAIL_FULL_URL = (
    "https://x.com/i/api/graphql/5IxZ_DFOXCqILZ1LK_3tdA/TweetDetail"
    "?variables=%7B%22focalTweetId%22%3A%221981193917677916261%22%2C%22with_rux_injections%22%3Afalse%2C%22rankingMode%22%3A%22Relevance%22%2C..."
    "&features=%7B%22rweb_video_screen_enabled%22%3Afalse%2C%22payments_enabled%22%3Afalse%2C..."
    "&fieldToggles=%7B%22withArticleRichContentState%22%3Atrue%2C..."
)

USER_FLOW_URL = "https://x.com/i/api/1.1/graphql/user_flow.json"


USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
]


VIEWPORTS = [
    {"width": 1920, "height": 1080},
    {"width": 1536, "height": 864},
    {"width": 1366, "height": 768},
]

def human_delay(min_ms=500, max_ms=2000):
    time.sleep(random.uniform(min_ms/1000, max_ms/1000))

def random_mouse_movement(page):
    try:
        width = page.viewport_size["width"]
        height = page.viewport_size["height"]
        for _ in range(random.randint(1, 3)):
            x = random.randint(100, width - 100)
            y = random.randint(100, height - 100)
            page.mouse.move(x, y, steps=random.randint(10, 30))
            time.sleep(random.uniform(0.1, 0.3))
    except Exception as e:
        print(f"Mouse movement error: {e}")

def add_comprehensive_stealth(context):

    context.add_init_script("""
    () => {
      // Webdriver property
      Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
      });

      // Chrome object
      window.chrome = {
        runtime: {},
        loadTimes: function() {},
        csi: function() {},
        app: {}
      };

      // Permissions
      const originalQuery = window.navigator.permissions.query;
      window.navigator.permissions.query = (parameters) => (
        parameters.name === 'notifications' ?
          Promise.resolve({ state: Notification.permission }) :
          originalQuery(parameters)
      );

      // Plugins
      Object.defineProperty(navigator, 'plugins', {
        get: () => [
          {
            0: {type: "application/x-google-chrome-pdf", suffixes: "pdf", description: "Portable Document Format"},
            description: "Portable Document Format",
            filename: "internal-pdf-viewer",
            length: 1,
            name: "Chrome PDF Plugin"
          },
          {
            0: {type: "application/pdf", suffixes: "pdf", description: ""},
            description: "",
            filename: "mhjfbmdgcfjbbpaeojofohoefgiehjai",
            length: 1,
            name: "Chrome PDF Viewer"
          }
        ],
      });

      // Languages
      Object.defineProperty(navigator, 'languages', {
        get: () => ['en-US', 'en']
      });

      // Hardware
      Object.defineProperty(navigator, 'hardwareConcurrency', {
        get: () => 8
      });

      Object.defineProperty(navigator, 'deviceMemory', {
        get: () => 8
      });

      // WebGL
      const getParameter = WebGLRenderingContext.prototype.getParameter;
      WebGLRenderingContext.prototype.getParameter = function(parameter) {
        if (parameter === 37445) {
          return 'Intel Inc.';
        }
        if (parameter === 37446) {
          return 'Intel Iris OpenGL Engine';
        }
        return getParameter.call(this, parameter);
      };

      // Canvas noise
      const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
      HTMLCanvasElement.prototype.toDataURL = function(type) {
        const context = this.getContext('2d');
        if (context) {
          const imageData = context.getImageData(0, 0, this.width, this.height);
          for (let i = 0; i < imageData.data.length; i += 4) {
            if (Math.random() < 0.001) {
              imageData.data[i] = imageData.data[i] ^ 1;
            }
          }
          context.putImageData(imageData, 0, 0);
        }
        return originalToDataURL.apply(this, arguments);
      };

      // Remove automation indicators
      delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
      delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
      delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
    }
    """)


def create_stealth_browser(p, storage_state=None):
    user_agent = random.choice(USER_AGENTS)
    viewport = random.choice(VIEWPORTS)
    launch_args = [
        "--disable-blink-features=AutomationControlled",
        "--disable-dev-shm-usage",
        "--disable-background-timer-throttling",
        "--disable-backgrounding-occluded-windows",
        "--disable-renderer-backgrounding",
        "--disable-features=IsolateOrigins,site-per-process",
        "--disable-site-isolation-trials",
        "--disable-web-security",
        "--disable-features=ImprovedCookieControls",
        "--no-first-run",
        "--no-service-autorun",
        "--password-store=basic",
        "--disable-infobars",
        "--window-size=1920,1080",
        f"--user-agent={user_agent}",
    ]
    browser = p.chromium.launch(channel="chrome", headless=False, args=launch_args, slow_mo=50)
    context_kwargs = dict(
        user_agent=user_agent,
        viewport=viewport,
        locale="en-US",
        timezone_id="America/New_York",
        geolocation={"longitude": -74.0060, "latitude": 40.7128},
        permissions=["geolocation"],
        color_scheme="light",
        device_scale_factor=1,
        has_touch=False,
        is_mobile=False,
        extra_http_headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0",
        }
    )
    if storage_state:
        context_kwargs["storage_state"] = storage_state

    context = browser.new_context(**context_kwargs)
    add_comprehensive_stealth(context)
    context.set_default_timeout(60000)
    context.set_default_navigation_timeout(60000)
    return browser, context


# Helpers for building requests.Session from Playwright storage

def load_storage_state(path=STORAGE_FILE):
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Storage state not found at {path}")
    return json.loads(p.read_text(encoding="utf-8"))

def build_session_from_storage(storage):
    s = requests.Session()
    cookies = storage.get("cookies", [])
    for c in cookies:
        cookie = requests.cookies.create_cookie(
            name=c.get("name"),
            value=c.get("value"),
            domain=c.get("domain"),
            path=c.get("path", "/"),
        )
        s.cookies.set_cookie(cookie)

    s.headers.update({
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": POST_URL,
        "Connection": "keep-alive",
    })


    ct0 = None
    for c in cookies:
        if c.get("name") in ("ct0", "csrf_token"):
            ct0 = c.get("value")
            break
    if ct0:
        s.headers["x-csrf-token"] = ct0

    s.headers.update({
        "x-twitter-auth-type": "OAuth2Session",
        "x-twitter-client-language": "en",
        "x-twitter-active-user": "yes",
    })
    return s


# JSON parsing helpers

def recursive_collect_full_texts(obj):
    results = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "full_text" and isinstance(v, str):
                results.append(v)
            else:
                results.extend(recursive_collect_full_texts(v))
    elif isinstance(obj, list):
        for item in obj:
            results.extend(recursive_collect_full_texts(item))
    return results

def recursive_collect_comment_objects(obj):
    found = []
    if isinstance(obj, dict):
        if "full_text" in obj and isinstance(obj.get("full_text"), str):
            comment = {
                "full_text": obj.get("full_text"),
                "id_str": obj.get("id_str"),
                "user_id_str": obj.get("user_id_str"),
                "in_reply_to_status_id_str": obj.get("in_reply_to_status_id_str"),

            }
            found.append(comment)
        for v in obj.values():
            found.extend(recursive_collect_comment_objects(v))
    elif isinstance(obj, list):
        for item in obj:
            found.extend(recursive_collect_comment_objects(item))
    return found


# Network functions

def get_tweet_detail_comments(session, url_with_query):
    if not url_with_query or "TweetDetail" not in url_with_query:
        raise ValueError("Please set TWEET_DETAIL_FULL_URL to the exact TweetDetail URL with query string.")
    url = unquote(url_with_query)
    r = session.get(url, timeout=30)
    r.raise_for_status()
    data = r.json()
    # Collect simple full_text list
    full_texts = recursive_collect_full_texts(data)
    # Collect structured comment objects
    comment_objs = recursive_collect_comment_objects(data)
    return full_texts, comment_objs, data

def call_user_flow_post(session, payload_dict):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://x.com",
        "Referer": "https://x.com/",

    }
    # Make a copy of session headers and update
    merged_headers = session.headers.copy()
    merged_headers.update(headers)

    r = session.post(USER_FLOW_URL, data=payload_dict, headers=merged_headers, timeout=30)
    r.raise_for_status()
    try:
        return r.json()
    except ValueError:
        return r.text

# Main flow

def main():
    storage_path = Path(STORAGE_FILE)
    storage_exists = storage_path.exists()
    storage_state = STORAGE_FILE if storage_exists else None

    with sync_playwright() as p:
        print(" Launching stealth browser...")
        browser, ctx = create_stealth_browser(p, storage_state=storage_state)
        try:
            page = ctx.new_page()
            page.set_extra_http_headers({
                "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
            })

            # --- If no previous session, perform manual login ---
            if not storage_exists:
                print(" No previous session found. Opening login page...")
                page.goto(LOGIN_URL, wait_until="networkidle", timeout=120000)
                human_delay(2000, 4000)
                random_mouse_movement(page)
                print("  After login, press ENTER here to continue.")
                input("Press ENTER after you've successfully logged in...")

                ctx.storage_state(path=STORAGE_FILE)
                print(f"[✓] Session saved to: {STORAGE_FILE}")

            else:
                print(f"Found existing storage file: {STORAGE_FILE}. Using it directly")
           
            print(f" Navigating to post: {POST_URL}")
            page.goto(POST_URL, wait_until="networkidle", timeout=120000)
            human_delay(1000, 2000)

        
            print("Building requests session from saved Playwright storage...")
            storage = load_storage_state(STORAGE_FILE)
            sess = build_session_from_storage(storage)

        
            if not TWEET_DETAIL_FULL_URL or "TweetDetail" not in TWEET_DETAIL_FULL_URL:
                print("ERROR: Please set TWEET_DETAIL_FULL_URL correctly.")
            else:
                print("Requesting TweetDetail endpoint and extracting comments...")
                try:
                    payload = {
                        "debug": "true",
                        "log": '[{"event":"tweet_detail_loaded","tweet_id":"1981193917677916261"}]'
                    }
                    resp = call_user_flow_post(sess, payload)

                    full_texts, comment_objs, raw_json = get_tweet_detail_comments(sess, TWEET_DETAIL_FULL_URL)
                    print(f"Extracted {len(full_texts)} full_texts and {len(comment_objs)} comments.")

                    Path("comments.json").write_text(
                        json.dumps({"full_texts": full_texts, "comment_objects": comment_objs}, indent=2, ensure_ascii=False)
                    )
                    print("Saved comments to comments.json")

                    for i, c in enumerate(comment_objs[:30], start=1):
                        print(f"{i:03d}: id={c.get('id_str')} user={c.get('user_id_str')}")
                        print(f"      {c.get('full_text')}\n")
                except Exception as e:
                    print(f"[!] Error fetching TweetDetail: {e}")

        except Exception as e:
            print(f"Error occurred in main flow: {e}")
        finally:
            print("Cleaning up Playwright resources...")
            try:
                ctx.close()
            except:
                pass
            try:
                browser.close()
            except:
                pass


if __name__ == "__main__":
    main()
