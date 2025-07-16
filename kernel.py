from modules import dorker, crawler, patterns

print("🧠 Operator Toolkit v4 — Say what you want to scan:")
user_input = input(">> ").lower()

if "dork" in user_input:
    dorker.run_dork_scan(user_input)
elif "crawl" in user_input or "scrape" in user_input:
    crawler.crawl_target(user_input)
elif "api" in user_input or "key" in user_input:
    patterns.scan_for_patterns("data/input.txt")
else:
    print("❌ No matching module found.")
