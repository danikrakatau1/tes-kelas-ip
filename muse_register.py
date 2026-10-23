#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MUSE.AI REGISTER — pakai browser LOKAL asli (Chromium Playwright).
===============================================================
KENAPA INI YANG WORKS:
  Hyperbrowser (cloud, use_stealth) -> register-completion 403 registrationBlocked.
  Browser lokal asli              -> register-completion 200 (akun kebuat).

BUG YANG SUDAH DIPERBAIKI:
  Form birthday muse.ai itu Radix Select, BUKAN <select> biasa.
  Default-nya tanggal HARI INI -> umur 0 tahun -> 403 underageRegistration.
  <select> native cuma fallback tersembunyi, jadi select_option() nggak ngefek.
  Solusi: buka dropdown, navigasi keyboard (daftarnya scrollable, 150 opsi tahun).

CARA PAKAI:
  python3.12 muse_register.py                 # 1 akun
  python3.12 muse_register.py 3               # 3 akun
  python3.12 muse_register.py 1 dini-faqih.my.id

CATATAN REGION:
  Setelah akun jadi, Muse bisa menampilkan halaman /access ("isn't available in
  your country or region yet") kalau IP keluar lu di region yang belum didukung.
  Akun tetap kebuat; ini soal akses layanan, bukan registrasi.
"""

import json
import os
import random
import re
import string
import sys
import time

import requests
from playwright.sync_api import sync_playwright

BOX = "https://box.celana-ar-store.my.id"
DASAR = "https://muse.ai"
DOMAIN = "celana-ar-store.my.id"
OUT = "/home/agentuser/muse/muse_accounts_local.json"

# Tanggal lahir — umur harus >= 13 tahun
BULAN, HARI, TAHUN = "June", "15", "2000"

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")


def bikin_email(domain):
    local = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"{local}@{domain}"


def nunggu_otp(email, timeout=150, interval=4):
    """Baca OTP dari box. Kalau email di luar domain box, minta ketik manual."""
    if "@" + DOMAIN not in email and "@dini-faqih.my.id" not in email:
        print(f"[otp] OTP dikirim ke {email}")
        print("[otp] ketik di sini (jangan dikirim ke chat)")
        batas = time.time() + timeout
        while time.time() < batas:
            try:
                k = input("  OTP (6 digit): ").strip()
            except EOFError:
                time.sleep(5)
                continue
            if re.fullmatch(r"\d{6}", k):
                return k
            print("  format salah.")
        return None

    mulai = time.time()
    while time.time() - mulai < timeout:
        try:
            r = requests.get(f"{BOX}/api/inbox", params={"address": email}, timeout=10)
            if r.status_code == 200:
                for mail in r.json().get("emails", []):
                    d = requests.get(f"{BOX}/api/read",
                                    params={"address": email, "id": mail.get("id")}, timeout=10)
                    if d.status_code == 200:
                        j = d.json()
                        teks = f"{j.get('subject','')} {j.get('body','')}"
                        m = re.search(r"(?<!\d)(\d{6})(?!\d)", teks)
                        if m:
                            return m.group(1)
        except Exception:
            pass
        time.sleep(interval)
    return None


def label_combobox(page):
    return page.evaluate("""() => Array.from(document.querySelectorAll('button[data-slot="select-trigger"]'))
        .map(c => c.getAttribute('aria-label') + '=' + (c.innerText||'').trim())""")


def highlighted(page):
    return page.evaluate("""() => {
        const h = document.querySelector('[role=option][data-highlighted]')
               || document.querySelector('[role=option][data-state="checked"]');
        return h ? h.innerText.trim() : '';
    }""")


def pilih_opsi(page, label, target):
    """Buka dropdown Radix Select lalu pindah highlight pakai keyboard."""
    trig = page.locator(f'button[data-slot="select-trigger"][aria-label="{label}"]').first
    trig.click(force=True, timeout=8000)
    time.sleep(2)
    opts = page.evaluate("""() => Array.from(document.querySelectorAll('[role=option]'))
        .map(o => o.innerText.trim())""")
    cur = highlighted(page)
    if cur == target:
        page.keyboard.press("Enter")
        time.sleep(1)
        return True
    try:
        # arah dari URUTAN INDEX (daftar tahun urut menurun, jadi jangan bandingin angka)
        arah = "ArrowDown" if opts.index(target) > opts.index(cur) else "ArrowUp"
    except ValueError:
        page.keyboard.press("Escape")
        return False
    for _ in range(200):
        if highlighted(page) == target:
            break
        page.keyboard.press(arah)
        time.sleep(0.1)
    if highlighted(page) != target:
        page.keyboard.press("Escape")
        return False
    page.keyboard.press("Enter")
    time.sleep(1)
    return target in " ".join(label_combobox(page))


def daftar(pages=1):
    hasil = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=[
            "--no-sandbox",
            "--disable-blink-features=AutomationControlled",
            "--disable-dev-shm-usage",
        ])
        for i in range(1, pages + 1):
            if i > 1:
                time.sleep(20)
            email = bikin_email(DOMAIN)
            print(f"\n{'='*56}")
            print(f"  AKUN #{i}/{pages}  ->  {email}")
            print(f"{'='*56}")

            ctx = browser.new_context(
                viewport={"width": 1366, "height": 768},
                user_agent=UA, locale="en-US", timezone_id="America/New_York",
            )
            page = ctx.new_page()
            page.set_default_timeout(8000)

            reg = {"status": None, "body": None}

            def on_resp(resp):
                if "register-completion" in resp.url:
                    reg["status"] = resp.status
                    try:
                        reg["body"] = resp.text()
                    except Exception:
                        reg["body"] = None
            page.on("response", on_resp)

            try:
                page.goto(DASAR + "/join", timeout=60000)
                time.sleep(5)
                page.locator("input").first.fill(email)
                time.sleep(1)
                page.locator("button:has-text('Continue')").first.click(force=True)
                time.sleep(8)

                otp = nunggu_otp(email)
                print(f"[1] OTP = {otp}")
                if not otp:
                    hasil.append({"email": email, "status": "no_otp"})
                    ctx.close()
                    continue

                for sel in ["input[autocomplete='one-time-code']",
                            "input[inputmode='numeric']", "input[maxlength='6']"]:
                    try:
                        loc = page.locator(sel)
                        if loc.count() > 0:
                            try:
                                loc.first.fill(otp, force=True)
                            except Exception:
                                pass
                            time.sleep(1)
                            break
                    except Exception:
                        pass

                for _ in range(40):
                    if page.locator('button[data-slot="select-trigger"]').count() >= 3:
                        break
                    time.sleep(1)

                for label, val in (("Month", BULAN), ("Day", HARI), ("Year", TAHUN)):
                    try:
                        pilih_opsi(page, label, val)
                    except Exception:
                        pass
                    time.sleep(1)
                print(f"[2] birthday = {label_combobox(page)}")

                page.locator("button[type='submit']").first.click(force=True, timeout=8000)
                time.sleep(15)

                try:
                    ins = page.locator("input:visible")
                    n = ins.count()
                    print(f"[3] input nama = {n}")
                    if n >= 2:
                        ins.nth(0).fill(random.choice(["Rizky", "Budi", "Andi", "Dewi"]),
                                       force=True, timeout=8000)
                        time.sleep(0.5)
                        ins.nth(1).fill(random.choice(["Pratama", "Santoso", "Wijaya"]),
                                       force=True, timeout=8000)
                        time.sleep(1)
                except Exception:
                    pass

                page.locator("button[type='submit']").first.click(force=True, timeout=8000)
                time.sleep(20)

                body = page.inner_text("body") or ""
                sukses = reg["status"] in (200, 201)
                region_lock = "isn’t available in your country" in body or \
                              "isn't available in your country" in body
                print(f"[4] register-completion = HTTP {reg['status']}")
                print(f"[5] url = {page.url}")
                print(f"[6] region lock? = {region_lock}")

                cks = ctx.cookies()
                sesi = [c.get("value") for c in cks if c.get("name") == "hatch_sess"]

                hasil.append({
                    "email": email,
                    "status": "ok" if sukses else f"http_{reg['status']}",
                    "register_http": reg["status"],
                    "register_body": (reg["body"] or "")[:400],
                    "url": page.url,
                    "region_lock": region_lock,
                    "ada_sesi": bool(sesi),
                })
                try:
                    page.screenshot(path=f"/home/agentuser/muse/akun_{i}.png")
                except Exception:
                    pass
                ctx.close()

            except Exception as e:
                print(f"[-] error: {e}")
                hasil.append({"email": email, "status": f"error: {e}"})
                try:
                    ctx.close()
                except Exception:
                    pass

        browser.close()

    # simpan
    try:
        ada = json.load(open(OUT)) if os.path.exists(OUT) else []
    except Exception:
        ada = []
    ada.extend(hasil)
    json.dump(ada, open(OUT, "w"), indent=2)

    print(f"\n{'='*56}")
    print("RINGKASAN")
    print(f"{'='*56}")
    for h in hasil:
        print(f"  {h['email']:34s} -> {h['status']}"
              + (" (region lock)" if h.get("region_lock") else ""))
    print(f"\n[tersimpan] {OUT}")
    return hasil


if __name__ == "__main__":
    n = 1
    for a in sys.argv[1:]:
        if a.isdigit():
            n = int(a)
        elif "@" not in a and "." in a:
            DOMAIN = a
    print(f"[*] target {n} akun | domain {DOMAIN}")
    daftar(n)
