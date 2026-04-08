
<style>
  @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Syne:wght@400;700&display=swap');
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: transparent; }
  .root { padding: 1rem 0; font-family: 'Syne', sans-serif; color: var(--color-text-primary); }
  .hero { background: #0a0a0a; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem; border: 0.5px solid #333; }
  .hero-banner { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #e53e3e; line-height: 1.4; letter-spacing: 0; white-space: pre; overflow: auto; }
  .hero-sub { font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #68d391; margin-top: 0.75rem; }
  .hero-sub span { color: #fc8181; }
  .section-label { font-size: 11px; font-weight: 700; letter-spacing: 0.12em; color: var(--color-text-secondary); text-transform: uppercase; margin-bottom: 0.75rem; }
  .step-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 12px; margin-bottom: 1.5rem; }
  .step-card { background: var(--color-background-primary); border: 0.5px solid var(--color-border-tertiary); border-radius: 10px; padding: 1rem; }
  .step-num { display: inline-flex; align-items: center; justify-content: center; width: 26px; height: 26px; background: #1a1a2e; border-radius: 6px; font-family: 'JetBrains Mono', monospace; font-size: 13px; color: #e53e3e; font-weight: 600; margin-bottom: 0.6rem; border: 1px solid #333; }
  .step-title { font-size: 14px; font-weight: 700; margin-bottom: 0.4rem; color: var(--color-text-primary); }
  .step-desc { font-size: 13px; color: var(--color-text-secondary); line-height: 1.5; }
  .terminal { background: #0d0d0d; border-radius: 10px; border: 0.5px solid #2a2a2a; overflow: hidden; margin-bottom: 1.5rem; }
  .term-bar { background: #1a1a1a; padding: 8px 14px; display: flex; align-items: center; gap: 6px; border-bottom: 0.5px solid #2a2a2a; }
  .dot { width: 10px; height: 10px; border-radius: 50%; }
  .dot-r { background: #e53e3e; } .dot-y { background: #ecc94b; } .dot-g { background: #48bb78; }
  .term-label { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #666; margin-left: 8px; }
  .term-body { padding: 1rem 1.25rem; font-family: 'JetBrains Mono', monospace; font-size: 12.5px; line-height: 1.7; }
  .t-prompt { color: #e53e3e; } .t-cmd { color: #68d391; } .t-comment { color: #555; font-style: italic; }
  .t-out { color: #a0aec0; } .t-found { color: #48bb78; font-weight: 600; }
  .t-url { color: #63b3ed; } .t-warn { color: #ecc94b; }
  .cmd-block { background: #111; border-radius: 8px; padding: 0.75rem 1rem; border-left: 3px solid #e53e3e; margin-bottom: 1rem; }
  .cmd-block code { font-family: 'JetBrains Mono', monospace; font-size: 12.5px; color: #68d391; display: block; line-height: 1.7; }
  .cmd-block .cmt { color: #555; font-style: italic; }
  .flag-table { width: 100%; border-collapse: collapse; font-size: 13px; margin-bottom: 1.5rem; }
  .flag-table th { font-size: 11px; font-weight: 700; letter-spacing: 0.1em; color: var(--color-text-secondary); text-transform: uppercase; padding: 0 0 8px; border-bottom: 0.5px solid var(--color-border-tertiary); text-align: left; }
  .flag-table td { padding: 8px 0; border-bottom: 0.5px solid var(--color-border-tertiary); vertical-align: top; }
  .flag-table tr:last-child td { border-bottom: none; }
  .flag { font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #e53e3e; white-space: nowrap; }
  .fdesc { color: var(--color-text-secondary); padding-left: 12px; line-height: 1.5; }
  .badge { display: inline-block; font-size: 10px; font-family: 'JetBrains Mono', monospace; padding: 2px 6px; border-radius: 4px; margin-left: 6px; }
  .b-green { background: #1a3a2a; color: #68d391; border: 1px solid #2a5a3a; }
  .b-yellow { background: #3a2a00; color: #ecc94b; border: 1px solid #5a4400; }
  .note { background: var(--color-background-secondary); border: 0.5px solid var(--color-border-tertiary); border-left: 3px solid #e53e3e; border-radius: 8px; padding: 0.75rem 1rem; margin-bottom: 1.5rem; font-size: 13px; color: var(--color-text-secondary); line-height: 1.6; }
  .note strong { color: var(--color-text-primary); font-weight: 600; }
  .flow { display: flex; align-items: center; gap: 8px; margin-bottom: 1.5rem; flex-wrap: wrap; }
  .flow-box { background: var(--color-background-primary); border: 0.5px solid var(--color-border-tertiary); border-radius: 8px; padding: 0.5rem 0.85rem; font-size: 12px; font-weight: 600; text-align: center; min-width: 90px; }
  .flow-box.active { border-color: #e53e3e; color: #e53e3e; }
  .flow-arrow { color: var(--color-text-secondary); font-size: 14px; }
  .divider { border: none; border-top: 0.5px solid var(--color-border-tertiary); margin: 1.5rem 0; }
</style>

<div class="root">
  <div class="hero">
    <div class="hero-banner">╔══════════════════════════════════════════════════════════════╗
║  ███████╗██╗   ██╗███████╗███████╗██████╗                    ║
║  ██╔════╝██║   ██║╚══███╔╝╚══███╔╝██╔══██╗                   ║
║  █████╗  ██║   ██║  ███╔╝   ███╔╝ ██████╔╝                   ║
║  ██╔══╝  ██║   ██║ ███╔╝   ███╔╝  ██╔══██╗                   ║
║  ██║     ╚██████╔╝███████╗███████╗██║  ██║                    ║
║  ╚═╝      ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝   v2.0            ║
╚══════════════════════════════════════════════════════════════╝</div>
    <div class="hero-sub">Authorized Web Path Fuzzer — <span>Kali Linux</span> — SecLists integrated</div>
  </div>

  <div class="section-label">How it works</div>
  <div class="flow">
    <div class="flow-box active">Enter domain</div>
    <div class="flow-arrow">→</div>
    <div class="flow-box">Load SecLists</div>
    <div class="flow-arrow">→</div>
    <div class="flow-box">Multi-threaded fuzz</div>
    <div class="flow-arrow">→</div>
    <div class="flow-box">Found dir?</div>
    <div class="flow-arrow">→</div>
    <div class="flow-box active">Auto recurse</div>
    <div class="flow-arrow">→</div>
    <div class="flow-box">JSON report</div>
  </div>

  <div class="section-label">Installation — run once</div>
  <div class="terminal">
    <div class="term-bar"><div class="dot dot-r"></div><div class="dot dot-y"></div><div class="dot dot-g"></div><div class="term-label">terminal — kali</div></div>
    <div class="term-body">
<span class="t-comment"># 1. Run the installer</span><br>
<span class="t-prompt">$ </span><span class="t-cmd">chmod +x install.sh && sudo ./install.sh</span><br><br>
<span class="t-comment"># 2. Install SecLists if not already present</span><br>
<span class="t-prompt">$ </span><span class="t-cmd">sudo apt install seclists -y</span><br><br>
<span class="t-comment"># 3. Reload shell (or restart terminal)</span><br>
<span class="t-prompt">$ </span><span class="t-cmd">source ~/.zshrc</span>
    </div>
  </div>

  <div class="section-label">Usage examples</div>
  <div class="cmd-block">
    <code><span class="cmt"># Interactive mode — tool asks everything</span>
python3 fuzzr.py</code>
  </div>
  <div class="cmd-block">
    <code><span class="cmt"># Quick scan with defaults</span>
python3 fuzzr.py -u https://pakaya.com</code>
  </div>
  <div class="cmd-block">
    <code><span class="cmt"># Full scan: recursive + php/html extensions + 50 threads + save report</span>
python3 fuzzr.py -u https://pakaya.com -r -e php,html,txt -t 50 -o report.json</code>
  </div>
  <div class="cmd-block">
    <code><span class="cmt"># Deep mode: big wordlist + custom path prefix</span>
python3 fuzzr.py -u https://pakaya.com/api --mode large -r --depth 4</code>
  </div>
  <div class="cmd-block">
    <code><span class="cmt"># With auth cookie + custom header</span>
python3 fuzzr.py -u https://pakaya.com --cookie "session=abc123" \
  --header "Authorization: Bearer TOKEN" -r -o out.json</code>
  </div>

  <hr class="divider">
  <div class="section-label">All flags</div>
  <table class="flag-table">
    <tr><th>Flag</th><th>Description</th></tr>
    <tr><td class="flag">-u / --url</td><td class="fdesc">Target URL. Supports path prefix (pakaya.com/api)</td></tr>
    <tr><td class="flag">-w / --wordlist</td><td class="fdesc">Custom wordlist path. Auto-detects SecLists if blank</td></tr>
    <tr><td class="flag">-t / --threads</td><td class="fdesc">Concurrent threads (default 30, fast=50, deep=20)</td></tr>
    <tr><td class="flag">-e / --extensions</td><td class="fdesc">Extensions to append: <code>php,html,txt</code></td></tr>
    <tr><td class="flag">-r / --recursive</td><td class="fdesc">Auto-fuzz all discovered directories <span class="badge b-green">key feature</span></td></tr>
    <tr><td class="flag">--depth</td><td class="fdesc">Max recursion depth (default 3)</td></tr>
    <tr><td class="flag">--mode</td><td class="fdesc"><code>small</code> (fast) or <code>large</code> (thorough)</td></tr>
    <tr><td class="flag">--timeout</td><td class="fdesc">Request timeout in seconds (default 7)</td></tr>
    <tr><td class="flag">--delay</td><td class="fdesc">Delay between requests in ms (stealth mode)</td></tr>
    <tr><td class="flag">--filter-codes</td><td class="fdesc">HTTP codes to suppress, e.g. <code>404,400</code></td></tr>
    <tr><td class="flag">--filter-size</td><td class="fdesc">Hide responses of exact byte size (false-positive filter)</td></tr>
    <tr><td class="flag">--cookie</td><td class="fdesc">Cookie string for authenticated scanning</td></tr>
    <tr><td class="flag">--header</td><td class="fdesc">Extra header: <code>"Key: Value"</code> (repeatable)</td></tr>
    <tr><td class="flag">-o / --output</td><td class="fdesc">Save JSON report to file</td></tr>
  </table>

  <div class="section-label">Sample output</div>
  <div class="terminal">
    <div class="term-bar"><div class="dot dot-r"></div><div class="dot dot-y"></div><div class="dot dot-g"></div><div class="term-label">fuzzr running</div></div>
    <div class="term-body">
<span class="t-out">  Target   : https://pakaya.com</span><br>
<span class="t-out">  Threads  : 30 | Recursive: True</span><br>
<span class="t-out">  Wordlist : 4,614 entries (SecLists/common.txt)</span><br>
<span class="t-out">────────────────────────────────────────</span><br>
<span class="t-out">  Fuzzing: https://pakaya.com/ [depth=0]</span><br>
<span class="t-out">────────────────────────────────────────</span><br>
<span class="t-found">[200]</span> <span class="t-url">https://pakaya.com/admin</span> <span class="t-warn">[2341b]</span><br>
<span class="t-found">[301]</span> <span class="t-url">https://pakaya.com/api</span> → /api/ <span class="t-warn">[0b]</span><br>
<span class="t-warn">[403]</span> <span class="t-url">https://pakaya.com/.git</span> <span class="t-warn">[512b]</span><br>
<span class="t-warn">[401]</span> <span class="t-url">https://pakaya.com/dashboard</span> <span class="t-warn">[892b]</span><br>
<span class="t-out">  [████████████████░░░░░░░░░░░░░░] 53% | req:2,450 | found:4 | err:2</span><br><br>
<span class="t-out">  ↳ Auto-recursing into /admin [depth=1]</span><br>
<span class="t-found">[200]</span> <span class="t-url">  └─ https://pakaya.com/admin/users</span> <span class="t-warn">[4102b]</span><br>
<span class="t-found">[200]</span> <span class="t-url">  └─ https://pakaya.com/admin/config</span> <span class="t-warn">[1887b]</span>
    </div>
  </div>

  <div class="note">
    <strong>SecLists wordlists used:</strong> common.txt (4,614 entries) for fast mode — directory-list-2.3-medium.txt (220,560 entries) for large mode. Fallback 200-entry built-in list activates if SecLists isn't installed.
  </div>

  <div class="step-grid">
    <div class="step-card">
      <div class="step-num">01</div>
      <div class="step-title">Clone files</div>
      <div class="step-desc">Copy <code>fuzzr.py</code> and <code>install.sh</code> into a folder on Kali, e.g. <code>~/tools/fuzzr/</code></div>
    </div>
    <div class="step-card">
      <div class="step-num">02</div>
      <div class="step-title">Run installer</div>
      <div class="step-desc">Run <code>sudo ./install.sh</code> — installs SecLists, Python deps, and creates the <code>fuzzr</code> alias</div>
    </div>
    <div class="step-card">
      <div class="step-num">03</div>
      <div class="step-title">Start scanning</div>
      <div class="step-desc">Run <code>python3 fuzzr.py</code> for interactive mode — enter the domain and answer 4 quick questions</div>
    </div>
    <div class="step-card">
      <div class="step-num">04</div>
      <div class="step-title">Review report</div>
      <div class="step-desc">Use <code>-o report.json</code> to save a structured JSON file with all findings, codes, and sizes</div>
    </div>
  </div>
</div>
