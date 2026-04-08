#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════╗
║         FUZZR - Authorized Web Path Fuzzer           ║
║         For authorized penetration testing only      ║
╚══════════════════════════════════════════════════════╝
"""

import sys
import os
import time
import argparse
import threading
import queue
import signal
import json
import re
from datetime import datetime
from urllib.parse import urlparse, urljoin
from pathlib import Path

# ─── DEPENDENCY CHECK ───────────────────────────────────────────────────────

def check_and_install_deps():
    missing = []
    try:
        import requests
    except ImportError:
        missing.append("requests")
    try:
        from colorama import Fore, Back, Style, init
    except ImportError:
        missing.append("colorama")
    
    if missing:
        print(f"[!] Missing dependencies: {', '.join(missing)}")
        print(f"[*] Installing: pip3 install {' '.join(missing)}")
        os.system(f"pip3 install {' '.join(missing)} -q")
        print("[+] Dependencies installed. Restarting...\n")

check_and_install_deps()

import requests
import urllib3
from colorama import Fore, Back, Style, init

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
init(autoreset=True)

requests.packages.urllib3.disable_warnings()

# ─── GLOBALS ────────────────────────────────────────────────────────────────

VERSION = "2.0.0"
BANNER = f"""
{Fore.RED}╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   {Fore.WHITE}███████╗██╗   ██╗███████╗███████╗██████╗ {Fore.RED}                  ║
║   {Fore.WHITE}██╔════╝██║   ██║╚══███╔╝╚══███╔╝██╔══██╗{Fore.RED}                  ║
║   {Fore.WHITE}█████╗  ██║   ██║  ███╔╝   ███╔╝ ██████╔╝{Fore.RED}                  ║
║   {Fore.WHITE}██╔══╝  ██║   ██║ ███╔╝   ███╔╝  ██╔══██╗{Fore.RED}                  ║
║   {Fore.WHITE}██║     ╚██████╔╝███████╗███████╗██║  ██║{Fore.RED}                   ║
║   {Fore.WHITE}╚═╝      ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝{Fore.RED}                  ║
║                                                              ║
║   {Fore.YELLOW}v{VERSION} — Authorized Web Path Fuzzer{Fore.RED}                    ║
║   {Fore.WHITE}For authorized penetration testing ONLY{Fore.RED}                     ║
╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""

# Default SecLists paths on Kali Linux
SECLIST_PATHS = [
    "/usr/share/seclists/Discovery/Web-Content/common.txt",
    "/usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt",
    "/usr/share/seclists/Discovery/Web-Content/directory-list-2.3-small.txt",
    "/usr/share/wordlists/dirb/common.txt",
    "/usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-small.txt",
]

FALLBACK_WORDLIST = [
    "admin", "login", "dashboard", "api", "api/v1", "api/v2", "backup",
    "config", "test", "dev", "staging", "upload", "uploads", "files",
    "images", "img", "static", "assets", "js", "css", "fonts", "media",
    "wp-admin", "wp-content", "wp-login.php", "phpmyadmin", "mysql",
    "database", "db", "sql", "server", "index", "home", "user", "users",
    "account", "accounts", "profile", "settings", "panel", "control",
    "manager", "management", "admin/login", "admin/dashboard", "secret",
    "private", "hidden", "old", "new", "tmp", "temp", "cache", "log", "logs",
    "robots.txt", ".htaccess", "sitemap.xml", ".env", ".git", ".svn",
    "readme.md", "README.txt", "CHANGELOG", "LICENSE", "composer.json",
    "package.json", "web.config", "phpinfo.php", "info.php",
    "shell", "cmd", "exec", "cgi-bin", "scripts", "bin",
    "app", "apps", "application", "portal", "gateway",
    "v1", "v2", "v3", "rest", "graphql", "swagger", "docs", "documentation",
    "status", "health", "ping", "metrics", "monitor",
    "includes", "include", "lib", "library", "plugins", "modules",
    "store", "shop", "cart", "checkout", "payment", "order", "orders",
    "search", "contact", "about", "help", "support", "faq",
    "register", "signup", "signin", "logout", "forgot", "reset",
    "download", "downloads", "export", "import", "feed", "rss",
]

