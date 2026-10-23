#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TES DOMAIN — apakah 403 registrationBlocked itu gara-gara domain email?

STATUS HIPOTESIS (sudah dibuktikan live):
  kelas IP (residensial / VPN / datacenter) -> BUKAN penyebab.
    Dites dari 4 kelas IP berbeda, semuanya tetap 403:
      - SG + Cloudflare WARP (VPN)
      - US + cloud datacenter
      - ID + seluler residensial (Telkomsel)
  Tersisa: DOMAIN email (disposable / catch-all yang reputasinya udah hangus).

CARA PAKAI (di Termux, HP):
  Mode 1 - domain lu sendiri:
      python3 tes_kelas_ip.py
  Mode 2 - pakai email sendiri (buat tes domain bersih):
      python3 tes_kelas_ip.py namalu@gmail.com
    -> nanti diminta OTP, ketik di sini (jangan dikirim ke chat).

Apa yang dicek:
  - kelas IP keluar (buat catatan)
  - hasil register-completion (403 = domain bermasalah, 200/201 = domain sehat)
"""

import json
import random
import re
import string
import sys
import time

DASAR = "https://muse.ai"
BOX = "https://box.celana-ar-store.my.id"
# Domain pilihan. Default: yang SEGAR (dini-faqih), bukan yang udah hangus.
DOMAIN = "dini-faqih.my.id"
DOMAIN_LAMA = "celana-ar-store.my.id"
DOMAIN_LIST = [DOMAIN, DOMAIN_LAMA]

try:
    from curl_cffi import requests as _r
    HTTP_CF = True
except ImportError:
    import requests as _r
    HTTP_CF = False


def http_get(url, **kw):
    if HTTP_CF:
        kw.setdefault("impersonate", "chrome")
    return _r.get(url, **kw)


def http_post(url, **kw):
    if HTTP_CF:
        kw.setdefault("impersonate", "chrome")
    return _r.post(url, **kw)


def garis(c="="):
    print(c * 60)


def cek_egress():
    """Kelas IP keluar. Robusto: coba beberapa layanan, nggak pernah crash."""
    urls = [
        "http://ip-api.com/json/?fields=status,country,countryCode,regionName,city,isp,org,as,mobile,proxy,hosting,query",
        "https://ipinfo.io/json",
    ]
    d = None
    for u in urls:
        try:
            r = http_get(u, timeout=15)
            if r.status_code == 200:
                j = r.json()
                # normalisasi ipinfo.io -> format ip-api
                # CATATAN: ipinfo.io nggak kasih info kelas (mobile/proxy/hosting).
                # Kita tandai 'unknown' supaya nggak salah klasifikasi.
                if "query" not in j and "ip" in j:
                    j["query"] = j.get("ip")
                    j.setdefault("country", (j.get("country") or ""))
                    j.setdefault("city", j.get("city") or "")
                    j.setdefault("isp", j.get("org") or "")
                    j["_sumber"] = "ipinfo.io"
                d = j
                break
        except Exception:
            continue

    if not d:
        print()
        garis()
        print("IP KELUAR HP INI")
        garis()
        print("  [ip] GAGAL baca IP keluar dari semua layanan.")
        print("  [ip] tes tetap jalan — tapi kelas IP nggak gw catet.")
        print()
        return None

    print()
    garis()
    print("IP KELUAR HP INI")
    garis()
    print(f"  IP      : {d.get('query')}")
    print(f"  Negara  : {d.get('country')} - {d.get('city')}")
    print(f"  ISP     : {d.get('isp')}  [{d.get('as') or ''}]")
    print(f"  mobile  : {d.get('mobile')}   (True = jaringan seluler)")
    print(f"  proxy   : {d.get('proxy')}    (True = kena VPN/proxy)")
    print(f"  hosting : {d.get('hosting')}  (True = IP datacenter)")

    kelas_residensial = bool(d.get("mobile")) and not d.get("proxy")
    if d.get("_sumber") == "ipinfo.io":
        print("  (catatan: ipinfo.io nggak kasih kelas -> kelas IP nggak dinilai)")
    elif not kelas_residensial:
        print("  *** PERINGATAN: kelas IP ini NON-RESIDENSIAL ***")
        print("      -> tes kelas IP nggak bersih, tapi tes DOMAIN tetap valid.")
    else:
        print("  >>> Kelas IP: RESIDENSIAL (seluler, tanpa VPN).")
    print()
    return d


def bikin_surel(domain=None):
    d = domain or DOMAIN
    local = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"{local}@{d}"


def baca_otp_box(email, timeout=180, interval=5):
    """Baca OTP dari box celana-ar-store.my.id."""
    akhir = time.time() + timeout
    kelar = set()
    print(f"[otp] nunggu email masuk ke {email} (maks {timeout}s)...")
    while time.time() < akhir:
        try:
            r = http_get(f"{BOX}/api/inbox", params={"address": email}, timeout=10)
            if r.status_code == 200:
                for m in r.json().get("emails", []):
                    if m.get("id") in kelar:
                        continue
                    kelar.add(m.get("id"))
                    mr = http_get(f"{BOX}/api/read",
                                  params={"address": email, "id": m.get("id")}, timeout=10)
                    if mr.status_code == 200:
                        dd = mr.json()
                        teks = f"{dd.get('subject','')} {dd.get('body','')}"
                        mt = re.search(r"\b(\d{6})\b", teks)
                        if mt:
                            print(f"[otp] kode diterima: {mt.group(1)}")
                            return mt.group(1)
        except Exception:
            pass
        time.sleep(interval)
    return None


def baca_otp(email, timeout=180, interval=5):
    """OTP: otomatis kalau domain box, manual kalau email lu sendiri."""
    if any(email.endswith("@" + d) for d in DOMAIN_LIST):
        return baca_otp_box(email, timeout, interval)

    print()
    print(f"[otp] OTP dikirim ke {email}")
    print("[otp] (ketik di sini, jangan dikirim ke chat siapa pun)")
    batas = time.time() + timeout
    while time.time() < batas:
        try:
            kode = input("  OTP (6 digit): ").strip()
        except EOFError:
            time.sleep(5)
            continue
        if re.fullmatch(r"\d{6}", kode):
            return kode
        print("  format salah, coba lagi.")
    return None


def jalankan(email=None):
    if not email:
        email = bikin_surel()
    print(f"\n[email] {email}")
    print(f"[email] pakai domain sendiri? {'YA' if email.endswith('@'+DOMAIN) else 'TIDAK (email lu)'}")

    s = _r.Session()
    s.headers.update({
        "User-Agent": ("Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36"),
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": DASAR,
        "Referer": DASAR + "/",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
    })

    # Landing page OPSIONAL (gw tes: tanpa landing, restart + send-otp tetap jalan)
    try:
        r = s.get(DASAR + "/", timeout=25, allow_redirects=True)
        print(f"[landing] HTTP {r.status_code}")
    except Exception as e:
        print(f"[landing] dilewati ({type(e).__name__}: {str(e)[:60]})")

    try:
        r = s.post(DASAR + "/api/auth/native/restart", json={}, timeout=30,
                   headers={"Content-Type": "application/json"})
        print(f"[restart] HTTP {r.status_code}")
        if r.status_code not in (200, 201):
            print(f"[restart] {r.text[:200]}")
            return None
        csrf = r.json().get("csrf_token")

        r = s.post(DASAR + "/api/auth/native/send-otp",
                   json={"contact_point": email, "region": "US"}, timeout=30,
                   headers={"Content-Type": "application/json", "x-hatch-csrf-token": csrf})
        print(f"[send-otp] HTTP {r.status_code} {r.text[:160]}")
        if r.status_code not in (200, 201):
            return None

        time.sleep(random.uniform(8, 15))
        otp = baca_otp(email)
        if not otp:
            print("[otp] OTP TIDAK DATANG")
            return None

        r = s.post(DASAR + "/api/auth/native/confirm-otp", json={"otp_code": otp}, timeout=30,
                   headers={"Content-Type": "application/json", "x-hatch-csrf-token": csrf})
        print(f"[confirm-otp] HTTP {r.status_code}")
        if r.status_code not in (200, 201):
            print(f"[confirm-otp] {r.text[:200]}")
            return None
        d = r.json()
        tos = (d.get("tos") or {}).get("content_version")
        print(f"[confirm-otp] state={d.get('registration_state')} tos={tos}")

        dob = f"{random.randint(1985,2004)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
        payload = {"date_of_birth": dob, "first_name": "Galih", "last_name": "Pratama",
                   "tos_content_version": tos}
        r = s.post(DASAR + "/api/auth/native/register-completion", json=payload, timeout=30,
                   headers={"Content-Type": "application/json", "x-hatch-csrf-token": csrf})
        print(f"[register-completion] HTTP {r.status_code}")
        print(f"[register-completion] {r.text[:300]}")
        return r.status_code, r.text[:300]
    except Exception as e:
        print(f"[error] {type(e).__name__}: {e}")
        return None


def main():
    print()
    print("  TES DOMAIN - muse.ai")
    print("  Tujuan: apakah 403 registrationBlocked gara-gara domain email?")
    print(f"  HTTP client: {'curl_cffi' if HTTP_CF else 'requests (fallback)'}")

    arg = sys.argv[1].strip().lower() if len(sys.argv) > 1 else ""

    # Mode: banding (dua domain sekaligus) / celana (domain lama) / email sendiri / default
    if arg == "banding":
        print(f"  Mode: BANDING -> {DOMAIN} (segar) vs {DOMAIN_LAMA} (hangus)")
        cek_egress()
        hasil = {}
        for i, d in enumerate(DOMAIN_LIST):
            if i:
                print("\n[jeda 40s biar nggak kena rate limit...]\n")
                time.sleep(40)
            print(f"\n### DOMAIN: {d} ###")
            hasil[d] = jalankan(bikin_surel(d))
        garis()
        print("HASIL BANDING")
        garis()
        for d in DOMAIN_LIST:
            h = hasil.get(d)
            if h is None:
                print(f"  {d:32s} -> nggak selesai")
            else:
                kode = h[0]
                status = "LOLOS" if kode in (200, 201) else f"GAGAL HTTP {kode}"
                print(f"  {d:32s} -> {status}")
        garis()
        segar = hasil.get(DOMAIN)
        lama = hasil.get(DOMAIN_LAMA)
        if segar and lama and segar[0] in (200, 201) and lama[0] not in (200, 201):
            print("  >>> Domain SEGAR lolos, domain HANGUS gagal.")
            print("  >>> TERTUTUP: penyebabnya DOMAIN. Solusi: domain bersih + rotasi.")
        elif segar and lama and segar[0] not in (200, 201) and lama[0] not in (200, 201):
            print("  >>> Dua-duanya gagal.")
            print("  >>> Domain segar pun diblokir -> curiga jalur HTTP-nya, bukan domain.")
        elif segar and segar[0] in (200, 201) and lama and lama[0] in (200, 201):
            print("  >>> Dua-duanya lolos?! Ada yang aneh, cek manual.")
        else:
            print("  >>> Lihat detail per-domain di atas.")
        garis()
        print("  Kirim ke gw: blok HASIL BANDING di atas")
        print()
        return

    email = None
    if arg and "@" in arg:
        email = sys.argv[1].strip()
        print(f"  Mode: email sendiri ({email})")
    elif arg == "celana":
        email = bikin_surel(DOMAIN_LAMA)
        print(f"  Mode: domain LAMA ({DOMAIN_LAMA})")
    else:
        email = bikin_surel(DOMAIN)
        print(f"  Mode: domain SEGAR ({DOMAIN})")

    cek_egress()

    print("Mulai registrasi...")
    hasil = jalankan(email)

    garis()
    print("HASIL TES")
    garis()
    if hasil is None:
        print("  nggak selesai (lihat error di atas)")
    else:
        kode, teks = hasil
        if kode in (200, 201):
            print("  >>> BERHASIL <<<")
            print("  Artinya: domain ini LOLOS.")
            print("  Kesimpulan: penyebab 403 itu DOMAIN (domain lu yang hangus).")
        else:
            print(f"  >>> GAGAL: HTTP {kode}")
            print(f"  {teks}")
            if kode == 403 and "registrationBlocked" in teks:
                print("  Artinya: domain ini diblokir di langkah terakhir.")
                print("  Kesimpulan: penyebabnya DOMAIN, bukan kelas IP.")
    garis()
    print("  Kirim ke gw:")
    print("    - baris IP keluar (negara/isp/mobile/proxy/hosting)")
    print("    - baris HASIL TES di atas")
    print()


if __name__ == "__main__":
    main()
