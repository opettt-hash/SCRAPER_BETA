#Coded By Rolandino!
"""
"""

import os, re, json, csv, time, random, urllib.parse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict, deque

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup

CONFIG = {
    "TIMEOUT": 8,
    "RETRIES": 2,
    "BACKOFF": 0.5,
    "DELAY_MIN": 0.12,
    "DELAY_MAX": 0.5,
    "DEPTH": 4,
    "WORKERS": 28,
    "JS_WORKERS": 8,
    "HEAD_WORKERS": 20,
    "SAVE_DIR": "hasil",
    "PROXIES_FILE": "proxies.txt",
    "RESPECT_ROBOTS": False,      
    "POSTMAN_EXPORT": True,
    "USER_AGENTS": [
        "Mozilla/5.0 (Linux; Android 12; SM-G998B) AppleWebKit/537.36 Chrome/120.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/118.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15"
    ]
}

PATTERNS = [
    
    r'["\'](https?://[^"\']+/api/[^\s"\']+)["\']',
    r'["\'](https?://[^"\']+/(?:graphql|gql)[^"\']*)["\']',
    r'["\'](https?://[^"\']+/(?:openapi|swagger|v3/api-docs)[^"\']*)["\']',
    r'["\'](https?://[^"\']+/(?:rest|rpc|endpoint|webapi)[^"\']*)["\']',
    r'["\'](https?://[^"\']+/(?:v[0-9]+)[^"\']*)["\']',

    r'["\'](/api/[^\s"\']+)["\']',
    r'["\'](/v[0-9]+/[^\s"\']+)["\']',
    r'["\'](/graphql[^\s"\']*)["\']',
    r'["\'](/gql[^\s"\']*)["\']',
    r'["\'](/rest/[^\s"\']+)["\']',
    
    r'fetch\s*\(\s*["\']([^"\']+)["\']',
    r'\.ajax\s*\(\s*{[^}]*url\s*:\s*["\']([^"\']+)["\']',
    r'\$.get\s*\(\s*["\']([^"\']+)["\']',
    r'\$.post\s*\(\s*["\']([^"\']+)["\']',
    r'\.open\s*\(\s*["\'](GET|POST)["\']\s*,\s*["\']([^"\']+)["\']',
    
    r'["\'](https?://[^"\']+\.json)["\']',
    r'["\'](https?://[^"\']+\.php)["\']',
    r'["\'](https?://[^"\']+\.aspx)["\']',
    r'["\'](https?://[^"\']+\.jsp)["\']',
    
    r'https://[a-z0-9\-]+\.firebaseio\.com',
    r'https://firebasestorage\.googleapis\.com/v0/b/[a-z0-9\-_]+',
    r'https://identitytoolkit\.googleapis\.com/v1/',
    
    r'https://[a-z0-9\-]+\.execute-api\.[a-z0-9\-]+\.amazonaws\.com/[^\s"\']*',
    r'https://api\.cloudflare\.com/[^\s"\']*',
    
    r'https?://(?:\d{1,3}\.){3}\d{1,3}:[0-9]+/[^\s"\']+',
]

KEY_PATTERNS = [
    
    (re.compile(r'["\']?(?:api[_-]?key|apikey|apiKey)["\'\s:=]+([A-Za-z0-9\-_]{16,})', re.I), "API Key"),
    (re.compile(r'["\']?(?:access[_-]?token|accesstoken|accessToken)["\'\s:=]+([A-Za-z0-9\-\._~\+\/=]{16,})', re.I), "Access Token"),
    (re.compile(r'["\']?(?:secret|client[_-]?secret|app[_-]?secret)["\'\s:=]+([A-Za-z0-9\-_]{8,})', re.I), "Client Secret"),
    (re.compile(r'["\']?(?:auth|authorization)["\'\s:=]+Bearer\s+([A-Za-z0-9\-\._~\+\/=]+)', re.I), "Bearer Token"),
    (re.compile(r'eyJ[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+'), "JWT Token"),
    (re.compile(r'AIza[0-9A-Za-z\-_]{35}'), "Google API Key"),
    (re.compile(r'AAAA[A-Za-z0-9_-]{7}:[A-Za-z0-9_-]{140}'), "Firebase Server Key"),
    (re.compile(r'SK[a-zA-Z0-9]{32}'), "Stripe Secret Key"),
    (re.compile(r'pk_live_[A-Za-z0-9]{24,}'), "Stripe Public Key"),
    (re.compile(r'R_[A-Za-z0-9\-_]{32,}'), "RapidAPI Key"),
    (re.compile(r'AKIA[0-9A-Z]{16}'), "AWS Access Key"),
    (re.compile(r'(?i)x-api-key["\'\s:=]+([A-Za-z0-9\-_]{16,})'), "x-api-key"),
    (re.compile(r'(?i)bearer\s+([A-Za-z0-9\-\._~\+\/=]{16,})'), "Bearer"),
]