FOUND_PATHS = []
SCAN_STATS = {"requests": 0, "found": 0, "errors": 0, "start_time": None}
STOP_FLAG = threading.Event()
RESULTS_LOCK = threading.Lock()
print_lock = threading.Lock()

# ─── HELPERS ────────────────────────────────────────────────────────────────

def safe_print(*args, **kwargs):
    with print_lock:
        print(*args, **kwargs)

def status_codes_color(code):
    if code in [200, 201, 204]:
        return Fore.GREEN
    elif code in [301, 302, 303, 307, 308]:
        return Fore.CYAN
    elif code in [401, 403]:
        return Fore.YELLOW
    elif code == 404:
        return Fore.RED
    elif code == 500:
        return Fore.MAGENTA
    else:
        return Fore.WHITE

def normalize_url(url):
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    parsed = urlparse(url)
    base = f"{parsed.scheme}://{parsed.netloc}"
    path_prefix = parsed.path.rstrip("/")
    return base, path_prefix

def get_wordlist(custom_path=None, mode="small"):
    """Load best available wordlist."""
    if custom_path and os.path.exists(custom_path):
        safe_print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Using custom wordlist: {custom_path}")
        with open(custom_path, "r", errors="ignore") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]

    # SecLists priority based on mode
    if mode == "large":
        priority = [SECLIST_PATHS[1], SECLIST_PATHS[0], SECLIST_PATHS[2]]
    else:
        priority = [SECLIST_PATHS[0], SECLIST_PATHS[2], SECLIST_PATHS[4], SECLIST_PATHS[3]]

    for path in priority:
        if os.path.exists(path):
            safe_print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Loaded SecList: {Fore.CYAN}{path}{Style.RESET_ALL}")
            with open(path, "r", errors="ignore") as f:
                words = [line.strip() for line in f if line.strip() and not line.startswith("#")]
            safe_print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Wordlist size: {Fore.YELLOW}{len(words):,}{Style.RESET_ALL} entries")
            return words

    safe_print(f"{Fore.YELLOW}[!]{Style.RESET_ALL} SecLists not found. Using built-in wordlist ({len(FALLBACK_WORDLIST)} entries)")
    safe_print(f"    Install: {Fore.CYAN}sudo apt install seclists{Style.RESET_ALL}")
    return FALLBACK_WORDLIST

def load_extensions(ext_string):
    if not ext_string:
        return [""]
    exts = [""] + ["." + e.strip().lstrip(".") for e in ext_string.split(",")]
    return exts

# ─── CORE FUZZER ────────────────────────────────────────────────────────────

