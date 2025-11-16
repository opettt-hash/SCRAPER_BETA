# Endpoint Scraper Beta

Tools ini adalah **Endpoint & API Discovery Scanner** yang dirancang dengan kemampuan deep crawling, API discovery, secret key extraction, dan Postman auto‑export.

---

# 📊 Tabel Dokumen Lengkap

## ⭐ Fitur Utama
| Kategori | Deskripsi |
|---------|-----------|
| **Endpoint Auto Extract** | HTML Parser, JS Parser, JS Recursive Crawler, Dynamic Import Detector, AJAX Interceptor |
| **Secret Key Detector** | Deteksi API Key, JWT, Bearer, Firebase, Stripe, AWS, RapidAPI, x-api-key |
| **Website Scanner** | Sitemap scan, robots.txt parser, admin path enum, API enum, mobile/debug path |
| **Smart Path Expansion** | Generate endpoint: login, register, auth, info, update, delete, dll |
| **Multithreading & Proxy** | ThreadPoolExecutor 200 thread, proxy rotator, retry system, custom user-agent |
| **Output Lengkap** | JSON, CSV, TXT, Postman Collection, summary log |

---

## 🔍 Endpoint Auto Extract
| Engine | Kemampuan |
|--------|-----------|
| HTML Parser | href, src, form action, link hidden |
| JS Inline Parser | regex + static code анализ |
| External JS Crawler | recursive scanning |
| Dynamic Import Detector | `import("...")` |
| AJAX Request Detector | fetch(), axios(), xhr |
| URL Pattern Recognizer | /api, /v1, /admin, /graphql |

---

## 🔑 Secret Key Detection
| Jenis Key | Contoh | Deteksi |
|-----------|--------|----------|
| Google API Key | `AIza...` | ✅ |
| Firebase Admin Key | `AAAA:xxxxx` | ✅ |
| Stripe Keys | `sk_live`, `pk_live` | ✅ |
| AWS Access Key | `AKIAxxxx` | ✅ |
| JWT Token | `eyJhbGciOi...` | ✅ |
| Bearer Token | `Bearer xxxxx` | ✅ |
| RapidAPI Key | `x-rapidapi-key` | ✅ |
| x-api-key | Header Custom | ✅ |

---

## 🌐 Website & API Scanner
| Fitur | Status |
|--------|--------|
| Multi-depth crawling | ✅ |
| Recursive link discovery | ✅ |
| robots.txt parser | ❇️ Bisa ignore |
| Sitemap.xml reader | ✅ |
| HEAD/GET validator | ✅ |
| Admin path scan | `/admin`, `/admincp`, `/panel`, `/dashboard` |
| API enumeration | `/api`, `/api/v1`, `/v2`, `/backend`, `/services` |

---

## ⚙️ Smart Path Expansion
| Input Path | Output Path (Generated) |
|-------------|--------------------------|
| `/api/v1/user` | `/login`, `/register`, `/auth`, `/info`, `/update`, `/delete` |
| `/auth` | `/auth/login`, `/auth/refresh`, `/auth/verify` |
| `/admin` | `/admin/login`, `/admin/dashboard`, `/admin/config` |

---

## 🤖 Multithreading + Proxy Rotator
| Fitur | Detail |
|-------|--------|
| Thread | Max 200 |
| Proxy | otomatis rotate |
| Retry | urllib3 + backoff |
| User-Agent rotate | Mobile + Desktop |
| Timeout | 8s default |

---

## 📤 Output Tools
| File | Fungsi |
|------|--------|
| `endpoints_TIMESTAMP.json` | Data lengkap endpoint |
| `endpoints_TIMESTAMP.csv` | Friendly spreadsheet |
| `endpoints_TIMESTAMP.txt` | Raw list |
| `postman_collection_TIMESTAMP.json` | Auto import ke Postman |
| `summary_TIMESTAMP.log` | Ringkasan scan |

---

# 🔧 Instalasi
```bash
pkg install python git -y
pip install requests bs4 urllib3 rich
