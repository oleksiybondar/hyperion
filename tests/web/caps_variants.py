# firefox_caps = {"automation": "selenium", "browser": "firefox"}
chrome_caps = {"automation": "selenium", "browser": "chrome", "headless": True}
edge_caps = {"automation": "selenium", "browser": "edge"}
webkit_playwright_caps = {"automation": "playwright", "browser": "webkit"}
chrome_playwright_caps = {"automation": "playwright", "browser": "chrome"}
firefox_playwright_caps = {"automation": "playwright", "browser": "firefox"}
caps_variants = [
    # firefox_caps,
    chrome_caps,
    edge_caps,
    webkit_playwright_caps,
    chrome_playwright_caps,
    firefox_playwright_caps,
]