COMMON_PATHS = [
    "/", "/api/", "/api/v1/", "/api/v2/", "/api/v3/", "/v1/", "/v2/", "/v3/",
    "/auth/login", "/auth/register", "/auth/refresh", "/auth/logout",
    "/users", "/user", "/profile", "/accounts", "/account/settings",
    "/graphql", "/gql", "/rest/", "/rpc/",
    "/swagger.json", "/openapi.json", "/v3/api-docs",
    "/health", "/status", "/ping", "/system/info", "/version",
    "/admin", "/dashboard", "/config", "/settings", "/setup",
    "/mobile/", "/android/", "/ios/", "/webapi/",
    "/api/internal/", "/api/external/", "/api/private/", "/api/public/",
    "/api/data/", "/api/app/", "/api/client/", "/api/server/",
    "/firebase.json", "/manifest.json", "/.well-known/openid-configuration",
    "/sitemap.xml", "/robots.txt", "/feeds/", "/feed/",
    "/api/test/", "/api/dev/", "/api/debug/",
    "/api/upload", "/api/download", "/api/files", "/api/image",
    "/api/payment", "/api/transaction", "/api/invoice",
    "/api/order", "/api/product", "/api/item",
    "/api/validate", "/api/check", "/api/verify",
    "/api/search", "/api/filter", "/api/list",
    "/api/notify", "/api/message", "/api/send",
    "/api/logs", "/api/stats", "/api/monitor"
]

def now_str(): return datetime.now().strftime("%Y%m%d_%H%M%S")

def make_session():
    s = requests.Session()
    retry = Retry(total=CONFIG["RETRIES"], backoff_factor=CONFIG["BACKOFF"],
                  status_forcelist=(429,500,502,503,504),
                  allowed_methods=frozenset(['HEAD','GET','OPTIONS','POST']))
    adapter = HTTPAdapter(max_retries=retry, pool_connections=100, pool_maxsize=100)
    s.mount("https://", adapter); s.mount("http://", adapter)
    s.headers.update({"User-Agent": random.choice(CONFIG["USER_AGENTS"])})
    s.timeout = CONFIG["TIMEOUT"]
    return s

def load_proxies(path=CONFIG["PROXIES_FILE"]):
    if os.path.exists(path):
        with open(path,'r') as f:
            lines = [l.strip() for l in f if l.strip()]
            if lines:
                
                normalized = []
                for l in lines:
                    if l.startswith("http://") or l.startswith("https://"):
                        normalized.append({"http": l, "https": l})
                    else:
                        normalized.append({"http": f"http://{l}", "https": f"http://{l}"})
                return normalized
    return [None]

def choose_proxy(proxies):
    return random.choice(proxies) if proxies and len(proxies)>0 else None

def detect_protocol(target, session):
    if target.startswith("http"):
        return target.rstrip("/")
    for proto in ("https://","http://"):
        try:
            r = session.head(proto + target, timeout=3, allow_redirects=True)
            if r and r.status_code < 500:
                return (proto + target).rstrip("/")
        except:
            pass
    return "https://" + target

def safe_request(session, method, url, **kwargs):
    try:
        return session.request(method, url, timeout=session.timeout, allow_redirects=True, **kwargs)
    except Exception:
        return None

