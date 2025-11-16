# Endpoint Scraper Beta

Tools ini adalah **Endpoint & API Discovery Scanner** yang dirancang dengan kemampuan deep crawling, API discovery, secret key extraction, dan otomatis xploitasi

---
## Fitur Utama
| Kategori | Deskripsi |
|---------|-----------|
| **Endpoint Auto Extract** | HTML Parser, JS Parser, JS Recursive Crawler, Dynamic Import Detector, AJAX Interceptor |
| **Secret Key Detector** | Deteksi API Key, JWT, Bearer, Firebase, Stripe, AWS, RapidAPI, x-api-key |
| **Website Scanner** | Sitemap scan, robots.txt parser, admin path enum, API enum, mobile/debug path |
| **Smart Path Expansion** | Generate endpoint: login, register, auth, info, update, delete, dll |
| **Multithreading & Proxy** | ThreadPoolExecutor 200 thread, proxy rotator, retry system, custom user-agent |
| **Output Lengkap** | JSON, CSV, TXT, Postman Collection, summary log |

---

## Endpoint Auto Extract
| Engine | Kemampuan |
|--------|-----------|
| HTML Parser | href, src, form action, link hidden |
| JS Inline Parser | regex + static code анализ |
| External JS Crawler | recursive scanning |
| Dynamic Import Detector | `import("...")` |
| AJAX Request Detector | fetch(), axios(), xhr |
| URL Pattern Recognizer | /api, /v1, /admin, /graphql |

---

## Secret Key Detection
| Jenis Key | Contoh | Deteksi |
|-----------|--------|----------|
| Google API Key | `AIza...` | ✓ |
| Firebase Admin Key | `AAAA:xxxxx` | ✓ |
| Stripe Keys | `sk_live`, `pk_live` | ✓ |
| AWS Access Key | `AKIAxxxx` | ✓ |
| JWT Token | `eyJhbGciOi...` | ✓ |
| Bearer Token | `Bearer xxxxx` | ✓ |
| x-api-key | Header Custom | ✓ |

---

## Website & API Scanner
| Fitur | Status |
|--------|--------|
| Multi-depth crawling |  |
| Recursive link discovery |  |
| robots.txt parser |  Bisa ignore |
| Sitemap.xml reader |  |
| HEAD/GET validator |  |
| Admin path scan | `/admin`, `/admincp`, `/panel`, `/dashboard` |
| API enumeration | `/api`, `/api/v1`, `/v2`, `/backend`, `/services` |

---

## Smart Path Expansion
| Input Path | Output Path (Generated) |
|-------------|--------------------------|
| `/api/v1/user` | `/login`, `/register`, `/auth`, `/info`, `/update`, `/delete` |
| `/auth` | `/auth/login`, `/auth/refresh`, `/auth/verify` |
| `/admin` | `/admin/login`, `/admin/dashboard`, `/admin/config` |

---

## Multithreading + Proxy Rotator
| Fitur | Detail |
|-------|--------|
| Thread | Max 200 |
| Proxy | otomatis rotate |
| Retry | urllib3 + backoff |
| User-Agent rotate | Mobile + Desktop |
| Timeout | 8s default |

---

## Output Tools
| File | Fungsi |
|------|--------|
| `endpoints_TIMESTAMP.json` | Data lengkap endpoint |
| `endpoints_TIMESTAMP.csv` | Friendly spreadsheet |
| `endpoints_TIMESTAMP.txt` | Raw list |
| `postman_collection_TIMESTAMP.json` | Auto import ke Postman |
| `summary_TIMESTAMP.log` | Ringkasan scan |

---

# Instalasi
```bash
pkg install python git -y
pip install requests bs4 urllib3 rich
```

# Cara Pakai Lengkap

## Mode Dasar
| Fungsi | Command | Keterangan |
|--------|---------|-------------|
| Scan dasar | `python scraper.py --url https://target.com` | Scan cepat tanpa fitur tambahan |
| Scan + simpan otomatis | `python scraper.py --url https://target.com --save` | Output JSON/CSV/TXT otomatis |

---

## Mode Web Scraping
| Fungsi | Command | Keterangan |
|--------|---------|-------------|
| Crawling multi-depth | `python scraper.py --url https://site.com --deep` | Mengaktifkan scan recursive |
| Atur depth | `python scraper.py --url https://site.com --depth 5` | Depth 1–10 |
| Scan JS recursive | `python scraper.py --url https://site.com --js-scan` | Memaksa scan semua file JS |

---

## Mode API & Endpoint Scan
| Fungsi | Command | Keterangan |
|--------|---------|-------------|
| Scan API otomatis | `python scraper.py --url https://site.com --api` | Cari endpoint `/api/*` |
| Scan + generate endpoint | `python scraper.py --url https://site.com --expand` | Smart Path Expansion aktif |
| Scan GraphQL | `python scraper.py --url https://site.com --graphql` | Cari `/graphql` & schema |

---

## Mode Secret Key Detector
| Fungsi | Command | Keterangan |
|--------|---------|-------------|
| Deteksi semua secret | `python scraper.py --url https://site.com --secrets` | API Key, JWT, AWS, Firebase |
| Deteksi Firebase | `python scraper.py --url https://site.com --firebase` | Firebase config extractor |
| Deteksi AWS Key | `python scraper.py --url https://site.com --aws` | `AKIAxxxx` + SecretKey |

