import re
def scan_for_patterns(file):
    print(f"🔍 Scanning {file} for secrets")
    patterns = {
        "API Key": r"(?i)(key|token|api)[\\s:=\\\"']{0,3}[A-Za-z0-9_\\-]{16,}",
        "Email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+",
        "CC": r"\\b(?:\\d[ -]*?){13,16}\\b"
    }
    try:
        with open(file, "r") as f:
            content = f.read()
            for label, regex in patterns.items():
                found = re.findall(regex, content)
                if found:
                    print(f"[+] {label} → {found}")
    except FileNotFoundError:
        print("❌ File not found.")
