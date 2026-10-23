#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
muke_v2.py — DAFTAR TEMBUS + REFF + REBIND CELANA
=================================================
Alur (sesuai rancangan bosku):

  [1] LOGIN SEKALI pakai email TEMBUS (akun yang sudah ada / tembus verif CC + umur)
  [2] UNBIND tembus  ->  BIND email celana / dini-faqih
  [3] LOGOUT
  [4] LOOP N x:
        DAFTAR (email tembus, OTP manual, nama manusia normal, DOB 2000-12-12)
        -> CEK ccv-status (skip redeem kalau kena verif CC/umur)
        -> REDEEM kode reff (FO3DHT)
        -> UNBIND tembus -> BIND celana/dini-faqih
        -> LOGOUT

Aturan:
  * Email TEMBUS  : diketik manual tiap run. OTP juga dimasukkan manual.
  * Email celana  : cuma buat UNBIND / BIND. Dibuat otomatis, OTP dibaca dari box.
  * Nama          : acak dari daftar nama manusia normal (NGARAN_DEPAN / NGARAN_TUKANG).
  * DOB           : fixed 12 Desember 2000.
  * Redeem code   : default FO3DHT.

Reusable dari muke.py (import muke as M).
"""

import os
import sys
import time
import random
import string
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import muke as M
except Exception as e:
    print(f"[-] gagal import muke.py: {type(e).__name__}: {e}")
    sys.exit(1)

# ------------------------------------------------------------------ state
ST = {
    'tembus': '',
    'domain': 'celana-ar-store.my.id',
    'box': 'https://box.celana-ar-store.my.id',
    'reff': 'FO3DHT',
    'jumlah': 1,
    'dob': '2000-12-12',
    'proxy': '',
}

DIR_SAYA = os.path.dirname(os.path.abspath(__file__))
OUT_HASIL = os.path.join(DIR_SAYA, 'muke_v2_hasil.json')
OUT_LOG = os.path.join(DIR_SAYA, 'muke_v2.log')


def log(teks):
    print(teks, flush=True)
    try:
        with open(OUT_LOG, 'a', encoding='utf-8') as f:
            f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {teks}\n")
    except Exception:
        pass


# ------------------------------------------------------------------ OTP
def box_url_aktif():
    """Cari box yang bisa dijangkau. Return (url, catatan) atau (None, alasan)."""
    kandidat = [f"https://box.{ST['domain']}"]
    if ST['domain'] != 'celana-ar-store.my.id':
        kandidat.append('https://box.celana-ar-store.my.id')
    for u in kandidat:
        try:
            r = M.preq.get(f"{u}/api/inbox",
                           params={'address': 'probe@' + ST['domain']}, timeout=12)
            if r.status_code in (200, 400):
                cat = ('dipakai langsung' if u == kandidat[0]
                       else f'box domain ini nggak ada — fallback ke {u}')
                return u, cat
        except Exception:
            continue
    return None, 'tidak ada box yang bisa dijangkau'


def otp_dari_box(surel, timeout=180, interval=5):
    if not ST.get('_box'):
        log(f'   ⚠  box nggak terjangkau buat {surel} — OTP diminta manual')
        return M.otp_konsol(surel)
    tm = M.TempMail()
    tm.base_url = ST['_box']
    tm.domain = ST['domain']
    tm.email = surel
    print(f"   [otp] nunggu OTP di box buat {surel} (maks {timeout}s)...", flush=True)
    return tm.wait_for_otp(timeout=timeout, interval=interval)


def otp_provider(surel):
    """Dispatcher OTP: tembus -> manual, celana/dini-faqih -> box."""
    if (surel or '').strip().lower() == ST['tembus'].strip().lower():
        return M.otp_konsol(surel)
    return otp_dari_box(surel)


# ------------------------------------------------------------------ util
def surel_celana_anyar():
    local = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"{local}@{ST['domain']}"


def tanya_email_tembus():
    while True:
        e = M.tanya('email TEMBUS (yang kamu jamin tembus verif CC + umur)').strip()
        if '@' in e and '.' in e:
            return e
        log('   email nggak valid — ketik ulang')


def tanya_jumlah():
    while True:
        a = M.tanya('jumlah reff mau diapain (1-7, Enter = 1)', meunang_kosong=True).strip()
        if not a:
            return 1
        try:
            n = int(a)
            if 1 <= n <= 7:
                return n
        except ValueError:
            pass
        log('   isi angka 1-7')


def tanya_domain():
    pilih = (M.tanya(
        'domain unbind (1 = celana-ar-store.my.id, 2 = dini-faqih.my.id, Enter = 1)',
        meunang_kosong=True).strip() or '1')
    return 'dini-faqih.my.id' if pilih == '2' else 'celana-ar-store.my.id'


def tanya_reff():
    return (M.tanya('kode reff (Enter = FO3DHT)', meunang_kosong=True).strip() or 'FO3DHT').upper()


def tanya_dob():
    return (M.tanya('tanggal lahir (Enter = 2000-12-12)', meunang_kosong=True).strip() or '2000-12-12')


# ------------------------------------------------------------------ setup
def setup_proxy():
    p = M.tanya('paste proxy (http://user:pass@host:port / socks5://...  Enter = lewatin)',
                meunang_kosong=True).strip()
    if not p:
        log('   tanpa proxy — jalan pakai IP sistem/VPN')
        ST['proxy'] = ''
        return
    try:
        proksi = M.baca_proksi(p)
    except ValueError as e:
        log(f'   {e}')
        ST['proxy'] = ''
        return
    log('   mengetes proxy & negaranya (10-20s, 3x coba)...')
    info = M.pariksa_geo_proksi(proksi)
    sae, vonis = M.vonis_us(info)
    if sae:
        log(f'   OK — {vonis}')
        ST['proxy'] = proksi
    else:
        log(f'   {vonis}')
        if M.pastikeun('tetap pakai proxy ini?'):
            ST['proxy'] = proksi
        else:
            ST['proxy'] = ''


def cek_ip():
    try:
        import curl_cffi
    except ImportError:
        log('   curl_cffi nggak ada — lewatin cek IP')
        return False
    proxies = {'http': ST['proxy'], 'https': ST['proxy']} if ST['proxy'] else None
    try:
        r = curl_cffi.requests.get(
            'http://ip-api.com/json/?fields=status,country,countryCode,query',
            proxies=proxies, timeout=15, impersonate='chrome')
        d = r.json()
        lewat = 'proxy' if proxies else 'IP sistem/VPN'
        if d.get('status') == 'success':
            kartu = (d.get('countryCode') or '').upper()
            tag = 'US — aman buat run' if kartu == 'US' else f'BUKAN US ({kartu}) — ganti negara VPN/proxy!'
            log(f'   {lewat}: {d.get("query")} -> {d.get("country")} ({kartu})  {tag}')
            return kartu == 'US'
        log(f'   ip-api menolak: {d}')
    except Exception as e:
        log(f'   {type(e).__name__}: {str(e)[:160]}')
    return False


# ------------------------------------------------------------------ auth
def login_atau_daftar(api, csrf, surel, dob):
    """Return (status, token, account_id) — status: login | register | 2fa"""
    try:
        katempo = {str(m.get('id')) for m in M.candak_kotak(surel)}
    except Exception:
        katempo = set()

    M.kirim_otp(api, csrf, surel)
    time.sleep(random.uniform(10, 30))
    otp = M.OTP_PANYADIA(surel)
    if not otp:
        M.gagal('otp', f'OTP nggak ada buat {surel}')

    data = M.pasti_otp(api, csrf, otp)
    sesi = data.get('auth_meta_session') or {}

    if sesi.get('frl_access_token'):
        log(f"   [login] email terdaftar -> LOGIN, frl_account_id={sesi.get('frl_account_id')}")
        return ('login', sesi['frl_access_token'], sesi.get('frl_account_id'))

    if data.get('registration_state') == 'completion_required':
        nh = random.choice(M.NGARAN_DEPAN)
        nt = random.choice(M.NGARAN_TUKANG)
        log(f'   [register] email baru -> DAFTAR ({nh} {nt}, {dob})')
        reg = M.rengsekeun_daptar(api, csrf, nh, nt, dob)
        sesi = reg.get('auth_meta_session') or {}
        if sesi.get('frl_access_token'):
            log(f"   [register] OK, frl_account_id={sesi.get('frl_account_id')}")
            return ('register', sesi['frl_access_token'], sesi.get('frl_account_id'))
        M.gagal('register', f'register-completion nggak balik token: {str(reg)[:200]}')

    if data.get('two_factor_required') or data.get('registration_state') == 'two_factor_required':
        tok, acct = M._asup_dua_faktor(api, csrf, surel, data)
        return ('2fa', tok, acct)

    M.gagal('auth', f'respons confirm-otp tak dikenal: {str(data)[:160]}')


# ------------------------------------------------------------------ unbind
def unbind_bind(api, surel_lama, surel_baru):
    sesi, tokens = M._ac_pastikeun_sesi(api, False)
    daptar_cp, _ = M._ac_daptar_coba(sesi, tokens)
    daptar_surel = M._ac_saring_surel(daptar_cp)
    if not daptar_surel:
        M.gagal('ac-list', 'tidak ada email terdaftar di akun ini')

    heubeul = next((c for c in daptar_surel
                    if (c.get('email') or '').lower() == surel_lama.lower()), None)
    if heubeul is None:
        log(f"   ℹ  {surel_lama} nggak ketemu di contact point — lanjut tambah email baru aja")

    id_alat = M._ac_acak(20, 'abcdefghijklmnopqrstuvwxyz_')
    sae, pesen, normal = M._ac_nambah(sesi, tokens, id_alat, surel_baru)
    if not sae:
        M.gagal('ac-add', f'gagal tambah email baru: {pesen or "unknown"}')
    tujuan = normal or surel_baru
    log(f'   📩 OTP dikirim ke {tujuan}')

    parantos = False
    for i in range(3):
        pin = M.OTP_PANYADIA(tujuan)
        if pin:
            sae, pesen = M._ac_verifikasi(sesi, tokens, id_alat, tujuan, pin)
            if sae:
                parantos = True
                break
            log(f"   ❌ OTP salah/kadaluarsa: {pesen or 'coba lagi'}")
        # fallback: kadang OTP dikirim ke email lama (tembus)
        if not parantos and surel_lama.strip().lower() != tujuan.strip().lower():
            pin2 = M.otp_konsol(surel_lama)
            if pin2:
                sae, pesen = M._ac_verifikasi(sesi, tokens, id_alat, tujuan, pin2)
                if sae:
                    parantos = True
                    break
                log(f"   ❌ OTP (dari email lama) salah: {pesen or 'coba lagi'}")
    if not parantos:
        M.gagal('ac-verify', 'verifikasi email baru gagal — email lama masih nempel')

    if heubeul:
        sae, pesen = M._ac_pupus(sesi, tokens, id_alat, heubeul['id'])
        if not sae:
            M.gagal('ac-delete', f'unbind email lama gagal: {pesen or "unknown"}')
        log(f"   ✅ email lama {heubeul.get('email')} di-unbind")
    return True


def logout(api):
    try:
        api.cookies.clear()
    except Exception:
        pass
    log('   [logout] sesi dibuang')


# ------------------------------------------------------------------ hasil
def simpen_hasil(hasil):
    try:
        with open(OUT_HASIL, 'w', encoding='utf-8') as f:
            json.dump(hasil, f, indent=1)
    except Exception:
        pass


def ringkasan(hasil):
    log('\n' + '=' * 62)
    log('RINGKASAN')
    log('=' * 62)
    for h in hasil:
        log(f"  reff #{h.get('i')}: {h.get('status')}"
            + (f"  -> {h.get('email')}" if h.get('email') else ''))
    log('=' * 62)


# ------------------------------------------------------------------ utama
def utama():
    log('=' * 62)
    log('  muKE v2 — DAFTAR TEMBUS + REFF + REBIND CELANA')
    log('=' * 62)

    # S1a — proxy
    setup_proxy()
    # S1b — cek IP (gaya menu 8)
    cek_ip()
    # S2 — email tembus
    ST['tembus'] = tanya_email_tembus()
    # S3 — jumlah reff
    ST['jumlah'] = tanya_jumlah()
    # S4 — reff
    ST['reff'] = tanya_reff()
    # S5 — DOB
    ST['dob'] = tanya_dob()
    # S6 — domain unbind
    ST['domain'] = tanya_domain()
    ST['box'] = f"https://box.{ST['domain']}"
    ST['_box'], cat_box = box_url_aktif()
    log(f'   box: {ST["_box"] or "(nggak ada)"} — {cat_box}')
    if not ST['_box']:
        log('   ⚠  tanpa box, OTP email unbind bakal diminta MANUAL')

    log(f"""
  ── SETUP ──────────────────────────────────────────
  email tembus : {ST['tembus']}
  jumlah reff  : {ST['jumlah']}
  kode reff    : {ST['reff']}
  tanggal lahir: {ST['dob']}
  domain unbind: {ST['domain']}
  proxy        : {M.samarkeun_proksi(ST['proxy']) if ST['proxy'] else '(kosong — IP sistem/VPN)'}
  ────────────────────────────────────────────────────""")

    # pasang config global muke
    M.KONF['use_hb'] = False
    M.KONF['proxy_enabled'] = bool(ST['proxy'])
    M.KONF['proxy'] = ST['proxy']
    M.KONF['ref_code'] = ST['reff']
    M.KONF['date_of_birth'] = ST['dob']
    M.KONF['random_profile'] = False
    M.KONF['email'] = ST['tembus']
    M.PROKSI = M.candak_proksi(M.KONF)
    M.OTP_PANYADIA = otp_provider

    hasil = []

    # ---------- [1][2][3] LOGIN sekali -> unbind -> logout ----------
    log('\n── [1] LOGIN sekali pakai email tembus ──')
    try:
        api, csrf = M.mimitian_alur()
        status, token, acct = login_atau_daftar(api, csrf, ST['tembus'], ST['dob'])
        log(f'   status = {status}  frl_account_id = {acct}')

        if status in ('login', 'register', '2fa'):
            M.jieun_sesi(api, token)
            celana = surel_celana_anyar()
            log(f'\n── [2] UNBIND {ST["tembus"]} -> {celana} ──')
            unbind_bind(api, ST['tembus'], celana)
            log('\n── [3] LOGOUT ──')
            logout(api)
        else:
            log('   status tak dikenal — skip unbind, lanjut loop')
            logout(api)
    except SystemExit as e:
        log(f'   [login] berhenti: {e}')

    # ---------- [4] LOOP ----------
    for i in range(1, ST['jumlah'] + 1):
        log('\n' + '=' * 62)
        log(f'  REFF {i}/{ST["jumlah"]}')
        log('=' * 62)
        try:
            api, csrf = M.mimitian_alur()
            status, token, acct = login_atau_daftar(api, csrf, ST['tembus'], ST['dob'])

            if status != 'register':
                log(f'   email tembus masih terdaftar (status={status}) — skip reff ini')
                hasil.append({'i': i, 'status': f'skip_{status}'})
                logout(api)
                simpen_hasil(hasil)
                continue

            M.jieun_sesi(api, token)

            # cek verif CC / umur dulu
            _, ccv = M.intip_status_ccv(api)
            if ccv in ('not_required', None):
                try:
                    out = M.tebus_kode(api, ST['reff'])
                    log(f"   redeem: {out}")
                    hasil.append({'i': i, 'status': 'redeemed', 'out': out})
                except SystemExit as e:
                    log(f'   redeem berhenti: {e}')
                    hasil.append({'i': i, 'status': f'redeem_error'})
            else:
                log(f'   ccv_status={ccv!r} — SKIP redeem (kena verif CC/umur)')
                hasil.append({'i': i, 'status': f'skip_ccv_{ccv}'})

            # unbind -> bind celana
            celana = surel_celana_anyar()
            log(f'   UNBIND {ST["tembus"]} -> {celana}')
            unbind_bind(api, ST['tembus'], celana)
            logout(api)

        except SystemExit as e:
            log(f'   reff #{i} berhenti: {e}')
            hasil.append({'i': i, 'status': f'error_{e}'})
        except Exception as e:
            log(f'   reff #{i} error: {type(e).__name__}: {e}')
            hasil.append({'i': i, 'status': f'error_{type(e).__name__}'})

        simpen_hasil(hasil)

    ringkasan(hasil)
    log(f'hasil tersimpan di: {OUT_HASIL}')


if __name__ == '__main__':
    try:
        utama()
    except KeyboardInterrupt:
        log('\n[dibatalkan user]')
        sys.exit(130)
    except EOFError:
        log('\n[stdin tertutup — berhenti]')
        sys.exit(130)