class Fuzzer:
    def __init__(self, base_url, path_prefix, wordlist, config):
        self.base_url = base_url
        self.path_prefix = path_prefix
        self.wordlist = wordlist
        self.config = config
        self.session = self._build_session()
        self.found_dirs = []  # for recursive fuzzing
        self.task_queue = queue.Queue()

    def _build_session(self):
        s = requests.Session()
        s.verify = False
        s.headers.update({
            "User-Agent": self.config.get("user_agent", 
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 FUZZR/2.0"),
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
        })
        if self.config.get("cookie"):
            s.headers["Cookie"] = self.config["cookie"]
        if self.config.get("header"):
            for h in self.config["header"]:
                k, v = h.split(":", 1)
                s.headers[k.strip()] = v.strip()
        
        s.max_redirects = 3
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=self.config.get("threads", 30),
            pool_maxsize=self.config.get("threads", 30),
            max_retries=1
        )
        s.mount("http://", adapter)
        s.mount("https://", adapter)
        return s

    def probe(self, url, word, depth=0):
        if STOP_FLAG.is_set():
            return

        try:
            resp = self.session.get(
                url,
                timeout=self.config.get("timeout", 7),
                allow_redirects=True,
                stream=False
            )
            with RESULTS_LOCK:
                SCAN_STATS["requests"] += 1

            code = resp.status_code
            length = len(resp.content)

            # Filter conditions
            filter_codes = self.config.get("filter_codes", [404])
            filter_size = self.config.get("filter_size", None)

            if code in filter_codes:
                return
            if filter_size and length == filter_size:
                return

            # Check for positive hits
            hit_codes = self.config.get("hit_codes", [200, 201, 204, 301, 302, 307, 401, 403])
            if code in hit_codes:
                with RESULTS_LOCK:
                    SCAN_STATS["found"] += 1
                    FOUND_PATHS.append({
                        "url": url,
                        "code": code,
                        "size": length,
                        "word": word,
                        "depth": depth,
                        "redirect": resp.url if resp.url != url else None
                    })

                color = status_codes_color(code)
                depth_indent = "  " * depth + ("└─ " if depth > 0 else "")
                redirect_str = f" → {resp.url}" if resp.url != url else ""
                
                safe_print(
                    f"{color}[{code}]{Style.RESET_ALL} "
                    f"{depth_indent}{Fore.WHITE}{url}{Style.RESET_ALL}"
                    f"{Fore.CYAN}{redirect_str}{Style.RESET_ALL} "
                    f"{Fore.YELLOW}[{length}b]{Style.RESET_ALL}"
                )

                # Auto-recurse into directories
                if self.config.get("recursive") and code in [200, 301, 302, 307]:
                    if not any(url.endswith(ext) for ext in [".php", ".html", ".js", ".css", ".txt", ".xml", ".json"]):
                        clean_url = url.rstrip("/")
                        if clean_url not in self.found_dirs:
                            self.found_dirs.append(clean_url)

        except requests.exceptions.Timeout:
            with RESULTS_LOCK:
                SCAN_STATS["errors"] += 1
        except requests.exceptions.ConnectionError:
            with RESULTS_LOCK:
                SCAN_STATS["errors"] += 1
        except Exception:
            with RESULTS_LOCK:
                SCAN_STATS["errors"] += 1

    def fuzz_path(self, base_path, wordlist, depth=0, extensions=None):
        if extensions is None:
            extensions = [""]

        safe_print(f"\n{Fore.MAGENTA}{'─'*60}{Style.RESET_ALL}")
        safe_print(f"{Fore.MAGENTA}[~] Fuzzing:{Style.RESET_ALL} {Fore.WHITE}{self.base_url}{base_path}/{Style.RESET_ALL} "
                   f"[depth={depth}, words={len(wordlist):,}]")
        safe_print(f"{Fore.MAGENTA}{'─'*60}{Style.RESET_ALL}\n")

        work_queue = queue.Queue()
        for word in wordlist:
            for ext in extensions:
                work_queue.put((word + ext, depth))

        threads_count = min(self.config.get("threads", 30), work_queue.qsize())
        
        def worker():
            while not STOP_FLAG.is_set():
                try:
                    word, d = work_queue.get(timeout=1)
                    if not word:
                        work_queue.task_done()
                        continue
                    url = f"{self.base_url}{base_path}/{word}"
                    self.probe(url, word, d)
                    work_queue.task_done()
                    
                    # Rate limiting
                    delay = self.config.get("delay", 0)
                    if delay > 0:
                        time.sleep(delay / 1000.0)
                except queue.Empty:
                    break

        threads = [threading.Thread(target=worker, daemon=True) for _ in range(threads_count)]
        for t in threads:
            t.start()

        # Progress display
        total = work_queue.qsize() + sum(1 for _ in [None] * len(wordlist) * len(extensions))
        total = len(wordlist) * len(extensions)

        try:
            while any(t.is_alive() for t in threads):
                if STOP_FLAG.is_set():
                    break
                done = total - work_queue.qsize()
                pct = (done / total * 100) if total > 0 else 0
                bar_len = 30
                filled = int(bar_len * pct / 100)
                bar = "█" * filled + "░" * (bar_len - filled)
                with print_lock:
                    sys.stdout.write(
                        f"\r  {Fore.BLUE}[{bar}]{Style.RESET_ALL} "
                        f"{pct:.1f}% | "
                        f"req:{SCAN_STATS['requests']:,} | "
                        f"found:{Fore.GREEN}{SCAN_STATS['found']}{Style.RESET_ALL} | "
                        f"err:{SCAN_STATS['errors']}"
                    )
                    sys.stdout.flush()
                time.sleep(0.3)
        except KeyboardInterrupt:
            STOP_FLAG.set()

        for t in threads:
            t.join(timeout=2)

        print()  # newline after progress bar

    def run(self, extensions=None):
        wordlist = self.wordlist
        self.fuzz_path(self.path_prefix, wordlist, depth=0, extensions=extensions)

        if self.config.get("recursive"):
            max_depth = self.config.get("max_depth", 3)
            visited = set()
            current_dirs = list(self.found_dirs)

            for depth in range(1, max_depth + 1):
                if STOP_FLAG.is_set():
                    break
                new_dirs = []
                for dir_url in current_dirs:
                    if dir_url in visited:
                        continue
                    visited.add(dir_url)
                    path_part = dir_url.replace(self.base_url, "")
                    prev_found = len(FOUND_PATHS)
                    self.found_dirs_snapshot = list(self.found_dirs)
                    self.fuzz_path(path_part, wordlist, depth=depth, extensions=extensions)
                    for d in self.found_dirs:
                        if d not in visited and d not in new_dirs:
                            new_dirs.append(d)
                current_dirs = new_dirs
                if not current_dirs:
                    break

