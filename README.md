## Craper Endepoint Beta
Tools ini merupakan Advanced Endpoint & API Discovery Scanner yang dibangun dengan teknologi analisis modern untuk analisis yang cerdas, tools ini mampu mengungkap endpoint yang tidak muncul di permukaan, memahami pola API internal, serta menyajikan data teknis yang relevan untuk keamanan dan validasi sistem

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
pip install requests bs4 urllib3 rich
 git clone https://github.com/opettt-hash/SCRAPER_BETA.git
cd SCRAPER_BETA
python scraper.py
```
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
