import socket
import ipaddress
from urllib.parse import urlparse
from datetime import datetime

G = "\033[92m"
R = "\033[91m"
X = "\033[0m"
HISTORY = "azzou_history.txt"

def get_data():
    raw = input("\nEnter domain or URL: ").strip()
    if not raw:
        print("Empty input!")
        return None
    if "://" not in raw:
        raw = "https://" + raw
    try:
        p = urlparse(raw)
        if not p.hostname:
            print("Invalid URL!")
            return None
        return raw, p
    except ValueError:
        print("Invalid URL!")
        return None

def is_short_url(host):
    shorteners = {
        "bit.ly", "tinyurl.com", "t.co", "is.gd",
        "cutt.ly", "ow.ly", "buff.ly", "shorturl.at",
        "rebrand.ly", "rb.gy", "tiny.cc"
    }
    host = host.lower().rstrip(".")
    return any(host == d or host.endswith("." + d)
               for d in shorteners)

def scan_url():
    data = get_data()
    if not data:
        return
    raw, p = data
    host = p.hostname
    warnings = []

    if is_short_url(host):
        warnings.append("Shortened URL detected")

    if p.scheme != "https":
        warnings.append("No HTTPS")
    if p.username or p.password:
        warnings.append("Credentials inside URL")
    try:
        ipaddress.ip_address(host)
        warnings.append("Host is an IP address")
    except ValueError:
        pass
    if "xn--" in host.lower():
        warnings.append("Encoded domain name")
    if len(raw) > 120:
        warnings.append("Unusually long URL")

    score = 0
    weights = {
        "No HTTPS": 15,
        "Host is an IP address": 20,
        "Credentials inside URL": 35,
        "Encoded domain name": 15,
        "Unusually long URL": 10,
        "Shortened URL detected": 20
    }

    for warning in warnings:
        score += weights.get(warning, 0)

    score = min(score, 100)

    if score >= 40:
        level = "HIGH"
    elif score >= 20:
        level = "MEDIUM"
    else:
        level = "LOW"

    print("\nRISK SCORE:", str(score) + "/100")
    print("Risk Level:", level)

    print("\n=== AZZOU SCAN REPORT ===")
    print("Domain:", host)
    if warnings:
        for item in warnings:
            print(R + "WARNING:", item + X)
        result = "Warnings found"
    else:
        print(G + "No basic warning indicators found." + X)
        result = "No basic warnings found"

    print("This scan cannot guarantee website safety.")
    with open(HISTORY, "a") as f:
        f.write(f"{datetime.now()} | {raw} | {result}\n")
    print("Report saved!")

def analyze_domain():
    data = get_data()
    if not data:
        return
    raw, p = data
    host = p.hostname

    print("\n=== DOMAIN ANALYZER ===")
    print("Domain:", host)
    print("Protocol:", p.scheme)
    print("Port:", p.port or "Default")
    print("Path:", p.path or "/")

    try:
        ipaddress.ip_address(host)
        print("Host type: IP address")
    except ValueError:
        print("Host type: Domain name")
        try:
            addresses = sorted(set(
                item[4][0] for item in socket.getaddrinfo(host, None)
            ))
            print("IP addresses:")
            for address in addresses:
                print("-", address)
        except OSError:
            print("Could not resolve domain.")

    print("DNS data does not prove a site is safe.")

def show_history():
    try:
        with open(HISTORY) as f:
            print("\n" + f.read())
    except FileNotFoundError:
        print("No scans yet.")

def menu():
    while True:
        print(G + "\n=== AZZOU GOUiZI ===" + X)
        print("[1] SCAN URL")
        print("[2] SCAN HISTORY")
        print("[3] DOMAIN ANALYZER")
        print("[4] ABOUT")
        print("[0] EXIT")

        choice = input("\nAZZOU > ").strip()

        if choice == "1":
            scan_url()
        elif choice == "2":
            show_history()
        elif choice == "3":
            analyze_domain()
        elif choice == "4":
            print("AZZOU GOUiZI - Local URL Scanner")
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")

        input("\nPress Enter to continue...")

if __name__ == "__main__":
    menu()