---

## Mode Kecepatan (Threading)
| Fungsi | Command | Keterangan |
|--------|---------|-------------|
| Gunakan 50 thread | `python scraper.py --url https://site.com --threads 50` | Mode cepat |
| Mode full speed | `python scraper.py --url https://site.com --threads 200` | Maximum speed |

---

## Proxy & User-Agent
| Fungsi | Command | Keterangan |
|--------|---------|-------------|
| Gunakan proxy list | `python scraper.py --url https://site.com --proxy proxy.txt` | Rotasi otomatis |
| Gunakan proxy tunggal | `python scraper.py --url https://site.com --proxy http://127.0.0.1:8080` | Proxy manual |
| Random UA | `python scraper.py --url https://site.com --random-ua` | Mobile + Desktop mix |
| Set custom UA | `python scraper.py --url https://site.com --ua "Mozilla/5.0"` | Manual UA |

---

## Filter & Rules
| Fungsi | Command | Keterangan |
|--------|---------|-------------|
| Whitelist path | `python scraper.py --url https://site.com --allow api,auth,user` | Hanya scan folder tertentu |
| Blacklist path | `python scraper.py --url https://site.com --deny admin,debug,static` | Skip folder tertentu |
| Ignore robots.txt | `python scraper.py --url https://site.com --ignore-robots` | Scan tanpa dibatasi |

---

## Output & Export
| Fungsi | Command | Keterangan |
|--------|---------|-------------|
| Export Postman | `python scraper.py --url https://site.com --postman` | Auto generate `.postman.json` |
| Export ke folder lain | `python scraper.py --url https://site.com --output results/` | Custom output folder |
| Simpan JSON | `python scraper.py --url https://site.com --json` | Export JSON saja |
| Simpan CSV | `python scraper.py --url https://site.com --csv` | Export CSV saja |
| Simpan TXT | `python scraper.py --url https://site.com --txt` | Export list TXT |

---

## Mode Debug & Testing
| Fungsi | Command | Keterangan |
|--------|---------|-------------|
| Mode debug | `python scraper.py --url https://site.com --debug` | Menampilkan log internal |
| Cek status endpoint | `python scraper.py --url https://site.com --check` | HTTP status checker |
| Print semua JS file | `python scraper.py --url https://site.com --list-js` | Debug resource |

---

## Contoh Kombinasi Paling Laris
| Tujuan | Command |
|--------|---------|
| Deep scan + secret + postman + thread 100 | `python scraper.py --url https://target.com --deep --secrets --postman --threads 100` |
| Full API scan + expand | `python scraper.py --url https://target.com --api --expand` |
| Proxy + deep JS crawler | `python scraper.py --url https://target.com --proxy proxy.txt --js-scan --deep` |
| Crawl + bypass robots | `python scraper.py --url https://target.com --ignore-robots --deep` |

---

# Tips
| Tip | Manfaat |
|------|---------|
| Gunakan proxy list minimal 50 | Supaya tidak kena rate‑limit |
| Aktifkan --random-ua | Menghindari blokir bot |
| Gunakan --expand | Munculin endpoint tersembunyi |
| Gunakan --secrets | Buka peluang temukan API KEY |

---
# Peringatan

| Bagian | Pernyataan |
|--------|------------|
| Tujuan Penggunaan | Perangkat lunak ini dikembangkan untuk keperluan **penelitian keamanan siber**, **audit sistem**, dan **penetration testing** yang dilakukan secara **sah dan berizin**. |
| Kepemilikan & Akses | Seluruh aktivitas pengujian hanya boleh dilakukan pada sistem, server, atau aplikasi yang **dimiliki secara sah** oleh pengguna atau ketika pengguna telah memperoleh **izin tertulis** dari pemilik sistem. |
| Batasan Penggunaan | Dilarang menggunakan perangkat ini untuk tujuan yang bertentangan dengan hukum, seperti: akses ilegal, peretasan, pencurian data, gangguan layanan, ataupun aktivitas merugikan lainnya. |
| Tanggung Jawab Pengguna | Segala bentuk tindakan, hasil, dan konsekuensi yang timbul dari penggunaan perangkat ini sepenuhnya menjadi **tanggung jawab pengguna**. Pengembang tidak bertanggung jawab atas penyalahgunaan dalam bentuk apa pun. |
| Kepatuhan Hukum | Pengguna diharuskan mematuhi seluruh peraturan perundang‑undangan yang berlaku, termasuk regulasi keamanan data, privasi, dan etika penggunaan teknologi informasi. |
| Ketentuan Lisensi | Dengan menggunakan perangkat ini, pengguna menyetujui bahwa perangkat hanya digunakan untuk keperluan profesional yang sah, serta tidak untuk melakukan tindakan yang mengancam keamanan sistem mana pun. |
| Tujuan Edukasi | Dokumentasi, kode, dan seluruh komponen proyek ini disediakan sebagai materi edukasi dan referensi teknis bagi para profesional keamanan informasi. |

---