def extract_candidates_from_text(text, base):
    out = set()
    for p in PATTERNS:
        for m in re.findall(p, text, re.I):
            url = m if isinstance(m,str) else (m[0] if isinstance(m,tuple) else str(m))
            full = urllib.parse.urljoin(base, url.strip())
            if not full.lower().endswith((".png",".jpg",".jpeg",".gif",".svg",".css")):
                out.add(full)
    
    for m in re.findall(r'https?://[^\s"\'<>]+', text):
        if any(k in m.lower() for k in ("/api","graphql",".json","openapi","swagger")):
            out.add(m)
    return out

def detect_secrets_in_text(text):
    findings = []
    for regex, tag in KEY_PATTERNS:
        for m in regex.findall(text):
            val = m if isinstance(m,str) else (m[0] if isinstance(m,tuple) else str(m))
            findings.append({"type": tag, "value": val})
    return findings

def fetch_robots(session, base):
    robots = {}
    r = safe_request(session, "GET", urllib.parse.urljoin(base, "/robots.txt"))
    if r and r.status_code == 200:
        robots["text"] = r.text
        robots["sitemaps"] = re.findall(r'(?i)Sitemap:\s*(\S+)', r.text)
    return robots

def fetch_sitemap(session, sitemap_url, proxies):
    found = set()
    r = safe_request(session, "GET", sitemap_url, proxies=choose_proxy(proxies))
    if r and r.status_code == 200:
        for loc in re.findall(r'<loc>([^<]+)</loc>', r.text, re.I):
            found.add(loc.strip())
    return found

def enum_common_paths(session, base, proxies):
    results = {}
    for p in COMMON_PATHS:
        full = urllib.parse.urljoin(base + "/", p.lstrip("/"))
        r = safe_request(session, "HEAD", full, proxies=choose_proxy(proxies))
        if r and r.status_code in (200,201,301,302,401,403,405,500):
            results[full] = {"status": r.status_code, "ctype": r.headers.get("content-type","")}
        else:
            g = safe_request(session, "GET", full, proxies=choose_proxy(proxies))
            if g and g.status_code in (200,201,301,302,401,403,405,500):
                results[full] = {"status": g.status_code, "ctype": g.headers.get("content-type","")}
        time.sleep(random.uniform(CONFIG["DELAY_MIN"], CONFIG["DELAY_MAX"]))
    return results

def crawl_site(session, start_url, proxies):
    depth_limit = CONFIG["DEPTH"]
    visited = set()
    q = deque([(start_url, 0)])
    candidates = set()
    js_urls = set()
    while q:
        url, depth = q.popleft()
        if url in visited or depth > depth_limit:
            continue
        visited.add(url)
        resp = safe_request(session, "GET", url, proxies=choose_proxy(proxies))
        if not resp or resp.status_code != 200:
            
            time.sleep(random.uniform(CONFIG["DELAY_MIN"]*1.5, CONFIG["DELAY_MAX"]*1.5))
            continue
        text = resp.text or ""
        
        soup = BeautifulSoup(text, "html.parser")
        for tag in soup.find_all(["a","link","area","form","iframe","script"]):
            href = tag.get("href") or tag.get("src") or tag.get("action")
            if not href: continue
            full = urllib.parse.urljoin(url, href)
            
            if urllib.parse.urlparse(full).netloc == urllib.parse.urlparse(start_url).netloc:
                if full not in visited and depth+1 <= depth_limit:
                    q.append((full, depth+1))
            
            if full.lower().endswith(".js"):
                js_urls.add(full)
        
        for c in extract_candidates_from_text(text, url):
            candidates.add(c)
        
        for script in soup.find_all("script"):
            stext = script.string
            if stext:
                for c in extract_candidates_from_text(stext, url):
                    candidates.add(c)
                for s in detect_secrets_in_text(stext):
                    candidates.add(f"[SECRET:{s['type']}]{s['value']}")
        time.sleep(random.uniform(CONFIG["DELAY_MIN"], CONFIG["DELAY_MAX"]))
    return candidates, js_urls, visited

def fetch_js_recursive(session, js_urls, proxies, max_depth=2):
    
    found = set()
    visited_js = set()
    q = deque([(u,0) for u in js_urls])
    while q:
        js, depth = q.popleft()
        if not js or js in visited_js or depth>max_depth:
            continue
        visited_js.add(js)
        r = safe_request(session, "GET", js, proxies=choose_proxy(proxies))
        if not r or r.status_code != 200:
            continue
        text = r.text or ""
        for c in extract_candidates_from_text(text, js):
            found.add(c)
        
        for m in re.findall(r'(https?://[^\s"\']+\.js)', text):
            if m not in visited_js:
                q.append((m, depth+1))
        time.sleep(0.01)
    return found