# ─── REPORTING ──────────────────────────────────────────────────────────────

def save_report(output_file, config_info):
    elapsed = time.time() - SCAN_STATS["start_time"]
    report = {
        "tool": "FUZZR v2.0",
        "scan_date": datetime.now().isoformat(),
        "target": config_info.get("target"),
        "elapsed_seconds": round(elapsed, 2),
        "stats": {
            "total_requests": SCAN_STATS["requests"],
            "paths_found": SCAN_STATS["found"],
            "errors": SCAN_STATS["errors"],
        },
        "findings": FOUND_PATHS
    }
    
    with open(output_file, "w") as f:
        json.dump(report, f, indent=2)
    
    safe_print(f"\n{Fore.GREEN}[+]{Style.RESET_ALL} Report saved: {Fore.CYAN}{output_file}{Style.RESET_ALL}")

def print_summary():
    elapsed = time.time() - SCAN_STATS["start_time"]
    safe_print(f"\n{Fore.RED}{'═'*60}{Style.RESET_ALL}")
    safe_print(f"{Fore.WHITE}  SCAN SUMMARY{Style.RESET_ALL}")
    safe_print(f"{Fore.RED}{'─'*60}{Style.RESET_ALL}")
    safe_print(f"  Total Requests : {Fore.YELLOW}{SCAN_STATS['requests']:,}{Style.RESET_ALL}")
    safe_print(f"  Paths Found    : {Fore.GREEN}{SCAN_STATS['found']}{Style.RESET_ALL}")
    safe_print(f"  Errors         : {Fore.RED}{SCAN_STATS['errors']}{Style.RESET_ALL}")
    safe_print(f"  Elapsed Time   : {Fore.CYAN}{elapsed:.1f}s{Style.RESET_ALL}")
    
    if FOUND_PATHS:
        safe_print(f"\n{Fore.GREEN}  ✓ DISCOVERED PATHS:{Style.RESET_ALL}")
        for item in sorted(FOUND_PATHS, key=lambda x: x["code"]):
            color = status_codes_color(item["code"])
            safe_print(f"  {color}[{item['code']}]{Style.RESET_ALL} {item['url']} {Fore.YELLOW}[{item['size']}b]{Style.RESET_ALL}")
    
    safe_print(f"{Fore.RED}{'═'*60}{Style.RESET_ALL}")

