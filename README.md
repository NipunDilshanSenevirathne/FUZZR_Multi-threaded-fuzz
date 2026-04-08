@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Syne:wght@400;700&display=swap'); \* { box-sizing: border-box; margin: 0; padding: 0; } body { background: transparent; } .root { padding: 1rem 0; font-family: 'Syne', sans-serif; color: var(--color-text-primary); } .hero { background: #0a0a0a; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem; border: 0.5px solid #333; } .hero-banner { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #e53e3e; line-height: 1.4; letter-spacing: 0; white-space: pre; overflow: auto; } .hero-sub { font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #68d391; margin-top: 0.75rem; } .hero-sub span { color: #fc8181; } .section-label { font-size: 11px; font-weight: 700; letter-spacing: 0.12em; color: var(--color-text-secondary); text-transform: uppercase; margin-bottom: 0.75rem; } .step-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 12px; margin-bottom: 1.5rem; } .step-card { background: var(--color-background-primary); border: 0.5px solid var(--color-border-tertiary); border-radius: 10px; padding: 1rem; } .step-num { display: inline-flex; align-items: center; justify-content: center; width: 26px; height: 26px; background: #1a1a2e; border-radius: 6px; font-family: 'JetBrains Mono', monospace; font-size: 13px; color: #e53e3e; font-weight: 600; margin-bottom: 0.6rem; border: 1px solid #333; } .step-title { font-size: 14px; font-weight: 700; margin-bottom: 0.4rem; color: var(--color-text-primary); } .step-desc { font-size: 13px; color: var(--color-text-secondary); line-height: 1.5; } .terminal { background: #0d0d0d; border-radius: 10px; border: 0.5px solid #2a2a2a; overflow: hidden; margin-bottom: 1.5rem; } .term-bar { background: #1a1a1a; padding: 8px 14px; display: flex; align-items: center; gap: 6px; border-bottom: 0.5px solid #2a2a2a; } .dot { width: 10px; height: 10px; border-radius: 50%; } .dot-r { background: #e53e3e; } .dot-y { background: #ecc94b; } .dot-g { background: #48bb78; } .term-label { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #666; margin-left: 8px; } .term-body { padding: 1rem 1.25rem; font-family: 'JetBrains Mono', monospace; font-size: 12.5px; line-height: 1.7; } .t-prompt { color: #e53e3e; } .t-cmd { color: #68d391; } .t-comment { color: #555; font-style: italic; } .t-out { color: #a0aec0; } .t-found { color: #48bb78; font-weight: 600; } .t-url { color: #63b3ed; } .t-warn { color: #ecc94b; } .cmd-block { background: #111; border-radius: 8px; padding: 0.75rem 1rem; border-left: 3px solid #e53e3e; margin-bottom: 1rem; } .cmd-block code { font-family: 'JetBrains Mono', monospace; font-size: 12.5px; color: #68d391; display: block; line-height: 1.7; } .cmd-block .cmt { color: #555; font-style: italic; } .flag-table { width: 100%; border-collapse: collapse; font-size: 13px; margin-bottom: 1.5rem; } .flag-table th { font-size: 11px; font-weight: 700; letter-spacing: 0.1em; color: var(--color-text-secondary); text-transform: uppercase; padding: 0 0 8px; border-bottom: 0.5px solid var(--color-border-tertiary); text-align: left; } .flag-table td { padding: 8px 0; border-bottom: 0.5px solid var(--color-border-tertiary); vertical-align: top; } .flag-table tr:last-child td { border-bottom: none; } .flag { font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #e53e3e; white-space: nowrap; } .fdesc { color: var(--color-text-secondary); padding-left: 12px; line-height: 1.5; } .badge { display: inline-block; font-size: 10px; font-family: 'JetBrains Mono', monospace; padding: 2px 6px; border-radius: 4px; margin-left: 6px; } .b-green { background: #1a3a2a; color: #68d391; border: 1px solid #2a5a3a; } .b-yellow { background: #3a2a00; color: #ecc94b; border: 1px solid #5a4400; } .note { background: var(--color-background-secondary); border: 0.5px solid var(--color-border-tertiary); border-left: 3px solid #e53e3e; border-radius: 8px; padding: 0.75rem 1rem; margin-bottom: 1.5rem; font-size: 13px; color: var(--color-text-secondary); line-height: 1.6; } .note strong { color: var(--color-text-primary); font-weight: 600; } .flow { display: flex; align-items: center; gap: 8px; margin-bottom: 1.5rem; flex-wrap: wrap; } .flow-box { background: var(--color-background-primary); border: 0.5px solid var(--color-border-tertiary); border-radius: 8px; padding: 0.5rem 0.85rem; font-size: 12px; font-weight: 600; text-align: center; min-width: 90px; } .flow-box.active { border-color: #e53e3e; color: #e53e3e; } .flow-arrow { color: var(--color-text-secondary); font-size: 14px; } .divider { border: none; border-top: 0.5px solid var(--color-border-tertiary); margin: 1.5rem 0; }

