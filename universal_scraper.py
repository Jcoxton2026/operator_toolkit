
import re, sys, requests, json, csv, os
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from datetime import datetime

REGEX_MAP = {
    "api_keys": [
        r"AKIA[0-9A-Z]{16}",
        r"sk-[A-Za-z0-9]{48}",
        r"AIza[0-9A-Za-z-_]{35}",
        r"sk_live_[0-9a-zA-Z]{24,}",
        r"(?i)(api|access|secret)[_-]?(key|token)['"=:\s]{0,5}[0-9a-zA-Z\-_.]{10,}"
    ],
    "emails": [r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"],
    "ips": [r"\b(?:\d{1,3}\.){3}\d{1,3}\b"],
    "cards": [r"4[0-9]{12}(?:[0-9]{3})?"],
    "hashes": [r"\b[a-f0-9]{32}\b", r"\b[a-f0-9]{40}\b"]
}

visited = set()
results = []

def get_regex(type_string):
    t = type_string.lower()
    if "api" in t: return REGEX_MAP["api_keys"]
    if "email" in t: return REGEX_MAP["emails"]
    if "ip" in t: return REGEX_MAP["ips"]
    if "card" in t or "visa" in t or "credit" in t: return REGEX_MAP["cards"]
    if "hash" in t: return REGEX_MAP["hashes"]
    return []

def clean_url(url): return url.strip().split("?")[0].split("#")[0]

def scan_text(content, patterns, source):
    matches = []
    for pattern in patterns:
        found = re.findall(pattern, content)
        for match in found:
            matches.append({"match": match, "source": source})
    if not matches:
        # fallback: scan for lines with "api", "key", "auth"
        if any(w in content.lower() for w in ["apikey", "auth", "secret"]):
            for line in content.splitlines():
                if any(w in line.lower() for w in ["apikey", "auth", "secret"]):
                    matches.append({"match": line.strip(), "source": source})
    return matches

def scrape_site(start_url, target_type, depth=2):
    if start_url in visited or depth == 0:
        return
    visited.add(start_url)
    try:
        print(f"[+] Scanning: {start_url}")
        r = requests.get(start_url, timeout=5)
        content = r.text
        patterns = get_regex(target_type)
        found = scan_text(content, patterns, start_url)
        results.extend(found)
        soup = BeautifulSoup(content, "html.parser")
        for tag in soup.find_all("a", href=True):
            href = tag["href"]
            full_url = urljoin(start_url, href)
            if urlparse(full_url).netloc == urlparse(start_url).netloc:
                scrape_site(full_url, target_type, depth - 1)
    except:
        pass

def save_results():
    with open("universal_scrape_results.json", "w") as f:
        json.dump(results, f, indent=2)
    with open("universal_scrape_results.csv", "w", newline="") as f:
        if results:
            writer = csv.DictWriter(f, fieldnames=["match", "source"])
            writer.writeheader()
            for row in results:
                writer.writerow(row)
    with open("scrape_log.txt", "a") as log:
        log.write(f"[{datetime.now().isoformat()}] Scanned {len(results)} results\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python universal_scraper.py \"scrape [what] from [site]\"")
        sys.exit(1)
    instruction = sys.argv[1].lower()
    if "from" not in instruction:
        print("Example: scrape visa cards from pastebin.com")
        sys.exit(1)
    what, site = instruction.split("from")
    what = what.replace("scrape", "").strip()
    site = site.strip()
    if not site.startswith("http"): site = "https://" + site
    print(f"[~] Scraping {what} from {site}")
    scrape_site(site, what)
    save_results()
    print("[✓] Done. Results saved to JSON, CSV and log.")