# ─── INTERACTIVE MODE ────────────────────────────────────────────────────────

def interactive_mode():
    print(BANNER)
    print(f"{Fore.YELLOW}  ⚠  AUTHORIZED USE ONLY — Ensure you have written permission{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}     before scanning any target. Unauthorized use is illegal.{Style.RESET_ALL}\n")

    # Target
    print(f"{Fore.WHITE}  Enter target URL (e.g. pakaya.com or https://pakaya.com/api):{Style.RESET_ALL}")
    print(f"  {Fore.RED}▶{Style.RESET_ALL} ", end="")
    target = input().strip()
    if not target:
        print(f"{Fore.RED}[!] No target provided. Exiting.{Style.RESET_ALL}")
        sys.exit(1)

    # Mode
    print(f"\n{Fore.WHITE}  Scan mode:{Style.RESET_ALL}")
    print(f"    {Fore.CYAN}[1]{Style.RESET_ALL} Fast   (small wordlist, 50 threads)")
    print(f"    {Fore.CYAN}[2]{Style.RESET_ALL} Normal (medium wordlist, 30 threads)  {Fore.GREEN}[default]{Style.RESET_ALL}")
    print(f"    {Fore.CYAN}[3]{Style.RESET_ALL} Deep   (large wordlist, 20 threads)")
    print(f"  {Fore.RED}▶{Style.RESET_ALL} ", end="")
    mode_input = input().strip() or "2"
    
    mode_map = {"1": ("small", 50), "2": "normal", "3": ("large", 20)}
    if mode_input == "1":
        wl_mode, threads = "small", 50
    elif mode_input == "3":
        wl_mode, threads = "large", 20
    else:
        wl_mode, threads = "small", 30

    # Recursive
    print(f"\n{Fore.WHITE}  Enable recursive fuzzing? (auto-fuzz found directories) [Y/n]:{Style.RESET_ALL}")
    print(f"  {Fore.RED}▶{Style.RESET_ALL} ", end="")
    rec = input().strip().lower()
    recursive = rec != "n"

    # Extensions
    print(f"\n{Fore.WHITE}  File extensions to append (e.g. php,html,txt) or press Enter to skip:{Style.RESET_ALL}")
    print(f"  {Fore.RED}▶{Style.RESET_ALL} ", end="")
    ext_input = input().strip()

    # Output
    print(f"\n{Fore.WHITE}  Save report to file? (e.g. report.json) or press Enter to skip:{Style.RESET_ALL}")
    print(f"  {Fore.RED}▶{Style.RESET_ALL} ", end="")
    output = input().strip()

    return {
        "target": target,
        "wl_mode": wl_mode,
        "threads": threads,
        "recursive": recursive,
        "extensions": ext_input or None,
        "output": output or None,
    }

# ─── SIGNAL HANDLER ─────────────────────────────────────────────────────────

def signal_handler(sig, frame):
    safe_print(f"\n\n{Fore.YELLOW}[!] Scan interrupted by user (Ctrl+C){Style.RESET_ALL}")
    STOP_FLAG.set()

# ─── MAIN ────────────────────────────────────────────────────────────────────