╔══════════════════════════════════════════════════════════════╗ ║ ███████╗██╗ ██╗███████╗███████╗██████╗ ║ ║ ██╔════╝██║ ██║╚══███╔╝╚══███╔╝██╔══██╗ ║ ║ █████╗ ██║ ██║ ███╔╝ ███╔╝ ██████╔╝ ║ ║ ██╔══╝ ██║ ██║ ███╔╝ ███╔╝ ██╔══██╗ ║ ║ ██║ ╚██████╔╝███████╗███████╗██║ ██║ ║ ║ ╚═╝ ╚═════╝ ╚══════╝╚══════╝╚═╝ ╚═╝ v2.0 ║ ╚══════════════════════════════════════════════════════════════╝

Authorized Web Path Fuzzer — Kali Linux — SecLists integrated

How it works

Enter domain

→

Load SecLists

→

Multi-threaded fuzz

→

Found dir?

→

Auto recurse

→

JSON report

Installation — run once

terminal — kali

\# 1. Run the installer  
$ chmod +x install.sh && sudo ./install.sh  
  
\# 2. Install SecLists if not already present  
$ sudo apt install seclists -y  
  
\# 3. Reload shell (or restart terminal)  
$ source ~/.zshrc

Usage examples

`# Interactive mode — tool asks everything python3 fuzzr.py`

`# Quick scan with defaults python3 fuzzr.py -u https://pakaya.com`

`# Full scan: recursive + php/html extensions + 50 threads + save report python3 fuzzr.py -u https://pakaya.com -r -e php,html,txt -t 50 -o report.json`

`# Deep mode: big wordlist + custom path prefix python3 fuzzr.py -u https://pakaya.com/api --mode large -r --depth 4`

`# With auth cookie + custom header python3 fuzzr.py -u https://pakaya.com --cookie "session=abc123" \ --header "Authorization: Bearer TOKEN" -r -o out.json`

* * *

All flags

Flag

Description

\-u / --url

Target URL. Supports path prefix (pakaya.com/api)

\-w / --wordlist

Custom wordlist path. Auto-detects SecLists if blank

\-t / --threads

Concurrent threads (default 30, fast=50, deep=20)

\-e / --extensions

Extensions to append: `php,html,txt`

\-r / --recursive

Auto-fuzz all discovered directories key feature

\--depth

Max recursion depth (default 3)

\--mode

`small` (fast) or `large` (thorough)

\--timeout

Request timeout in seconds (default 7)

\--delay

Delay between requests in ms (stealth mode)

\--filter-codes

HTTP codes to suppress, e.g. `404,400`

\--filter-size

Hide responses of exact byte size (false-positive filter)

\--cookie

Cookie string for authenticated scanning

\--header

Extra header: `"Key: Value"` (repeatable)

\-o / --output

Save JSON report to file

Sample output

fuzzr running

Target : https://pakaya.com  
Threads : 30 | Recursive: True  
Wordlist : 4,614 entries (SecLists/common.txt)  
────────────────────────────────────────  
Fuzzing: https://pakaya.com/ \[depth=0\]  
────────────────────────────────────────  
\[200\] https://pakaya.com/admin \[2341b\]  
\[301\] https://pakaya.com/api → /api/ \[0b\]  
\[403\] https://pakaya.com/.git \[512b\]  
\[401\] https://pakaya.com/dashboard \[892b\]  
\[████████████████░░░░░░░░░░░░░░\] 53% | req:2,450 | found:4 | err:2  
  
↳ Auto-recursing into /admin \[depth=1\]  
\[200\] └─ https://pakaya.com/admin/users \[4102b\]  
\[200\] └─ https://pakaya.com/admin/config \[1887b\]

**SecLists wordlists used:** common.txt (4,614 entries) for fast mode — directory-list-2.3-medium.txt (220,560 entries) for large mode. Fallback 200-entry built-in list activates if SecLists isn't installed.

01

Clone files

Copy `fuzzr.py` and `install.sh` into a folder on Kali, e.g. `~/tools/fuzzr/`

02

Run installer

Run `sudo ./install.sh` — installs SecLists, Python deps, and creates the `fuzzr` alias

03

Start scanning

Run `python3 fuzzr.py` for interactive mode — enter the domain and answer 4 quick questions

04

Review report

Use `-o report.json` to save a structured JSON file with all findings, codes, and sizes
