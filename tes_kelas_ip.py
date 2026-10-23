#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TES KELAS IP — apakah 403 registrationBlocked itu gara-gara kelas IP?

CARA PAKAI (di Termux, HP):
  1. MATIIN Cloudflare WARP dulu
  2. Pastiin HP jalan di DATA SELULER
  3. python3 tes_kelas_ip.py

Apa yang dicek:
  - kelas IP keluar (residensial / datacenter / VPN-proxy)
  - kalau ternyata non-residensial -> hasil tes ini nggak bersih, ulangi sesudah WARP mati
"""

import json
import random
import re
import string
import sys
import time
import uuid

DASAR = "https://muse.ai"
BOX = "https://box.celana-ar-store.my.id"
DOMAIN = "celana-ar-store.my.id"

# ---- HTTP client: curl_cffi kalau ada, kalau nggak pakai requests biasa ----
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
    """Kelas IP keluar — ini yang mau kita ukur."""
    try:
        r = http_get("http://ip-api.com/json/"
                     "?fields=status,country,countryCode,regionName,city,isp,org,as,mobile,proxy,hosting,query",
                     timeout=20)
        d = r.json()
    except Exception as e:
        print(f"[ip] GAGAL baca IP keluar: {type(e).__name__}: {e}")
        return None

    print()
    garis()
    print("IP KELUAR HP INI")
    garis()
    print(f"  IP      : {d.get('query')}")
    print(f"  Negara  : {d.get('country')} ({d.get('countryCode')}) - {d.get('city')}")
    print(f"  ISP     : {d.get('isp')} / {d.get('org')}  [{d.get('as')}]")
    print(f"  mobile  : {d.get('mobile')}   (True = jaringan seluler)")
    print(f"  proxy   : {d.get('proxy')}    (True = kena VPN/proxy)")
    print(f"  hosting : {d.get('hosting')}  (True = IP datacenter)")

    masalah = []
    if d.get("proxy"):
        masalah.append("proxy=True  -> HP masih kena WARP/VPN")
    if d.get("hosting"):
        masalah.append("hosting=True -> ini IP datacenter, bukan residensial")
    if not d.get("mobile"):
        masalah.append("mobile=False -> bukan jaringan seluler")

    print()
    if masalah:
        print("  *** PERINGATAN: kelas IP ini NON-RESIDENSIAL ***")
        for m in masalah:
            print(f"      - {m}")
        print("  -> Hasil tes ini NGGak bersih. Matiin WARP, pakai data seluler, ulangi.")
    else:
        print("  >>> Kelas IP: RESIDENSIAL. Tes ini valid, lanjut.")
    print()
    return d


def bikin_surel():
    local = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"{local}@{DOMAIN}"


def baca_otp(email, timeout=180, interval=5):
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
                        d = mr.json()
                        teks = f"{d.get('subject','')} {d.get('body','')}"
                        mt = re.search(r"\b(\d{6})\b", teks)
                        if mt:
                            print(f"[otp] kode diterima: {mt.group(1)}")
                            return mt.group(1)
        except Exception:
            pass
        time.sleep(interval)
    return None


def jalankan():
    email = bikin_surel()
    print(f"\n[email] {email}")

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

    try:
        r = s.get(DASAR + "/", timeout=25)
        print(f"[landing] HTTP {r.status_code}")

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

        time.sleep(random.uniform(10, 25))
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
    print("  TES KELAS IP - muse.ai")
    print("  Tujuan: apakah 403 registrationBlocked gara-gara kelas IP?")
    print(f"  HTTP client: {'curl_cffi' if HTTP_CF else 'requests (fallback)'}")

    cek_egress()

    print("Mulai registrasi...")
    hasil = jalankan()

    garis()
    print("HASIL TES")
    garis()
    if hasil is None:
        print("  nggak selesai (lihat error di atas)")
    else:
        kode, teks = hasil
        if kode in (200, 201):
            print("  >>> BERHASIL <<<")
            print("  Artinya: kelas IP residensial BISA menembus.")
            print("  Kesimpulan: penyebab 403 itu KELAS IP, bukan domain.")
        else:
            print(f"  >>> GAGAL: HTTP {kode}")
            print(f"  {teks}")
            if kode == 403 and "registrationBlocked" in teks:
                print("  Artinya: IP residensial pun tetap diblokir.")
                print("  Kesimpulan: penyebabnya DOMAIN, bukan kelas IP.")
    garis()
    print("  Kirim ke gw:")
    print("    - baris IP keluar (negara/isp/mobile/proxy/hosting)")
    print("    - baris HASIL TES di atas")
    print()


if __name__ == "__main__":
    main()