def classify_endpoints(session, urls, proxies):
    results = {}
    with ThreadPoolExecutor(max_workers=CONFIG["HEAD_WORKERS"]) as ex:
        futs = {ex.submit(safe_request, session, "HEAD", u, proxies=choose_proxy(proxies)): u for u in urls}
        for fut in as_completed(futs):
            u = futs[fut]
            r = fut.result()
            if r and r.status_code in (200,201,301,302,401,403,405,500):
                ctype = r.headers.get("content-type","")
                results[u] = {"status": r.status_code, "ctype": ctype, "is_json": ("json" in ctype or "openapi" in ctype or "swagger" in ctype)}
            else:
                g = safe_request(session, "GET", u, proxies=choose_proxy(proxies))
                if g and g.status_code in (200,201,301,302,401,403,405,500):
                    ctype = g.headers.get("content-type","")
                    results[u] = {"status": g.status_code, "ctype": ctype, "is_json": ("json" in ctype or "openapi" in ctype or "swagger" in ctype)}
            time.sleep(0.01)
    return results

def expand_based_on_patterns(found_urls):
    
    additions = set()
    for u in list(found_urls):
        lower = u.lower()
        if re.search(r'/api/.*?/user', lower) or re.search(r'/v\d+/.*?/user', lower):
            base = re.sub(r'(user).*', '', u, flags=re.I)
            for cand in ("users","me","profile","login","logout","register"):
                additions.add(urllib.parse.urljoin(base, cand))
        if '/graphql' in lower and not lower.endswith('/graphql'):
            additions.add(u.split('?')[0])
    return additions

def group_endpoints(endpoints_meta):
    groups = defaultdict(list)
    for u, meta in endpoints_meta.items():
        path = urllib.parse.urlparse(u).path.lower()
        if '/auth' in path or 'login' in path or 'token' in path:
            groups['auth'].append((u,meta))
        elif '/admin' in path:
            groups['admin'].append((u,meta))
        elif '/graphql' in path or 'graphql' in path:
            groups['graphql'].append((u,meta))
        elif re.search(r'/v\d+/', path):
            groups['versioned'].append((u,meta))
        elif 'user' in path or 'profile' in path:
            groups['user'].append((u,meta))
        else:
            groups['other'].append((u,meta))
    return groups