def main():
    signal.signal(signal.SIGINT, signal_handler)

    parser = argparse.ArgumentParser(
        description="FUZZR — Authorized Web Path Fuzzer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 fuzzr.py                          # Interactive mode
  python3 fuzzr.py -u https://pakaya.com    # Quick scan
  python3 fuzzr.py -u https://pakaya.com -r -e php,html -t 50
  python3 fuzzr.py -u https://pakaya.com -w /path/to/wordlist.txt -o report.json
        """
    )
    parser.add_argument("-u", "--url",        help="Target URL")
    parser.add_argument("-w", "--wordlist",   help="Custom wordlist path")
    parser.add_argument("-t", "--threads",    type=int, default=30, help="Thread count (default: 30)")
    parser.add_argument("-e", "--extensions", help="File extensions (e.g. php,html,txt)")
    parser.add_argument("-r", "--recursive",  action="store_true", help="Recursive fuzzing")
    parser.add_argument("--depth",            type=int, default=3, help="Max recursion depth (default: 3)")
    parser.add_argument("--timeout",          type=int, default=7,  help="Request timeout seconds")
    parser.add_argument("--delay",            type=int, default=0,  help="Delay between requests in ms")
    parser.add_argument("--mode",             choices=["small","large"], default="small", help="Wordlist mode")
    parser.add_argument("-o", "--output",     help="Save JSON report to file")
    parser.add_argument("--cookie",           help="Cookie header value")
    parser.add_argument("--header",           action="append", help="Extra header (Key: Value)")
    parser.add_argument("--filter-codes",     help="Comma-separated HTTP codes to ignore (default: 404)")
    parser.add_argument("--filter-size",      type=int, help="Filter responses of this exact byte size")
    parser.add_argument("-q", "--quiet",      action="store_true", help="Minimal output")

    args = parser.parse_args()

    # If no URL provided → interactive mode
    if not args.url:
        cfg = interactive_mode()
        target_url = cfg["target"]
        wordlist = get_wordlist(None, cfg["wl_mode"])
        extensions = load_extensions(cfg["extensions"])
        config = {
            "threads": cfg["threads"],
            "recursive": cfg["recursive"],
            "max_depth": 3,
            "timeout": 7,
            "delay": 0,
            "filter_codes": [404],
            "filter_size": None,
            "cookie": None,
            "header": None,
        }
        output_file = cfg["output"]
    else:
        print(BANNER)
        target_url = args.url
        wordlist = get_wordlist(args.wordlist, args.mode)
        extensions = load_extensions(args.extensions)
        filter_codes = [int(c) for c in args.filter_codes.split(",")] if args.filter_codes else [404]
        config = {
            "threads": args.threads,
            "recursive": args.recursive,
            "max_depth": args.depth,
            "timeout": args.timeout,
            "delay": args.delay,
            "filter_codes": filter_codes,
            "filter_size": args.filter_size,
            "cookie": args.cookie,
            "header": args.header,
        }
        output_file = args.output

    # Normalize URL
    base_url, path_prefix = normalize_url(target_url)

    safe_print(f"\n{Fore.WHITE}  Target   : {Fore.CYAN}{base_url}{path_prefix}{Style.RESET_ALL}")
    safe_print(f"{Fore.WHITE}  Threads  : {Fore.CYAN}{config['threads']}{Style.RESET_ALL}")
    safe_print(f"{Fore.WHITE}  Recursive: {Fore.CYAN}{config['recursive']}{Style.RESET_ALL}")
    safe_print(f"{Fore.WHITE}  Wordlist : {Fore.CYAN}{len(wordlist):,} entries{Style.RESET_ALL}")
    safe_print(f"{Fore.WHITE}  Extensions:{Fore.CYAN} {extensions}{Style.RESET_ALL}")
    safe_print(f"\n{Fore.RED}  Press Ctrl+C to stop at any time{Style.RESET_ALL}\n")
    time.sleep(1)

    SCAN_STATS["start_time"] = time.time()

    fuzzer = Fuzzer(base_url, path_prefix, wordlist, config)
    fuzzer.run(extensions=extensions)

    print_summary()

    if output_file:
        save_report(output_file, {"target": target_url})

if __name__ == "__main__":
    main()