# ---------------- OUTPUT ----------------
def save_all(aggregate, secrets, start_url):
    ts = now_str()
    host = urllib.parse.urlparse(start_url).netloc.replace(":", "_")
    outdir = os.path.join(CONFIG["SAVE_DIR"], f"{host}_{ts}")
    os.makedirs(outdir, exist_ok=True)
    
    with open(os.path.join(outdir, f"endpoints_{ts}.json"), "w", encoding="utf-8") as f:
        json.dump({"meta":{"target": start_url, "generated": ts}, "endpoints": aggregate, "secrets": secrets}, f, indent=2, ensure_ascii=False)
    # csv
    with open(os.path.join(outdir, f"endpoints_{ts}.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["url","status","content_type","is_json","notes"])
        for u,m in aggregate.items():
            w.writerow([u, m.get("status",""), m.get("ctype",""), m.get("is_json",False), m.get("notes","")])
    
    with open(os.path.join(outdir, f"endpoints_{ts}.txt"), "w", encoding="utf-8") as f:
        for u in aggregate.keys():
            f.write(u + "\n")
    
    if CONFIG["POSTMAN_EXPORT"]:
        postman = {"info":{"name":f"Endpoints - {host}","schema":"https://schema.getpostman.com/json/collection/v2.1.0/"},"item":[]}
        for u,m in aggregate.items():
            parsed = urllib.parse.urlparse(u)
            item = {"name": u, "request":{"method":"GET","header":[{"key":"User-Agent","value":requests.Session().headers.get("User-Agent","")}], "url":{"raw":u, "host":[parsed.netloc], "path": parsed.path.strip("/").split("/")}}}
            postman["item"].append(item)
        with open(os.path.join(outdir, f"postman_collection_{ts}.json"), "w", encoding="utf-8") as f:
            json.dump(postman, f, indent=2, ensure_ascii=False)
    
    with open(os.path.join(outdir, f"summary_{ts}.log"), "w", encoding="utf-8") as f:
        f.write(f"Target: {start_url}\nGenerated: {ts}\nTotal endpoints: {len(aggregate)}\nTotal secrets: {len(secrets)}\n")
    print(f"Hasil Disimpan Di: {outdir}")

def main():
    print("=== Premium Beta Endepoint Scraping ===")
    target = input("Target Website: ").strip()
    if not target:
        print("Target Kosong!"); return
    session = make_session()
    proxies = load_proxies()
    start_url = detect_protocol(target, session)
    print(f"Target Terdeteksi: {start_url}")
    if not CONFIG["RESPECT_ROBOTS"]:
        print("Otomatis Bypas Aktif")

    
    robots = fetch_robots(session, start_url)
    sitemap_urls = robots.get("sitemaps", []) if robots else []
    sitemap_urls += [urllib.parse.urljoin(start_url, p) for p in ("/sitemap.xml","/sitemap_index.xml")]
    sitemap_pages = set()
    for s in sitemap_urls:
        sitemap_pages |= fetch_sitemap(session, s, proxies)

    
    print("Mengecek Path")
    enum_paths = enum_common_paths(session, start_url, proxies)

    print("Scraping Halaman Untuk Kandidat Endpoint")
    candidates, js_urls, visited_pages = crawl_site(session, start_url, proxies)
    print(f"Halaman Dikunjungi: {len(visited_pages)}  | Kandidat Awal: {len(candidates)}")

    
    for s in sitemap_pages:
        candidates.add(s)

    
    print(f"Mengambil File Js Eksternal: {len(js_urls)} File")
    js_candidates = fetch_js_recursive(session, js_urls, proxies)
    for c in js_candidates:
        candidates.add(c)

    
    expansions = expand_based_on_patterns(candidates)
    for e in expansions: candidates.add(e)

    
    print("Mengklasifikasi Kandidat (HEAD/GET)")
    classified = classify_endpoints(session, list(candidates | set(enum_paths.keys())), proxies)

    
    aggregate = {}
    for u,meta in classified.items():
        notes = ""
        if "openapi" in (meta.get("ctype") or "").lower() or "swagger" in (meta.get("ctype") or "").lower():
            notes += "openapi/swagger;"
        if "/graphql" in u.lower() or "graphql" in u.lower():
            notes += "graphql;"
        aggregate[u] = {"status": meta.get("status"), "ctype": meta.get("ctype"), "is_json": meta.get("is_json"), "notes": notes}

    
    for u,meta in enum_paths.items():
        if u not in aggregate:
            aggregate[u] = {"status": meta.get("status"), "ctype": meta.get("ctype"), "is_json": ("json" in (meta.get("ctype") or "")), "notes":"enum"}

    print("Mencari Secret/Token Dari Sampel Halaman Dan Js")
    secrets = []
    sample_urls = [u for u in aggregate.keys() if aggregate[u].get("status") and aggregate[u].get("status")<500][:80]
    
    sample_urls += list(list(candidates)[:80])
    with ThreadPoolExecutor(max_workers=10) as ex:
        futs = {ex.submit(safe_request, session, "GET", u, proxies=choose_proxy(proxies)): u for u in set(sample_urls)}
        for fut in as_completed(futs):
            u = futs[fut]
            r = fut.result()
            if r and r.text:
                for s in detect_secrets_in_text(r.text):
                    secrets.append(s)
    
    uniq = []
    seen = set()
    for s in secrets:
        v = s.get("value") if isinstance(s,dict) else str(s)
        if v not in seen:
            uniq.append(s); seen.add(v)

    
    groups = group_endpoints(aggregate)

    
    save_all(aggregate, uniq, start_url)

    
    total = len(aggregate)
    json_like = sum(1 for m in aggregate.values() if m.get("is_json"))
    print(f"Selesai, Total Endpoint: {total} | JSON-like: {json_like} | Secrets Unik: {len(uniq)}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nKeluar")

