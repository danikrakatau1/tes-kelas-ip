
import requests as preq
HB_API_KEY = "hb_cdfc571755daac8231b0c1812ec4"

def make_hb_session():
    headers = {"x-api-key": HB_API_KEY, "Content-Type": "application/json"}
    try:
        res = preq.post("https://api.hyperbrowser.ai/api/session", headers=headers, json={}, timeout=30)
        if res.status_code == 200:
            data = res.json()
            print(f"[HB] Sesi Hyperbrowser US Aktif! ID: {data.get('id')}")
            return data.get("id")
    except Exception as e:
        print(f"[HB] Gagal buat sesi: {e}")
    return None

def stop_hb_session(session_id):
    if not session_id:
        return
    headers = {"x-api-key": HB_API_KEY, "Content-Type": "application/json"}
    try:
        preq.put(f"https://api.hyperbrowser.ai/api/session/{session_id}/stop", headers=headers, timeout=30)
        print("[HB] Sesi Hyperbrowser dihentikan.")
    except Exception:
        pass

import base64
import hashlib
import json
import os
import random
import re
import string
import sys
import time
import uuid
from curl_cffi import requests as cr
JALUR_KONFIG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
KONFIG_BAKU = {'mode': 'signup_redeem', 'ref_code': '', 'email': '', 'first_name': 'Miauru', 'last_name': 'Juanda', 'date_of_birth': '1998-11-12', 'random_profile': True, 'use_hb': False, 'proxy_enabled': False, 'proxy': '', 'vcc': {'number': '', 'expiry': '', 'cvv': '', 'zip': '', 'country': 'US'}, 'product_id': '766358168544755', 'receiver_id': '352501280694489'}

def maca_konfig():
    if not os.path.exists(JALUR_KONFIG):
        with open(JALUR_KONFIG, 'w') as f:
            json.dump(KONFIG_BAKU, f, indent=2)
        print(f'[config] {JALUR_KONFIG} dibuat, isi dulu lalu jalankan lagi.', flush=True)
        sys.exit(1)
    with open(JALUR_KONFIG) as f:
        konf = json.load(f)
    ngahiji = dict(KONFIG_BAKU)
    ngahiji.update(konf)
    if isinstance(konf.get('vcc'), dict):
        ngahiji['vcc'] = dict(KONFIG_BAKU['vcc'])
        ngahiji['vcc'].update(konf['vcc'])
    return ngahiji

def candak_proksi(konf):
    if konf.get('proxy_enabled') and konf.get('proxy'):
        return {'http': konf['proxy'], 'https': konf['proxy']}
    return {}
KONF = dict(KONFIG_BAKU)
PROKSI = candak_proksi(KONF)
API_JESTCO = 'https://jestco.id/api.php'
DASAR_MUSE = 'https://muse.ai'
WEWENGKON = 'US'
BATAS_ANTOS_OTP = 150
SELANG_ANTOS_OTP = 5
VERSI_TOS = 'ntm_create_account:default_v1_meta_account_v2+docs_v1'
ID_APP_PTT = '2220391788200892'                                                                    
NAGARA_DIDUKUNG = ['US', 'CA', 'GB', 'DZ', 'AR', 'AU', 'AT', 'BE', 'BR', 'CL', 'CO', 'CI', 'HR', 'CZ', 'DK', 'EG', 'FI', 'FR', 'DE', 'GH', 'HK', 'IS', 'IN', 'ID', 'IE', 'IL', 'IT', 'JP', 'KE', 'LB', 'MY', 'MX', 'MA', 'NL', 'NZ', 'NG', 'NO', 'PK', 'PH', 'PL', 'PT', 'QA', 'RO', 'SA', 'SN', 'SG', 'ZA', 'KR', 'ES', 'SE', 'CH', 'TW', 'TH', 'TR', 'AE', 'VN', 'ZM', 'ZW']
ALIAS_NAGARA = {'USA': 'US', 'UK': 'GB', 'ENGLAND': 'GB', 'AUS': 'AU', 'UAE': 'AE', 'KOREA': 'KR', 'SOUTH KOREA': 'KR'}
NGARAN_DEPAN = ['Miauru', 'Anya', 'Sinta', 'Putri', 'Dian', 'Nadia', 'Fitri', 'Intan', 'Rani', 'Wulan', 'Lestari', 'Ayu', 'Bima', 'Rizky', 'Fajar', 'Dimas', 'Agus', 'Budi', 'Andi', 'Yoga', 'Reza', 'Ilham', 'Fahmi', 'Galih', 'Bagas', 'Teguh', 'Hendri', 'Nabila', 'Kirana', 'Zahra', 'Amelia', 'Dinda', 'Salsa', 'Ratna', 'Melati', 'Anggun']
NGARAN_TUKANG = ['Juanda', 'Pratama', 'Nugroho', 'Saputra', 'Kusuma', 'Wijaya', 'Santoso', 'Hidayat', 'Ramadhan', 'Firmansyah', 'Setiawan', 'Gunawan', 'Hakim', 'Maulana', 'Syahputra', 'Rahmawati', 'Anggraini', 'Maharani', 'Laksmana', 'Puspita', 'Kartika', 'Handayani', 'Septiani', 'Utami']
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36'

                                  
                                                                      
                                                                                 
                                                                   
PROFIL_CHROME = [
    ("146.0.0.0", "chrome146"),
    ("145.0.0.0", "chrome145"),
    ("142.0.0.0", "chrome142"),
    ("131.0.0.0", "chrome131"),
    ("124.0.0.0", "chrome124"),
]
UA_JALAN = UA                                                           
TIRU_JALAN = 'chrome'

def pilih_profil_browser(binih):
    
    h = hashlib.sha256(str(binih).encode()).digest()
    ver, tiruan = PROFIL_CHROME[int.from_bytes(h[:2], 'big') % len(PROFIL_CHROME)]
    ua = (f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
          f'(KHTML, like Gecko) Chrome/{ver} Safari/537.36')
    return ua, tiruan

def bereskeun_profil_browser():
    
    global UA_JALAN, TIRU_JALAN
    binih = (KONF.get('email') or '').strip() or uuid.uuid4().hex
    UA_JALAN, TIRU_JALAN = pilih_profil_browser(binih)
    catet('profile', f'browser: {TIRU_JALAN} (UA Chrome/{UA_JALAN.split("Chrome/")[1].split(" ")[0]})')

def catet(lengkah, pesen):
    print(f'[{lengkah}] {pesen}', flush=True)

def gagal(lengkah, pesen):
    print(f'[{lengkah}] GAGAL: {pesen}', flush=True)
    sys.exit(1)


JELASKEUN_TOLAK = {
                                                                   
    '2078019': 'Bank menolak otorisasi kartu ini',
    '2078136': 'Prosesor/bank menolak kartu ini (keluarga decline 2078xxx)',
}


class KartuDitolak(Exception):
    def __init__(self, mana, pesen, kode):
        super().__init__(f'kartu ditolak [{mana}] code={kode}: {pesen}')
        self.where = mana
        self.msg = pesen
        self.code = kode


def gagal_tolak(mana, pesen, kode):
    


    kode = str(kode or '')
    jelaskeun = JELASKEUN_TOLAK.get(kode, '')
    mistar = '=' * 62
    print(warna(f'\n{mistar}', 'r'), flush=True)
    print(warna(f'  ❌  KARTU DITOLAK  [{mana}]', 'r'), flush=True)
    print(warna(f'  Alasan : {pesen or "-"}', 'w'))
    print(warna(f'  Code   : {kode or "-"}', 'w'))
    if jelaskeun:
        print(warna(f'  Artinya : {jelaskeun}', 'w'))
    print(warna(f'  → Kartu ini tidak bisa dipakai. Ganti kartu lain.', 'y'))
    print(warna(f'  → Ini keputusan bank/prosesor, BUKAN error script.', 'y'))
    print(warna(f'{mistar}\n', 'r'), flush=True)
    raise KartuDitolak(mana, pesen, kode)

def kode64(data: bytes) -> str:
    
    return base64.urlsafe_b64encode(data).decode().rstrip('=')

def buka_kode64(s: str) -> bytes:
    return base64.urlsafe_b64decode(s + '=' * (-len(s) % 4))

def json_padet(objek) -> str:
    
    return json.dumps(objek, separators=(',', ':'))

def profil_acak():
    dinten_ieu = time.localtime()
    min_y, max_y = (dinten_ieu.tm_year - 40, dinten_ieu.tm_year - 18)
    tanggal_lahir = f'{random.randint(min_y, max_y):04d}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}'
    return (random.choice(NGARAN_DEPAN), random.choice(NGARAN_TUKANG), tanggal_lahir)

def _u32_gede(n: int) -> bytes:
    return n.to_bytes(4, 'big')

def jieun_token_ptt(rantai_kapercayaan_b64: str, data: dict, beban_rusiah: dict | None) -> str:
    





    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, load_der_public_key
    jero = {'data': data, 'nonce': str(uuid.uuid4()), 'op': data.pop('_op'), 'ver': 1}
    jero_b64 = kode64(json_padet(jero).encode())
    if beban_rusiah is None:
        beban = jero_b64
        return kode64(json_padet({'payload': beban, 'signatures': []}).encode())
    der_sertipikat = base64.b64decode(rantai_kapercayaan_b64)
    try:
        from cryptography import x509
        sertipikat = x509.load_der_x509_certificate(der_sertipikat)
        der_spki = sertipikat.public_key().public_bytes(Encoding.DER, PublicFormat.SubjectPublicKeyInfo)
    except Exception:
        der_spki = der_sertipikat
    pub_server = load_der_public_key(der_spki)
    if not isinstance(pub_server, ec.EllipticCurvePublicKey):
        gagal('ptt', 'kunci server bukan EC')
    priv_sakedap = ec.generate_private_key(ec.SECP256R1())
    pub_sakedap = priv_sakedap.public_key()
    spki_sakedap = pub_sakedap.public_bytes(Encoding.DER, PublicFormat.SubjectPublicKeyInfo)
    Z = priv_sakedap.exchange(ec.ECDH(), pub_server)
    sidik_jari = 'fp:' + kode64(hashlib.sha256(spki_sakedap).digest())
    asupan_kdf = b''.join([_u32_gede(1), Z, _u32_gede(len('A256GCM')), b'A256GCM', _u32_gede(0), b'', _u32_gede(len(sidik_jari)), sidik_jari.encode(), _u32_gede(256)])
    konci_aes = hashlib.sha256(asupan_kdf).digest()
    pem_b64 = base64.b64encode(spki_sakedap).decode()
    pem = '-----BEGIN PUBLIC KEY-----\n'
    for i in range(0, len(pem_b64), 64):
        pem += pem_b64[i:i + 64] + '\n'
    pem += '-----END PUBLIC KEY-----\n'
    ditangtayungan = {'alg': 'ECDH-ES', 'apu': '', 'apv': kode64(sidik_jari.encode()), 'enc': 'A256GCM', 'epk': {'crv': 'P-256', 'kty': 'EC', 'pem': pem}}
    lindung_b64 = kode64(json_padet(ditangtayungan).encode())
    aad = (lindung_b64 + '.' + jero_b64).encode()
    iv = os.urandom(12)
    ct_tag = AESGCM(konci_aes).encrypt(iv, json_padet(beban_rusiah).encode(), aad)
    ct, tag = (ct_tag[:-16], ct_tag[-16:])
    beban = f'{jero_b64}.{lindung_b64}..{kode64(iv)}.{kode64(ct)}.{kode64(tag)}'
    return kode64(json_padet({'payload': beban, 'signatures': []}).encode())

def token_kartu_ptt(rantai_kapercayaan_b64, nomer_kartu, cvv, bulan_kadal, taun_kadal):
    
    data = {'app_id': ID_APP_PTT, 'auth_ticket_type': 'PAN', 'cardholder_name': '', 'credit_card': '$e2ee', 'csc': '$e2ee', 'device_id': 'DEVICE_ID', 'expiry_month': bulan_kadal, 'expiry_year': taun_kadal, '_op': 'ADD_CARD'}
    rusiah = {'csc': cvv, 'credit_card': nomer_kartu}
    return jieun_token_ptt(rantai_kapercayaan_b64, data, rusiah)

def token_wadah_ptt(id_pesenan, receiver_id, mode_wadah, jumlah, duit, id_kredensial, bulan_kadal, taun_kadal):
    

    sen_jumlah = int(round(float(jumlah) * 100))
    data = {'components': [{'amount': sen_jumlah, 'cred_id': str(id_kredensial), 'currency': duit}],
            'container_mode': mode_wadah, 'context_id': str(id_pesenan),
            'credential_id': str(id_kredensial), 'expiry_month': bulan_kadal, 'expiry_year': taun_kadal,
            'receiver_id': str(receiver_id), 'security_origin': '', '_op': 'CREATE_CONTAINER'}
    return jieun_token_ptt('', data, None)

def sesi_api_anyar():
    s = cr.Session(impersonate=TIRU_JALAN, proxies=PROKSI)
    s.headers.update({'User-Agent': UA_JALAN, 'Accept': '*/*', 'Accept-Language': 'en-US,en;q=0.9', 'Origin': DASAR_MUSE, 'Referer': DASAR_MUSE + '/', 'x-hatch-caa-reg-entry-point': 'login_home', 'x-hatch-waterfall-id': str(uuid.uuid4()), 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty'})
    return s

def lacak_sentry():
    return f'{uuid.uuid4().hex}{uuid.uuid4().hex[:16]}-{uuid.uuid4().hex[:16]}-0'

def post_api(sesi, path, beban, csrf=None, cobaan=3, timeout=30):
    headers = {'sentry-trace': lacak_sentry(), 'Content-Type': 'application/json'}
    if csrf:
        headers['x-hatch-csrf-token'] = csrf
    ngarakan = None
    for a in range(cobaan):
        try:
            r = sesi.post(DASAR_MUSE + path, json=beban, headers=headers, timeout=timeout)
            if r.status_code in (200, 201):
                return r
            if r.status_code == 429:
                catet('ratelimit', f'{path} -> HTTP 429 ({r.text[:120]})')
                print(warna(f'  ⏳ 429 — tunggu {60 * (a + 1)}s lalu retry ({a + 1}/{cobaan})', 'y'), flush=True)
                time.sleep(60 * (a + 1))
                continue
            ngarakan = f'HTTP {r.status_code}: {r.text[:160]}'
        except Exception as e:
            ngarakan = f'{type(e).__name__}: {e}'
        time.sleep(2 * (a + 1))
    gagal('http', f'POST {path} gagal {cobaan}x: {ngarakan}')
def pamundut_app(sesi, metode, path, beban=None, perujuk=DASAR_MUSE + '/', cobaan=3, timeout=30, fatal=True):
    


    headers = {'Accept': '*/*', 'Referer': perujuk, 'Origin': DASAR_MUSE, 'Content-Type': 'application/json'}
    ngaran_tukang = None
    for a in range(cobaan):
        try:
            if metode == 'POST':
                r = sesi.post(DASAR_MUSE + path, json=beban, headers=headers, timeout=timeout)
            else:
                r = sesi.get(DASAR_MUSE + path, headers=headers, timeout=timeout)
            if r.status_code == 200:
                return r
            ngaran_tukang = f'HTTP {r.status_code}: {r.text[:160]}'
        except Exception as e:
            ngaran_tukang = f'{type(e).__name__}: {e}'
        time.sleep(2 * (a + 1))
    if not fatal:
        catet('http', f'{metode} {path} -> {ngaran_tukang} (non-fatal)')
        return None
    gagal('http', f'{metode} {path} gagal {cobaan}x: {ngaran_tukang}')

def post_app(sesi, path, beban, perujuk=DASAR_MUSE + '/'):
    return pamundut_app(sesi, 'POST', path, beban, perujuk)

def candak_app(sesi, path, perujuk=DASAR_MUSE + '/'):
    return pamundut_app(sesi, 'GET', path, None, perujuk)

def mimitian_alur():
    hb_id = make_hb_session() if KONF.get("use_hb") else None
    bereskeun_profil_browser()
    api = sesi_api_anyar()
    proksi_samaran = samarkeun_proksi(KONF.get('proxy') or '')
    cobaan = 3
    for i in range(cobaan):
        try:
            r = api.get(DASAR_MUSE + '/', timeout=25)
                                                                     
            catet('net', f'landing OK (HTTP {r.status_code})')
            break
        except Exception as e:
            catet('net', f'landing GET {i + 1}/{cobaan} gagal via {proksi_samaran or "IP langsung"} ({e})')
            time.sleep(5 * (i + 1))
    else:
        catet('net', warna('landing page NGGAK WAJIB — lanjut tanpa GET / (restart tetap jalan)', 'y'))
    r = post_api(api, '/api/auth/native/restart', {})
    try:
        csrf = r.json()['csrf_token']
    except (KeyError, ValueError):
        gagal('restart', f'no csrf_token: {r.text[:200]}')
    catet('restart', 'flow dimulai')
    return (api, csrf)

def kirim_otp(api, csrf, surel):
    r = post_api(api, '/api/auth/native/send-otp', {'contact_point': surel, 'region': WEWENGKON}, csrf=csrf)
    catet('send-otp', f'OTP dikirim ke {surel}')

def pasti_otp(api, csrf, otp):
    r = post_api(api, '/api/auth/native/confirm-otp', {'otp_code': otp}, csrf=csrf)
    return r.json()

def rengsekeun_daptar(api, csrf, ngaran_hareup, ngaran_tukang, tanggal_lahir):
    r = post_api(api, '/api/auth/native/register-completion', {'date_of_birth': tanggal_lahir, 'first_name': ngaran_hareup, 'last_name': ngaran_tukang, 'tos_content_version': VERSI_TOS}, csrf=csrf)
    return r.json()

def simpen_akun(api):
    r = post_api(api, '/api/auth/save-account', {})
    catet('save-account', f"saved={r.json().get('saved')}")

def jieun_sesi(api, token_akses_frl):
    



    catet('bootstrap', 'menukar token jadi sesi ...')
    lulugu_navigasi = {'Content-Type': 'application/x-www-form-urlencoded', 'Referer': DASAR_MUSE + '/', 'Origin': DASAR_MUSE, 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.9', 'Upgrade-Insecure-Requests': '1', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Sec-Fetch-User': '?1'}
    r = api.post('https://auth.meta.com/hatch/session/bootstrap/', data={'frl_access_token': token_akses_frl}, headers=lulugu_navigasi, allow_redirects=False, timeout=30)
    for _ in range(5):
        lokasi = r.headers.get('location')
        if r.status_code not in (301, 302, 303, 307, 308) or not lokasi:
            break
        r = api.get(lokasi, headers={'Referer': DASAR_MUSE + '/'}, allow_redirects=False, timeout=30)
    catet('bootstrap', f'sesi aktif (akhir: {r.url[:60]})')

def _sesi_surel():
    s = cr.Session(impersonate='chrome', proxies=PROKSI)
    s.headers.update({'User-Agent': UA})
    return s

def candak_domain_surel(cobaan=3):
    s = _sesi_surel()
    ngaran_tukang = None
    for a in range(cobaan):
        try:
            r = s.get(API_JESTCO, params={'action': 'get_public_config'}, timeout=30)
            data = r.json()
            daptar_domain = data.get('temp_email_domains') or data.get('domains') or []
            if daptar_domain:
                catet('email', f'{len(daptar_domain)} domain temp tersedia')
                return daptar_domain
            ngaran_tukang = r.text[:120]
        except Exception as e:
            ngaran_tukang = f'{type(e).__name__}: {e}'
        time.sleep(2 * (a + 1))
    gagal('email', f'get_public_config gagal {cobaan}x: {ngaran_tukang}')



class TempMail:
    def __init__(self):
        self.base_url = "https://box.celana-ar-store.my.id"
        self.email = None
        self.domain = "celana-ar-store.my.id"

    def generate_email(self):
        import random, string
        local = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        self.email = f"{local}@{self.domain}"
        print(f"[email] Temp Email Custom Dibuat: {self.email}")
        return self.email

    def wait_for_otp(self, timeout=150, interval=5):
        print(f"[otp] Menunggu email masuk ke {self.email} (Maks {timeout} detik)...")
        start_time = time.time()
        seen_ids = set()
        while time.time() - start_time < timeout:
            try:
                res = preq.get(f"{self.base_url}/api/inbox", params={"address": self.email}, timeout=10)
                if res.status_code == 200:
                    emails = res.json().get("emails", [])
                    for mail in emails:
                        msg_id = mail.get("id")
                        if msg_id not in seen_ids:
                            seen_ids.add(msg_id)
                            m_res = preq.get(f"{self.base_url}/api/read", params={"address": self.email, "id": msg_id}, timeout=10)
                            if m_res.status_code == 200:
                                data = m_res.json()
                                body = data.get("body", "")
                                subject = data.get("subject", "")
                                combined = f"{subject} {body}"
                                otp_match = re.search(r'\b(\d{6})\b', combined)
                                if otp_match:
                                    otp = otp_match.group(1)
                                    print(f"[otp] Kode OTP Diterima: {otp}")
                                    return otp
            except Exception as e:
                pass
            time.sleep(interval)
        return None
def surel_sakedap_anyar():
    global _GLOBAL_MAIL_OBJ
    _GLOBAL_MAIL_OBJ = TempMail()
    surel = _GLOBAL_MAIL_OBJ.generate_email()
    if not surel:
        print("[-] Gagal generate email")
        sys.exit(1)
    return surel

def antos_otp(surel, timeout=150, id_diabaikan=frozenset()):
    global _GLOBAL_MAIL_OBJ
    if not _GLOBAL_MAIL_OBJ:
        print("[-] TempMail belum diinisialisasi")
        sys.exit(1)
    otp = _GLOBAL_MAIL_OBJ.wait_for_otp(timeout=timeout, interval=5)
    if not otp:
        print("[-] OTP tidak datang")
        sys.exit(1)
    return otp

def candak_kotak(surel):
    return []

def cokot_otp(daptar_pesen):
    return None

def merek_kartu(nomer):
    
    if nomer.startswith('4'):
        return 'VISA'
    if re.match('^(5[1-5]|2(22[1-9]|2[3-9][0-9]|3[0-9]{2}|7([01][0-9]|20)))', nomer):
        return 'MASTERCARD'
    if nomer.startswith(('34', '37')):
        return 'AMEX'
    if nomer.startswith('6011') or nomer.startswith('65'):
        return 'DISCOVER'
    return 'UNKNOWN'

def satuju_tos(api):
    awak = {'saw_meta_ai_tos': False, 'client_request_timestamp': str(int(time.time())), 'entry_point': 'web_onboarding_flow', 'nux_type': 'ROW', 'disclosure_version': 'HATCH_ROW_v0', 'disclosure_text': "By continuing, you agree to the Muse Terms and Meta's AI Terms, which include important information about your rights and responsibilities. Learn more about Muse's approach to privacy in the Muse Privacy Policy."}
    r = pamundut_app(api, 'POST', '/api/hatch/accept-tos', awak, perujuk=DASAR_MUSE + '/access/disclosure', fatal=False)
    if r is None:
        catet('tos', 'accept-tos 403: dilewati (akun gate / sudah diterima)')
    else:
        catet('tos', f'accept-tos: {r.json()}')

def tebus_kode(api, kode_reff):
    r = post_app(api, '/api/hatch/invite-code/redeem', {'code': kode_reff, 'supportsRedemptionStatus': True})
    data = r.json()
    catet('redeem', f"success={data.get('success')} redemption={data.get('redemptionStatus')} waitlist={data.get('waitlistStatus')}")
    return data

def mimitian_checkout(api, product_id, receiver_id):
    id_sesi = f'upl_{int(time.time() * 1000)}_{uuid.uuid4()}'
    awak = {'amount': '1.00', 'currency': 'USD', 'sessionId': id_sesi, 'productId': product_id, 'receiverId': receiver_id, 'productData': []}
    r = post_app(api, '/api/checkout/init', awak, perujuk=DASAR_MUSE + '/access/verification')
    data = r.json()
    catet('vcc-init', f"orderId={data.get('orderId')} receiver={data.get('receiverName')}")
    return (id_sesi, data)

def candak_konci_enkripsi(api, id_sesi_upl, product_id):
    awak = {'deviceId': 'device_id', 'paymentType': 'ECP', 'uplSessionId': id_sesi_upl, 'productId': product_id, 'otcSessionId': str(uuid.uuid4()), 'otcType': 'card'}
    r = post_app(api, '/api/ptt/encryption-key', awak, perujuk=DASAR_MUSE + '/access/verification')
    data = r.json()
    if not data.get('trustChain'):
        gagal('vcc-key', f'trustChain kosong: {r.text[:200]}')
    catet('vcc-key', f"key id={data.get('id')} devExternal={data.get('devExternal')}")
    return (awak['otcSessionId'], data)

TANDA_TOLAK = ('declined', 'do not honor', 'insufficient funds',
                   '2078019', 'card declined')


def _tolak_kena(teks):
    t = (teks or '').lower()
    return any(m in t for m in TANDA_TOLAK)


STATUS_BERES = ('SUCCESS', 'SUCCEEDED', 'COMPLETED')

def vonis_vcc(pamungkas):
    



    if not isinstance(pamungkas, dict):
        return ('UNKNOWN', f'respons bukan dict: {str(pamungkas)[:120]}')
                                                                     
                                                                                      
    status = pamungkas.get('checkoutStatus')
    eror = pamungkas.get('error')
    pesenan = pamungkas.get('orderId')
    if status is None:
        ecp = ((pamungkas.get('data') or {}).get('ecp_finalize_checkout') or {})
        status = ecp.get('checkout_status')
        pesenan = pesenan or ecp.get('order_id')
        if eror is None:
            eror = ecp.get('error')
    rincian = f'status={status} order={pesenan}'
    err_s = json.dumps(eror) if eror else ''
    if _tolak_kena(err_s):
        return ('DECLINED', f'{rincian} error={err_s[:200]}')
    if isinstance(status, str) and status.upper() in STATUS_BERES and not eror:
        return ('SUCCESS', rincian)
    if eror:
        return ('UNKNOWN', f'{rincian} error={err_s[:200]}')
    return ('UNKNOWN', rincian)


def jieun_kredensial(api, id_sesi_upl, id_sesi_otc, data_awal, product_id, receiver_id, token_ptt, vcc, nomer, kadal):
    nomer = re.sub('\\D', '', nomer)
                                                                     
                                                                            
    awak = {'operation': 'CREATE', 'uplSessionId': id_sesi_upl, 'ecpCheckoutSessionId': None, 'orderId': data_awal['orderId'], 'amount': '1.00', 'currencyCode': 'USD', 'paymentContainerMode': data_awal.get('paymentContainerMode', 'LIVE'), 'productId': product_id, 'receiverId': receiver_id, 'platformTrustToken': token_ptt, 'cardFirst6': nomer[:6], 'cardLast4': nomer[-4:], 'expiryMonth': kadal[:2], 'expiryYear': '20' + kadal[2:4], 'city': '', 'state': '', 'street1': '', 'street2': '', 'zip': vcc.get('zip', ''), 'countryCode': vcc.get('country', 'US'), 'cardholderName': '', 'cardholderEmail': '', 'cardholderPhone': '', 'otcSessionId': id_sesi_otc, 'otcType': 'card'}
    r = post_app(api, '/api/checkout/credential', awak, perujuk=DASAR_MUSE + '/access/verification')
    data = r.json()
    _jaga_sakedap(data, 'checkout/credential')
    mutasi = data.get('mutation') or {}
    if not mutasi.get('success'):
        eror = mutasi.get('error') or {}
        pesen = f"{eror.get('title')}: {eror.get('description')}"
                                                                        
                                                                   
        if _tolak_kena(pesen) or _tolak_kena(str(eror.get('error_code') or '')):
            gagal('vcc-cred', f'kartu DITOLAK bank ({eror.get("title")}). '
                             'Ganti kartu lain — retry kartu yg sama percuma.')
        gagal('vcc-cred', pesen)
    id_kredensial = mutasi.get('credentialId')
    catet('vcc-cred', f'credentialId={id_kredensial}')
    return id_kredensial

def pamungkas_checkout(api, id_sesi_upl, id_sesi_otc, data_awal, product_id, receiver_id, id_kredensial2, kadal):
    wadah_ptt = token_wadah_ptt(data_awal['orderId'], receiver_id, data_awal.get('paymentContainerMode', 'LIVE'), '1.00', 'USD', id_kredensial2, kadal[:2], '20' + kadal[2:4])
                                                                           
                                                                          
    awak = {'uplSessionId': id_sesi_upl, 'ecpCheckoutSessionId': None, 'orderId': data_awal.get('orderId', ''), 'selectedCredentialId': id_kredensial2, 'credentialType': 'CREDIT_CARD', 'countryCode': 'US', 'amount': '1.00', 'currencyCode': 'USD', 'payButtonClickId': str(uuid.uuid4()), 'paymentRequestId': str(uuid.uuid4()), 'platformTrustToken': wadah_ptt, 'paymentContainerMode': data_awal.get('paymentContainerMode', 'LIVE'), 'otcSessionId': id_sesi_otc, 'otcType': 'card', 'productId': product_id, 'receiverId': receiver_id}
    r = post_app(api, '/api/checkout/finalize', awak, perujuk=DASAR_MUSE + '/access/verification')
    data = r.json()
    _jaga_sakedap(data, 'checkout/finalize')
    vonis, rincian = vonis_vcc(data)
    if vonis == 'SUCCESS':
        catet('vcc-final', f"✅ BERHASIL — {rincian}")
    elif vonis == 'DECLINED':
        gagal('vcc-final', f'kartu DITOLAK bank saat finalize ({rincian}). '
                           'Ganti kartu lain — retry kartu yg sama percuma.')
    else:
        gagal('vcc-final', f'status tak dikenal ({rincian}) — cek manual di '
                           'https://muse.ai/access/verification')
    return data
OTP_PANYADIA = None
VCC_PANYADIA = None

def _asup_biasa(api, csrf, surel):
    



    try:
        katempo = {str(m.get('id')) for m in candak_kotak(surel)}
    except Exception:
        katempo = set()
    kirim_otp(api, csrf, surel)
    # 10-30s deliberate pause before confirming OTP (anti 429)
    time.sleep(random.uniform(10, 30))
    if OTP_PANYADIA is not None:
        otp = OTP_PANYADIA(surel)
    else:
        otp = antos_otp(surel, id_diabaikan=katempo)
    data = pasti_otp(api, csrf, otp)
    sesi = data.get('auth_meta_session') or {}
    if sesi.get('frl_access_token'):
        catet('login', f"email terdaftar -> login, frl_account_id={sesi.get('frl_account_id')}")
        return (sesi['frl_access_token'], sesi.get('frl_account_id'))
    if data.get('registration_state') == 'completion_required':
        catet('register', 'email baru -> daftar akun baru')
        ngaran_hareup = KONF['first_name']
        ngaran_tukang = KONF['last_name']
        tanggal_lahir = KONF['date_of_birth']
        if KONF.get('random_profile'):
            ngaran_hareup, ngaran_tukang, tanggal_lahir = profil_acak()
        catet('profil', f'{ngaran_hareup} {ngaran_tukang}, {tanggal_lahir}')
        pendaptaran = rengsekeun_daptar(api, csrf, ngaran_hareup, ngaran_tukang, tanggal_lahir)
        sesi = pendaptaran.get('auth_meta_session') or {}
        catet('register', f"frl_account_id={sesi.get('frl_account_id')}")
        return (sesi.get('frl_access_token'), sesi.get('frl_account_id'))
    if data.get('two_factor_required') or data.get('registration_state') == 'two_factor_required':
        return _asup_dua_faktor(api, csrf, surel, data)
    gagal('auth', f'respons confirm-otp tak dikenal: {str(data)[:160]}')

def _asup_dua_faktor(api, csrf, surel, data):
    


    metode2 = data.get('two_factor_methods') or []
    def _g(m, *ks):
        for k in ks:
            if m.get(k) is not None:
                return m.get(k)
        return None
    m = next((x for x in metode2 if str(_g(x, 'method_type', 'methodType') or '').upper() == 'SMS'), None)
    if m is None and metode2:
        m = metode2[0]
    if m is None:
        gagal('auth', '2FA: tidak ada metode verifikasi tersedia')
    tengah = _g(m, 'method_id', 'methodId')
    etiket = _g(m, 'label', 'method_type', 'methodType') or '?'
    catet('2fa', f'akun butuh 2FA — metode: {etiket}, kirim kode...')
    post_api(api, '/api/auth/native/two-factor-send-code', {'method_id': tengah}, csrf=csrf)
    if OTP_PANYADIA is not None:
        kode = OTP_PANYADIA(surel)
    else:
        kode = input('kode 2FA (SMS): ').strip()
    nilai2 = post_api(api, '/api/auth/native/two-factor',
                 {'method_id': tengah, 'code': kode}, csrf=csrf).json()
    sesi = nilai2.get('auth_meta_session') or {}
    if sesi.get('frl_access_token'):
        catet('2fa', f"login 2FA OK, frl_account_id={sesi.get('frl_account_id')}")
        return (sesi['frl_access_token'], sesi.get('frl_account_id'))
    gagal('auth', f'verifikasi 2FA gagal: {str(nilai2)[:160]}')
_DOMAIN_JESTCO = None

def _domain_jestco():
    global _DOMAIN_JESTCO
    if _DOMAIN_JESTCO is None:
        try:
            _DOMAIN_JESTCO = set(candak_domain_surel())
        except BaseException as e:
                                                                      
                                                           
            catet('email', f'daftar domain jestco tak terbaca ({type(e).__name__}) — fallback OTP manual')
            _DOMAIN_JESTCO = set()
    return _DOMAIN_JESTCO

def intip_status_ccv(api):
    







    try:
        r = api.get(DASAR_MUSE + '/api/hatch/ccv-status',
                    headers={'Accept': '*/*',
                             'Referer': DASAR_MUSE + '/access/verification',
                             'Origin': DASAR_MUSE},
                    timeout=30)
    except Exception as e:
        catet('gate', f'ccv-status probe gagal: {type(e).__name__}: {e}')
        return (None, None)
    if r.status_code != 200:
        catet('gate', f'ccv-status HTTP {r.status_code} (tak terbaca)')
        return (r.status_code, None)
    try:
        nilai = r.json().get('ccv_status')
    except Exception:
        nilai = None
    catet('gate', f"ccv_status={nilai!r}")
    return (200, nilai)


def _menta_kartu_ganti(panolakan):
    
    if VCC_PANYADIA is not None:
        nilai2 = VCC_PANYADIA() or {}
        return nilai2 if nilai2.get('number') else None
    if not sys.stdin.isatty():
        return None
    print(warna(f"\n💳 Kartu ditolak ({panolakan}/3). Masukkan kartu LAIN, "
              "atau 'stop' untuk berhenti.", 'y'))
    for _ in range(3):
        atah = tanya("VCC  nomor|MM|YY|CVV  ('stop' = berhenti)", meunang_kosong=True)
        if atah.lower() in ('stop', 'batal', ''):
            return None
        try:
            nomer, kadal, cvv = baca_pipa_vcc(atah)
        except SystemExit:
            print(warna("❌ format salah — contoh 5217123456789090|07|27|351", 'r'))
            continue
        try:
            nagara = pilih_nagara(nomer)
        except SystemExit:
            continue
        vcc = {'number': nomer, 'expiry': kadal, 'cvv': cvv,
               'zip': menta_pos(nagara), 'country': nagara}
        try:
            pariksa_vcc(vcc)
        except SystemExit as e:
            print(warna(f"❌ {e}", 'r'))
            continue
        return vcc
    return None


def _alur_gerbang_vcc(api):
    


    KONF["gate_vcc_hit"] = True
    panolakan = 0
    while True:
        vcc = KONF.get('vcc', {})
        if not vcc.get('number') and VCC_PANYADIA is not None:
            vcc = VCC_PANYADIA() or {}
            if vcc.get('number'):
                KONF['vcc'] = vcc
        if not vcc.get('number'):
            gagal('gate', 'akun kena gate verifikasi: isi VCC dulu (menu [5]) '
                         'atau ketik saat diminta')
        nomer, kadal = pariksa_vcc(vcc)
        try:
            pamungkas = lengkah_vcc(api, vcc, nomer, kadal)
        except KartuDitolak:
            panolakan += 1
            if panolakan >= 3:
                print(warna('\n🛑 3x kartu ditolak — berhenti.', 'r'))
                gagal('vcc', 'batas 3x penolakan kartu tercapai')
            KONF['vcc'] = {}
            vcc_anyar = _menta_kartu_ganti(panolakan)
            if not vcc_anyar:
                gagal('vcc', 'verifikasi dihentikan setelah kartu ditolak')
            KONF['vcc'] = vcc_anyar
            continue
        vonis, rincian = vonis_vcc(pamungkas)
        print(warna(f"✅ VCC BERHASIL — {rincian}", "g"))
        catet('gate', f"VCC selesai: {vonis} ({rincian})")
        _, ccv = intip_status_ccv(api)
        catet('gate', f'ccv_status pasca-VCC: {ccv!r}')
        uleman = pamundut_app(api, 'GET', '/api/hatch/invite', fatal=False)
        if uleman is None:
            gagal('gate', 'invite masih 403 setelah VCC; cek manual di https://muse.ai/access/verification')
        return uleman


def _sanggeus_auth(api, kode_reff=None):
    simpen_akun(api)
    satuju_tos(api)
                                                                      
    _, ccv = intip_status_ccv(api)
    if ccv == 'not_required':
        catet('gate', 'register TANPA VCC (ccv_status=not_required)')
        uleman = pamundut_app(api, 'GET', '/api/hatch/invite')
    elif ccv == 'blocked':
        gagal('gate', 'ccv_status=blocked (age-blocked); selesaikan manual di https://muse.ai/access/verification')
    elif ccv == 'ccv_required':
        catet('gate', 'akun perlu verifikasi VCC (ccv_status=ccv_required)')
        uleman = _alur_gerbang_vcc(api)
    else:
                                                                   
        uleman = pamundut_app(api, 'GET', '/api/hatch/invite', fatal=False)
        if uleman is None:
            catet('gate', 'invite 403 + ccv-status tak terbaca: gate VCC')
            uleman = _alur_gerbang_vcc(api)
    catet('invite', f"invite_state={uleman.json().get('invite_state')}")
    if kode_reff:
        return tebus_kode(api, kode_reff)
    return None

def alur_asup_tebus():
    reff = KONF.get('ref_code') or gagal('config', 'ref_code kosong')
    surel = KONF.get('email') or gagal('config', 'email kosong')
    api, csrf = mimitian_alur()
    token, _ = _asup_biasa(api, csrf, surel)
    if not token:
        gagal('auth', 'tidak ada frl_access_token')
    jieun_sesi(api, token)
    out = _sanggeus_auth(api, kode_reff=reff)
    catet('SELESAI', f'login {surel} -> redeem {reff}: {out}')

def normalkeun_kadaluwarsa(kadal):
    
    d = re.sub('\\D', '', kadal or '')
    if len(d) == 4:
        return d
    if len(d) == 6:
        return d[:2] + d[4:]
    gagal('config', f"expiry '{kadal}' tidak valid (pakai MM/YY)")

def pariksa_vcc(vcc):
    for k in ('number', 'expiry', 'cvv'):
        if not vcc.get(k):
            gagal('config', f'vcc.{k} kosong')
    c = (vcc.get('country') or 'US').upper().strip()
    c = ALIAS_NAGARA.get(c, c)
    if c not in NAGARA_DIDUKUNG:
        gagal('config', f"country '{vcc.get('country')}' tidak didukung; pilih: {', '.join(NAGARA_DIDUKUNG)}")
    vcc['country'] = c
    nomer = re.sub('\\D', '', vcc['number'])
    if len(nomer) < 13:
        gagal('config', 'nomor kartu tidak valid')
    return (nomer, normalkeun_kadaluwarsa(vcc['expiry']))

class CheckoutSakedap(Exception):
    pass



TANDA_SAKEDAP = ('request not completed', 'temporary problem',
                     'try again later', 'please try again')


def _sakedap_kena(teks):
    t = (teks or '').lower()
    return any(m in t for m in TANDA_SAKEDAP)


def _jaga_sakedap(beban, mana):
    s = beban if isinstance(beban, str) else json.dumps(beban or {})
    if _sakedap_kena(s):
                                                                         
                                                                              
        raise CheckoutSakedap(f'{mana}: {s[:300]}')


                                                                              
                                                                         
                                                                             
                                                             
                                                                              
META_DOK_KONCI = '23994203586844376'                                                     
META_DOK_KREDENSIAL = '27107429215520990'                           
META_DOK_PAMUNGKAS = '28179730211626671'                                        


def cokot_token_meta(html):
    
    lsd = re.search(r'"LSD"[^}]*?"token"\s*:\s*"([^"]+)"', html)
    palaku = re.search(r'"actorID"\s*:\s*"(\d+)"', html)
                                                        
    dtsg = re.search(r'\["DTSGInitialData",\[\],\{"token":"([^"]+)"', html)
    if not dtsg:
        dtsg = re.search(r'DTSGInitialData[^}]*?"token"\s*:\s*"([^"]+)"', html)
    return {
        'lsd': lsd.group(1) if lsd else '',
        'actor_id': palaku.group(1) if palaku else '',
        'fb_dtsg': dtsg.group(1) if dtsg else '',
    }


def graphql_meta(api, id_dok, ngaran_bageur, parubah, tokens):
    
    formulir = {
        '__a': '1',
        '__user': '0',
        'av': tokens['actor_id'],
        'dpr': '1',
        '__req': '1',
        '__rev': '1049502668',
        'doc_id': id_dok,
        'fb_api_caller_class': 'RelayModern',
        'fb_api_req_friendly_name': ngaran_bageur,
        'fb_dtsg': tokens.get('fb_dtsg') or '',
        'lsd': tokens['lsd'],
        'jazoest': '25661',
        'variables': json_padet(parubah),
        'server_timestamps': '1',
    }
                                                                          
    formulir = {k: nilai2 for k, nilai2 in formulir.items() if nilai2 != ''}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://auth.meta.com',
        'Referer': 'https://auth.meta.com/payments/checkout/',
        'x-fb-friendly-name': ngaran_bageur,
        'x-fb-lsd': tokens['lsd'],
    }
    r = api.post('https://auth.meta.com/api/graphql/', data=formulir, headers=headers, timeout=60)
    try:
        return r.json()
    except Exception:
        gagal('meta-gql', f'{ngaran_bageur}: respons bukan JSON: {r.text[:200]}')


def kaca_checkout_meta(api, receiver_id, product_id, id_pesenan):
    
    url = (f'https://auth.meta.com/payments/checkout/?receiver_id={receiver_id}'
           f'&product_id={product_id}&order_id={id_pesenan}')
    r = api.get(url, headers={'Referer': DASAR_MUSE + '/access/verification',
                              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
                timeout=60)
    if r.status_code != 200:
        gagal('meta-page', f'checkout page HTTP {r.status_code}')
    tokens = cokot_token_meta(r.text)
    if not tokens['lsd']:
        gagal('meta-page', 'LSD token tidak ketemu di HTML checkout')
    catet('meta-page', f"LSD+actor didapat (actor={tokens['actor_id'][:6]}... dtsg={'YA' if tokens['fb_dtsg'] else 'TIDAK'})")
    return tokens


def candak_konci_meta(api, tokens, id_sesi_upl, product_id, receiver_id, id_sesi_otc):
    
    parubah = {"input": {
        "device_id": "device_id",
        "fetch_unified_wallet_key": None,
        "fetch_unified_wallet_key_under_target_vc": None,
        "one_time_checkout_input": {"otc_session_id": id_sesi_otc, "otc_type": "CARD"},
        "payment_product_id": str(product_id),
        "payment_type": "ECP",
        "receiver_id": str(receiver_id),
        "session_id": id_sesi_upl,
        "actor_id": tokens['actor_id'],
        "client_mutation_id": str(uuid.uuid4()),
    }}
    data = graphql_meta(api, META_DOK_KONCI, 'PaymentsCometGetServerEncryptionKeyMutation',
                        parubah, tokens)
    data_konci = (data.get('data') or {}).get('get_server_encryption_key') or {}
    tc = data_konci.get('trust_chain') or []
    if not tc:
        gagal('meta-key', f'trust_chain kosong: {str(data)[:300]}')
    catet('meta-key', f"key id={data_konci.get('id')} dev_external={data_konci.get('dev_external')}")
    return tc


def jieun_kredensial_meta(api, tokens, id_sesi_upl, id_sesi_otc, id_pesenan,
                           product_id, receiver_id, token_ptt, vcc, nomer, kadal):
    
    nomer = re.sub(r'\D', '', nomer)
    nagara = (vcc.get('country') or 'US').upper()
    parubah = {"input": {
        "captcha_token": "",
        "client_receiver_id": str(receiver_id),
        "credential_input": {
            "credential_id": None,
            "credential_type": "CREDIT_CARD",
            "mutation_type": "CREATE",
            "save_credential_input": {
                "billing_address": {
                    "city": "", "country_code": nagara, "state": "",
                    "street1": "", "street2": "", "zip": vcc.get('zip', ''),
                },
                "cardholder_email": "",
                "cardholder_name": "",
                "cardholder_phone_number": "",
                "credit_card_first_6": {"sensitive_string_value": nomer[:6]},
                "credit_card_last_4": {"sensitive_string_value": nomer[-4:]},
                "credit_card_number": {"sensitive_string_value": "$e2ee"},
                "csc": {"sensitive_string_value": "$e2ee"},
                "expiry_month": kadal[:2],
                "expiry_year": '20' + kadal[2:4],
                "is_consent_required": False,
                "risk_features": "",
            },
        },
        "email_input": None,
        "one_time_checkout_input": {"otc_session_id": id_sesi_otc, "otc_type": "CARD"},
        "order_id": str(id_pesenan),
        "payer_name_input": None,
        "phone_input": None,
        "platform_trust_token": token_ptt,
        "product_id": str(product_id),
        "session_id": id_sesi_upl,
        "shipping_address_input": None,
        "tax_id_input": None,
        "actor_id": tokens['actor_id'],
        "client_mutation_id": "",
    },
    "product_id": str(product_id)}
    data = graphql_meta(api, META_DOK_KREDENSIAL, 'useFBPayAccountMutation',
                        parubah, tokens)
    mutasi = (data.get('data') or {}).get('fbpay_account_mutation') or {}
    waleran_kredensial = mutasi.get('credential_response') or {}
    kredensial = waleran_kredensial.get('credential')
    if kredensial and kredensial.get('id'):
        catet('meta-cred', f"credentialId={kredensial.get('id')}")
        return kredensial.get('id')
                                                                                
                                                                            
    eror = waleran_kredensial.get('error') or mutasi.get('error') or {}
    try:
        catet('meta-cred-err', f"full={json.dumps(eror, ensure_ascii=False)[:1500]}")
    except Exception:
        catet('meta-cred-err', f"full={str(eror)[:1500]}")
    pesen = f"{eror.get('error_title') or eror.get('title')}: {eror.get('error_message') or eror.get('description')}"
    kode = str(eror.get('error_code') or '')
                                                                        
                                                                                
                                                                                
                                                                        
                                               
    if eror and (kode or pesen.strip(': ')):
        if _tolak_kena(pesen) or _tolak_kena(kode) or kode.startswith('2078'):
            gagal_tolak('meta-credential', pesen, kode)
        gagal('meta-cred', f'gagal terstruktur (bukan transient, tidak di-retry): {pesen} code={kode}')
                                                                                
    _jaga_sakedap(data, 'meta/credential')
    gagal('meta-cred', f'gagal: {pesen} code={kode} | {str(data)[:300]}')


def pamungkas_checkout_meta(api, tokens, id_sesi_upl, id_sesi_otc, id_pesenan,
                           product_id, receiver_id, id_kredensial2, kadal, vcc):
    
    nagara = (vcc.get('country') or 'US').upper()
    wadah_ptt = token_wadah_ptt(id_pesenan, receiver_id, 'LIVE', '1.00',
                                        'USD', id_kredensial2, kadal[:2], '20' + kadal[2:4])
    parubah = {"input": {
        "apm_fields": {"failure_url": None, "success_url": None},
        "apm_return_method": "APP_URL",
        "auth_factors": {"cvv_platform_trust_token": None,
                         "platform_trust_token": wadah_ptt},
        "checkout_info_fields": {
            "billing_address": {
                "city": "", "country_code": nagara, "state": "",
                "street1": "", "street2": "", "zip": vcc.get('zip', ''),
            },
            "gift_aid_checkbox_value": False,
            "payer_name": None,
            "tax_id_info": None,
        },
        "client_domain_origin": None,
        "country_code": "US",
        "credentials": [{
            "charge_amount": {"amount": "1.00", "currency_code": "USD"},
            "credential_id": str(id_kredensial2),
            "credential_type": "CREDIT_CARD",
        }],
        "ecp_order_id": str(id_pesenan),
        "one_time_checkout_input": {"otc_session_id": id_sesi_otc, "otc_type": "CARD"},
        "pay_button_click_id": str(uuid.uuid4()),
        "payment_product_id": str(product_id),
        "payment_request_id": str(uuid.uuid4()),
        "receiver_info": [{
            "charge_amount": {"amount": "1.00", "currency_code": "USD"},
            "receiver_id": str(receiver_id),
        }],
        "risk_data": {"paypal_fraudnet_id": None},
        "upl_session_id": id_sesi_upl,
        "actor_id": tokens['actor_id'],
        "client_mutation_id": "1",
    }}
    data = graphql_meta(api, META_DOK_PAMUNGKAS, 'useECPCometFinalizeCheckoutMutation',
                        parubah, tokens)
    _jaga_sakedap(data, 'meta/finalize')
    return data


def _lengkah_vcc_sakali(api, vcc, nomer, kadal):
    
    product_id = KONF.get('product_id')
    receiver_id = KONF.get('receiver_id')
    id_sesi_upl, data_awal = mimitian_checkout(api, product_id, receiver_id)
    _jaga_sakedap(data_awal, 'checkout/init')
    sup = (data_awal.get('paymentMethod') or {}).get('supportedCardTypes') or []
    merek = merek_kartu(nomer)
    catet('vcc-brand', f"kartu={merek} didukung={sup or '?'}")
    if sup and merek not in sup:
        gagal('vcc', f"kartu {merek} tidak didukung {sup}; pakai {'/'.join(sup)}")
    nagara_hirup = [c.get('countryCode') for c in (data_awal.get('paymentMethod') or {}).get('countryPostalPolicy', {}).get('countries', [])]
    nagara = vcc.get('country', 'US')
    if nagara_hirup and nagara not in nagara_hirup:
        gagal('vcc', f"country {nagara} tidak didukung live; pilih: {', '.join(nagara_hirup)}")
    if not vcc.get('zip'):
                                                                           
                                                                      
        vcc['zip'] = jieun_pos(nagara)
                                                                  
    id_pesenan = data_awal['orderId']
    tokens = kaca_checkout_meta(api, receiver_id, product_id, id_pesenan)
    id_sesi_otc = str(uuid.uuid4())
    rantai_kapercayaan = candak_konci_meta(api, tokens, id_sesi_upl, product_id, receiver_id,
                               id_sesi_otc)
    ptt = token_kartu_ptt(rantai_kapercayaan[0], nomer, vcc['cvv'], kadal[:2], '20' + kadal[2:4])
    catet('vcc-ptt', f'token E2EE dibangun ({len(ptt)} char) app_id={ID_APP_PTT}')
    id_kredensial = jieun_kredensial_meta(api, tokens, id_sesi_upl, id_sesi_otc,
                                     id_pesenan, product_id, receiver_id,
                                     ptt, vcc, nomer, kadal)
    pamungkas = pamungkas_checkout_meta(api, tokens, id_sesi_upl, id_sesi_otc,
                                   id_pesenan, product_id, receiver_id,
                                   id_kredensial, kadal, vcc)
                                                                                       
    _tungtung = (pamungkas.get('data') or {}).get('ecp_finalize_checkout') or {}
    _eror_gagal = _tungtung.get('error') or {}
    _kode_gagal = str(_eror_gagal.get('error_code') or _eror_gagal.get('code') or '')
    if _eror_gagal and (_kode_gagal or _eror_gagal.get('error_message') or _eror_gagal.get('message')):
        if _tolak_kena(str(_eror_gagal)) or _kode_gagal.startswith('2078'):
            gagal_tolak('meta-finalize', _eror_gagal.get('error_message') or _eror_gagal.get('message'), _kode_gagal)
        gagal('meta-fin', f'finalize gagal terstruktur (bukan transient, tidak di-retry): code={_kode_gagal}')
    _jaga_sakedap(pamungkas, 'meta/finalize')
    return pamungkas


def lengkah_vcc(api, vcc, nomer, kadal):
    



    ngaran_tukang = None
    for a in range(3):
        try:
            return _lengkah_vcc_sakali(api, vcc, nomer, kadal)
        except CheckoutSakedap as e:
            ngaran_tukang = e
                                                                              
                                                                         
                                                                        
                                                                           
                                                        
        antos = 60 * (a + 1)
        catet('vcc-retry', f'transient server ({ngaran_tukang}); tunggu {antos}s, ulangi ({a + 1}/3)')
        time.sleep(antos)
    gagal('vcc', f'gagal 3x karena transient server: {ngaran_tukang}')

def alur_verifikasi_vcc():
    surel = KONF.get('email') or gagal('config', 'email kosong')
    api, csrf = mimitian_alur()
    token, _ = _asup_biasa(api, csrf, surel)
    if not token:
        gagal('auth', 'tidak ada frl_access_token')
    jieun_sesi(api, token)
    simpen_akun(api)
                                                                     
    _, ccv = intip_status_ccv(api)
    if ccv == 'not_required':
        catet('SELESAI', f'akun {surel} TANPA VCC '
                       '(ccv_status=not_required); tidak ada yg diverifikasi')
        return
    if ccv == 'blocked':
        gagal('gate', 'ccv_status=blocked (age-blocked); selesaikan manual di '
                     'https://muse.ai/access/verification')
    catet('gate', f"ccv_status={ccv!r}: lanjut verifikasi VCC")
    uleman = _alur_gerbang_vcc(api)
    try:
        kaayaan_uleman = uleman.json().get('invite_state')
    except Exception:
        kaayaan_uleman = '?'
    print(warna(f"✅ VCC VERIFY SELESAI — {surel} (invite_state={kaayaan_uleman})", "g"))
    catet('SELESAI', f'VCC verify {surel}: invite_state={kaayaan_uleman}')

def alur_pariksa_ccv():
    



    surel = KONF.get('email') or gagal('config', 'email kosong')
    api, csrf = mimitian_alur()
    token, _ = _asup_biasa(api, csrf, surel)
    if not token:
        gagal('auth', 'tidak ada frl_access_token')
    jieun_sesi(api, token)
    kode, ccv = intip_status_ccv(api)
    uleman = pamundut_app(api, 'GET', '/api/hatch/invite', fatal=False)
    kaayaan_uleman = uleman.json().get('invite_state') if uleman is not None else '403/gate'
    print(warna(f"\n🔍 HASIL CEK {surel}:", 'b'))
    print(f"   ccv_status   = {ccv!r} (HTTP {kode})")
    print(f"   invite_state = {kaayaan_uleman}")
    print(warna("   not_required = TANPA VCC, langsung bisa redeem", 'g'))
    print(warna("   ccv_required = kena gate VCC", 'y'))
    catet('SELESAI', f"cek {surel}: ccv_status={ccv!r} invite_state={kaayaan_uleman}")

AC_DASAR = 'https://accountscenter.meta.com'
AC_KACA_CP = AC_DASAR + '/youraccount/contact_points/'
AC_GQL = AC_DASAR + '/api/graphql/'
AC_DOK_DAPTAR = '26526896596904983'
AC_DOK_NAMBAH = '8929017267200363'
AC_DOK_VERIFIKASI = '33295109726800304'
AC_DOK_PUPUS = '9412959315500210'
AC_AGEN = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36'
AC_ASBD = '359341'
BERKAS_TUKER_SUREL = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'EmailGanti.txt')


def _ac_acak(n, hurup='abcdefghijklmnopqrstuvwxyz0123456789_'):
    return ''.join(random.choice(hurup) for _ in range(n))


def _ac_sesi_anyar():
    s = cr.Session(impersonate=TIRU_JALAN, proxies=PROKSI)
    s.headers.update({'User-Agent': AC_AGEN, 'Accept': '*/*', 'Accept-Language': 'en-US,en;q=0.9'})
    return s


def _ac_muat_kuki(sesi, atah):
    luncat = {'expires', 'max-age', 'path', 'domain', 'samesite', 'secure', 'httponly'}
    n = 0
    for bagian in atah.split(';'):
        bagian = bagian.strip()
        if not bagian or '=' not in bagian:
            continue
        k, nilai2 = bagian.split('=', 1)
        k = k.strip()
        nilai2 = nilai2.strip().strip('"')
        if not k or not nilai2 or k.lower() in luncat:
            continue
        sesi.cookies.set(k, nilai2, domain='.meta.com', path='/')
        n += 1
    return n


def _ac_token(sesi):
    try:
        r = sesi.get(AC_KACA_CP, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Referer': AC_DASAR + '/', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'same-origin', 'Upgrade-Insecure-Requests': '1'}, timeout=45)
    except Exception as e:
        catet('ac-page', f'GET contact_points gagal: {e}')
        return {}
    if r.status_code != 200:
        catet('ac-page', f'HTTP {r.status_code}')
        return {}
    t = cokot_token_meta(r.text)
    catet('ac-page', f"dtsg={'YA' if t.get('fb_dtsg') else 'TIDAK'} lsd={'YA' if t.get('lsd') else 'TIDAK'}")
    return t


def _ac_tanya(sesi, tokens, id_dok, bageur, parubah):
    formulir = {'__a': '1', '__user': '0', 'av': tokens.get('actor_id') or '', 'dpr': '1', '__req': '1', 'doc_id': id_dok, 'fb_api_caller_class': 'RelayModern', 'fb_api_req_friendly_name': bageur, 'fb_dtsg': tokens.get('fb_dtsg') or '', 'lsd': tokens.get('lsd') or '', 'jazoest': '25661', 'variables': json_padet(parubah), 'server_timestamps': '1'}
    formulir = {k: nilai2 for k, nilai2 in formulir.items() if nilai2 != ''}
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Origin': AC_DASAR, 'Referer': AC_KACA_CP, 'x-fb-friendly-name': bageur, 'x-fb-lsd': tokens.get('lsd') or '', 'x-asbd-id': AC_ASBD, 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty'}
    r = sesi.post(AC_GQL, data=formulir, headers=headers, timeout=60)
    try:
        return r.json()
    except Exception:
        gagal('ac-gql', f'{bageur}: respons bukan JSON (HTTP {r.status_code}): {r.text[:200]}')


def _ac_titik(d, konci):
    if not isinstance(d, dict):
        gagal('ac-gql', f'respons tak dikenal: {str(d)[:160]}')
    if d.get('errors'):
        eror = d['errors'][0]
        gagal('ac-gql', f"GraphQL error: {eror.get('message') or eror}")
    data = d.get('data') or {}
    titik = data.get(konci)
    if titik is None:
        gagal('ac-gql', f'tidak ada {konci} di respons: {str(data)[:200]}')
    return titik


def _ac_baca_cp(d):
    titik = ((d.get('data') or {}).get('fxcal_settings') or {}).get('node') or {}
    daptar_cp = titik.get('all_contact_points')
    if not daptar_cp:
        daptar_cp = (titik.get('content') or {}).get('all_contact_points')
    out = []
    for c in daptar_cp or []:
        out.append({'id': c.get('contact_point_id'), 'email': c.get('normalized_contact_point'), 'type': c.get('contact_point_type'), 'status': c.get('contact_point_status')})
    return out


def _ac_daptar_coba(sesi, tokens):
    atah = ''
    daptar_cp = []
    for i in range(3):
        d = _ac_tanya(sesi, tokens, AC_DOK_DAPTAR, 'FXAccountsCenterUnifiedContactPointRootQuery', {'interface': 'FRL_WEB'})
        atah = json_padet(d)[:1500]
        daptar_cp = _ac_baca_cp(d)
        if daptar_cp:
            break
        catet('ac-list', f'kosong — tunggu 10 dtk, coba lagi ({i + 1}/3)')
        time.sleep(10)
    catet('ac-list', f'{len(daptar_cp)} contact point terbaca')
    return daptar_cp, atah


def _ac_saring_surel(daptar_cp):
    return [c for c in daptar_cp if (c.get('type') or '').upper() == 'EMAIL' and c.get('id') and c.get('email')]


def _ac_pastikeun_sesi(api, paksa_tempel):
    sesi = api
    tokens = {} if paksa_tempel else _ac_token(sesi)
    if not tokens.get('fb_dtsg') or not tokens.get('lsd'):
        print(warna('\nℹ  sesi login tidak bisa membuka Meta Accounts Center.', 'y'))
        print(warna('   Buka di browser (sudah login akun ini):', 'w'))
        print(warna('   https://accountscenter.meta.com/youraccount/contact_points/', 'w'))
        print(warna('   DevTools (F12) → Application → Cookies → copy SEMUA cookie jadi satu baris', 'w'))
        print(warna('   format: nama1=nilai1; nama2=nilai2; ...  lalu paste di bawah.', 'w'))
        atah = tanya('paste cookie accountscenter.meta.com')
        sesi = _ac_sesi_anyar()
        n = _ac_muat_kuki(sesi, atah)
        catet('ac-cookie', f'{n} cookie dimuat (RAM saja, tidak disimpan)')
        tokens = _ac_token(sesi)
        if not tokens.get('fb_dtsg') or not tokens.get('lsd'):
            gagal('ac-auth', 'cookie tidak valid / sesi habis — login ulang di browser lalu paste lagi')
    catet('ac-auth', 'Meta Accounts Center OK')
    return sesi, tokens


def _ac_nambah(sesi, tokens, id_alat, surel):
    d = _ac_tanya(sesi, tokens, AC_DOK_NAMBAH, 'FXAccountsCenterUnifiedAddContactPointMutation', {'country': 'US', 'contact_point': surel, 'contact_point_type': 'EMAIL', 'family_device_id': id_alat, 'client_mutation_id': _ac_acak(25)})
    titik = _ac_titik(d, 'xfb_add_feta_contact_point')
    return bool(titik.get('success')), titik.get('error_text') or '', titik.get('normalized_contact_point') or ''


def _ac_verifikasi(sesi, tokens, id_alat, surel, pin):
    d = _ac_tanya(sesi, tokens, AC_DOK_VERIFIKASI, 'FXAccountsCenterUnifiedVerifyContactPointMutation', {'contact_point': surel, 'contact_point_type': 'EMAIL', 'pin_code': pin, 'family_device_id': id_alat, 'client_mutation_id': _ac_acak(25), 'contact_point_source': 'fx_settings'})
    titik = _ac_titik(d, 'xfb_verify_feta_contact_point')
    return bool(titik.get('success')), titik.get('error_text') or ''


def _ac_pupus(sesi, tokens, id_alat, id_cp):
    d = _ac_tanya(sesi, tokens, AC_DOK_PUPUS, 'FXAccountsCenterUnifiedDeleteContactPointMutation', {'contact_point_id': id_cp, 'contact_point_type': 'EMAIL', 'client_mutation_id': _ac_acak(25), 'family_device_id': id_alat})
    titik = _ac_titik(d, 'xfb_delete_feta_contact_point')
    return bool(titik.get('success')), titik.get('error_text') or ''


def alur_tuker_surel():
    surel = KONF.get('email') or gagal('config', 'email kosong')
    api, csrf = mimitian_alur()
    token, _ = _asup_biasa(api, csrf, surel)
    if not token:
        gagal('auth', 'tidak ada frl_access_token')
    jieun_sesi(api, token)
    catet('login', f'login OK: {surel}')
    sesi, tokens = _ac_pastikeun_sesi(api, False)
    daptar_cp, atah = _ac_daptar_coba(sesi, tokens)
    daptar_surel = _ac_saring_surel(daptar_cp)
    if not daptar_surel:
        print(warna('\nℹ  daftar contact point kosong / tidak ada email.', 'y'))
        print(warna('   respons mentah (untuk debug):', 'w'))
        print('   ' + atah[:1200])
        if pastikeun('coba lagi dengan cookie browser (sesi lain)?'):
            sesi, tokens = _ac_pastikeun_sesi(api, True)
            daptar_cp, atah = _ac_daptar_coba(sesi, tokens)
            daptar_surel = _ac_saring_surel(daptar_cp)
        if not daptar_surel:
            gagal('ac-list', 'tidak ada email terdaftar di akun ini')
    heubeul = None
    for c in daptar_surel:
        if (c.get('email') or '').lower() == surel.lower():
            heubeul = c
            break
    if heubeul is None:
        print(warna('\n📧 email yg terdaftar di akun ini:', 'b'))
        for i, c in enumerate(daptar_surel, 1):
            print(f"   [{i}] {c.get('email')} ({c.get('status')})")
        atah = tanya('pilih nomor email yg mau diganti')
        try:
            heubeul = daptar_surel[int(atah) - 1]
        except (ValueError, IndexError):
            gagal('ac-list', 'pilihan tidak valid')
    print(warna(f"\n📧 email lama : {heubeul.get('email')}", 'y'))
    surel_anyar = tanya('email BARU pengganti').strip()
    if '@' not in surel_anyar:
        gagal('input', 'email baru tidak valid')
    if not pastikeun(f"ganti {heubeul.get('email')} -> {surel_anyar} ?"):
        print(warna('dibatalkan', 'y'))
        return False
    id_alat = _ac_acak(20, 'abcdefghijklmnopqrstuvwxyz_')
    sae, pesen, normal = _ac_nambah(sesi, tokens, id_alat, surel_anyar)
    if not sae:
        gagal('ac-add', f'gagal tambah email baru: {pesen or "unknown"}')
    tujuan = normal or surel_anyar
    catet('ac-add', f'email baru ditambahkan — kode OTP dikirim ke {tujuan}')
    print(warna(f'\n📩 kode OTP dikirim ke {tujuan} — buka inbox email itu', 'b'))
    parantos = False
    for i in range(3):
        pin = tanya(f'kode OTP email baru (coba {i + 1}/3)').strip()
        if not pin:
            continue
        sae, pesen = _ac_verifikasi(sesi, tokens, id_alat, tujuan, pin)
        if sae:
            parantos = True
            break
        print(warna(f"❌ OTP salah/kadaluarsa: {pesen or 'coba lagi'}", 'r'))
    if not parantos:
        gagal('ac-verify', 'verifikasi email baru gagal 3x — email baru belum aktif, email lama masih nempel')
    catet('ac-verify', 'email baru terverifikasi')
    sae, pesen = _ac_pupus(sesi, tokens, id_alat, heubeul['id'])
    if not sae:
        gagal('ac-delete', f"email baru AKTIF tapi unbind email lama gagal: {pesen or 'unknown'} — hapus manual di Accounts Center")
    catet('ac-delete', f"email lama {heubeul.get('email')} di-unbind")
    with open(BERKAS_TUKER_SUREL, 'a', encoding='utf-8') as f:
        f.write(f"{surel} -> {surel_anyar} # OK {time.strftime('%Y-%m-%d %H:%M')}\n")
    print(warna(f'\n✅ SELESAI — {surel} -> {surel_anyar}', 'g'))
    print(warna(f'   email lama sudah di-unbind. Catatan: {BERKAS_TUKER_SUREL}', 'w'))
    return True



def baca_pipa_vcc(s):
    

    bagian2 = [p.strip() for p in s.split('|')]
    if len(bagian2) == 4:
        nomer, bulan, taun2, cvv = bagian2
        kadal = normalkeun_kadaluwarsa(bulan + taun2)
    elif len(bagian2) == 3:
        nomer, kadal_atah, cvv = bagian2
        kadal = normalkeun_kadaluwarsa(kadal_atah)
    else:
        gagal('input', 'format VCC: number|MM|YY|cvv  atau  number|MMYY|cvv')
    return (re.sub('\\D', '', nomer), kadal, cvv.strip())

def jieun_pos(nagara):
    


    return ''

"""geo.py — fuzzy country & validasi proxy wajib US.

- match_country(text): user mengetik 'indo' / 'Indonesia' / 'id' / 'ID' → 'ID'.
  Berlaku untuk SEMUA negara yg didukung engine (62 kode) dgn alias
  Indonesia & Inggris umum + kode ISO alpha-2/alpha-3.
- proxy info & wajib-US: geo_check_proxy(proxy) memakai ip-api.com (tanpa key).
"""
import random
import re
NAGARA = {'US': ('United States', ['usa', 'amerika', 'amerika serikat', 'america', 'united states of america', 'us', 'u.s.']), 'CA': ('Canada', ['kanada']), 'GB': ('United Kingdom', ['uk', 'inggris', 'england', 'british', 'britania raya']), 'DZ': ('Algeria', ['aljazair']), 'AR': ('Argentina', ['argentina']), 'AU': ('Australia', ['australian', 'aussie', 'aus', 'oz']), 'AT': ('Austria', []), 'BE': ('Belgium', ['belgia']), 'BR': ('Brazil', ['brasil', 'brazil']), 'CL': ('Chile', ['cile']), 'CO': ('Colombia', ['kolombia']), 'CI': ('Ivory Coast', ['cote divoire', 'pantai gading', 'ivory']), 'HR': ('Croatia', ['kroasia']), 'CZ': ('Czechia', ['ceko', 'czech republic', 'czech']), 'DK': ('Denmark', ['denmark']), 'EG': ('Egypt', ['mesir']), 'FI': ('Finland', ['finlandia']), 'FR': ('France', ['prancis', 'france']), 'DE': ('Germany', ['jerman', 'germany']), 'GH': ('Ghana', []), 'HK': ('Hong Kong', ['hongkong', 'hong kong']), 'IS': ('Iceland', ['islandia']), 'IN': ('India', []), 'ID': ('Indonesia', ['indo', 'ri', 'nkri', 'idn', 'republik indonesia', 'indonesian']), 'IE': ('Ireland', ['irlandia']), 'IL': ('Israel', []), 'IT': ('Italy', ['italia', 'italy']), 'JP': ('Japan', ['jepang', 'japan']), 'KE': ('Kenya', []), 'LB': ('Lebanon', ['lebanon']), 'MY': ('Malaysia', ['malaisia', 'malaysia']), 'MX': ('Mexico', ['meksiko', 'mexico']), 'MA': ('Morocco', ['maroko']), 'NL': ('Netherlands', ['belanda', 'holland', 'netherland']), 'NZ': ('New Zealand', ['selandia baru', 'new zealand']), 'NG': ('Nigeria', []), 'NO': ('Norway', ['norwegia']), 'PK': ('Pakistan', []), 'PH': ('Philippines', ['filipina', 'philippine', 'pinoy', 'ph']), 'PL': ('Poland', ['polandia', 'polska']), 'PT': ('Portugal', []), 'QA': ('Qatar', []), 'RO': ('Romania', ['rumania']), 'SA': ('Saudi Arabia', ['arab saudi', 'saudi', 'ksa', 'saudi arabia']), 'SN': ('Senegal', []), 'SG': ('Singapore', ['singapura', 'sgp', 'singapore']), 'ZA': ('South Africa', ['afrika selatan', 'afsel', 'south africa']), 'KR': ('South Korea', ['korea', 'south korea', 'korsel', 'korea selatan', 'kor']), 'ES': ('Spain', ['spanyol', 'espana', 'esy']), 'SE': ('Sweden', ['swedia']), 'CH': ('Switzerland', ['swiss']), 'TW': ('Taiwan', []), 'TH': ('Thailand', ['thai', 'thailand']), 'TR': ('Turkey', ['turki', 'turkiye', 'turkey']), 'AE': ('United Arab Emirates', ['uae', 'emirates', 'uni emirat arab', 'uea', 'dubai']), 'VN': ('Vietnam', ['vietnam', 'vietnamese', 'vn']), 'ZM': ('Zambia', []), 'ZW': ('Zimbabwe', [])}
_ALFA3 = {'USA': 'US', 'CAN': 'CA', 'GBR': 'GB', 'DZA': 'DZ', 'ARG': 'AR', 'AUS': 'AU', 'AUT': 'AT', 'BEL': 'BE', 'BRA': 'BR', 'CHL': 'CL', 'COL': 'CO', 'CIV': 'CI', 'HRV': 'HR', 'CZE': 'CZ', 'DNK': 'DK', 'EGY': 'EG', 'FIN': 'FI', 'FRA': 'FR', 'DEU': 'DE', 'GHA': 'GH', 'HKG': 'HK', 'ISL': 'IS', 'IND': 'IN', 'IDN': 'ID', 'IRL': 'IE', 'ISR': 'IL', 'ITA': 'IT', 'JPN': 'JP', 'KEN': 'KE', 'LBN': 'LB', 'MYS': 'MY', 'MEX': 'MX', 'MAR': 'MA', 'NLD': 'NL', 'NZL': 'NZ', 'NGA': 'NG', 'NOR': 'NO', 'PAK': 'PK', 'PHL': 'PH', 'POL': 'PL', 'PRT': 'PT', 'QAT': 'QA', 'ROU': 'RO', 'SAU': 'SA', 'SEN': 'SN', 'SGP': 'SG', 'ZAF': 'ZA', 'KOR': 'KR', 'ESP': 'ES', 'SWE': 'SE', 'CHE': 'CH', 'TWN': 'TW', 'THA': 'TH', 'TUR': 'TR', 'ARE': 'AE', 'VNM': 'VN', 'ZMB': 'ZM', 'ZWE': 'ZW'}
_INDEKS = {}

def _normalkeun(s):
    return re.sub('[^a-z0-9 ]+', ' ', str(s or '').lower()).replace('  ', ' ').strip()

def _bangun_indeks():
    for kode, (ngaran, alias) in NAGARA.items():
        syarat = {kode.lower(), ngaran.lower(), _normalkeun(ngaran)}
        for a in alias:
            syarat.add(a.lower())
            syarat.add(_normalkeun(a))
        for t in syarat:
            if t:
                _INDEKS.setdefault(t, kode)
    for a3, kode in _ALFA3.items():
        _INDEKS.setdefault(a3.lower(), kode)
_bangun_indeks()
RESMI = {c: n for c, (n, _) in NAGARA.items()}

def cocokkeun_nagara(teks):
    
    t = _normalkeun(teks)
    if not t:
        return None
    if len(t) == 2 and t.upper() in NAGARA:
        return t.upper()
    if t in _INDEKS:
        return _INDEKS[t]
    return None

def pos_acak(nagara):
    

    return ''


def menta_pos(nagara):
    
    if nagara not in ('US', 'CA'):
        return ''
    if not sys.stdin.isatty():
        return ''
    z = tanya("ZIP billing kartu US/CA (asli dari provider; kosongkan kalau tidak tahu)",
            meunang_kosong=True).strip()
    if z:
        catet('addr', f"ZIP billing diisi manual: {z}")
    else:
        catet('addr', "ZIP dikosongkan (tanpa karangan) — test AVS hypothesis")
    return z
POLA_PROKSI = re.compile('^(https?|socks5h?|socks4)://', re.I)

def baca_proksi(teks):
    import urllib.parse
    t = (teks or '').strip().strip('<>')
    if not POLA_PROKSI.match(t):
        raise ValueError('Format salah — contoh: <code>http://user:pass@host:port</code> atau <code>socks5://user:pass@host:port</code>')
    u = urllib.parse.urlparse(t)
    if not u.hostname or not u.port:
        raise ValueError('Host/port tidak lengkap.')
    return t

def samarkeun_proksi(p):
    import urllib.parse
    t = (p or '').strip()
    if not t:
        return '(langsung)'
    try:
        u = urllib.parse.urlparse(t)
        otentikasi = '***:***@' if u.username else ''
        return f'{u.scheme}://{otentikasi}{u.hostname}:{u.port}'
    except Exception:
        return '***'

def pariksa_geo_proksi(proksi, timeout=18):
    

    try:
        import curl_cffi.requests as cr
    except ImportError:
        return {'ok': False, 'error': 'curl_cffi belum terpasang di server.'}
    eror = '?'
    for _coba in range(3):
        try:
            s = cr.Session(impersonate='chrome', proxies={'http': proksi, 'https': proksi})
            r = s.get('http://ip-api.com/json/?fields=status,country,countryCode,query', timeout=timeout)
            d = r.json()
            if d.get('status') != 'success':
                eror = f"ip-api menolak (status={d.get('status')})."
                continue
            return {'ok': True, 'country_code': d.get('countryCode', ''), 'country': d.get('country', ''), 'ip': d.get('query', '')}
        except Exception as e:
            eror = f'{type(e).__name__}: {str(e)[:140]}'
            try:
                s.close()
            except Exception:
                pass
    return {'ok': False, 'error': f'setelah 3x coba: {eror}'}

def vonis_us(info):
    
    if not info.get('ok'):
        return (False, f"Proxy tidak bisa dipakai: {info.get('error', '?')[:160]}")
    if info.get('country_code') != 'US':
        return (False, f"Proxy ini bernegara <b>{info.get('country') or '?'}</b> ({info.get('country_code') or '?'}) — sedangkan muse.ai <b>wajib IP Amerika (US)</b>.")
    return (True, info.get('ip', ''))



                                                                       
import json, os, time, shutil

C = {"g": "\033[92m", "y": "\033[93m", "r": "\033[91m", "c": "\033[96m",
     "b": "\033[94m", "w": "\033[97m", "bold": "\033[1m", "0": "\033[0m"}
if os.name == "nt":
    try:
        os.system("")
    except Exception:
        pass

BERKAS_KAAYAAN = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".muse_state.json")
BERKAS_RIWAYAT = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".muse_history.json")
BERKAS_JESTCO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Jestco.txt")
VERSI = "2.10.0"


def warna(teks2, k):
    if not sys.stdout.isatty():
        return teks2
    return f"{C[k]}{teks2}{C['0']}"


def spanduk():
    print(warna("""
╔══════════════════════════════════════════════════╗
║      🎧   MUSE PRO CLI   v""" + VERSI + """   🎧        ║
║      Creator @JoestarMojo — Gratis Komunitas     ║
╚══════════════════════════════════════════════════╝""", "c"))
    print(warna("  ⚠  IP tujuan harus US — bisa dari VPN / proxy (opsional)", "y"))
    print(warna("  🔒 VCC TIDAK disimpan (RAM saat run) • Proxy tersimpan biar tak input ulang", "w"))
    print(warna("  📜 email yang jalan masuk History (menu 6) — bisa dihapus (menu 7)", "w"))


def maca_json(path, baku):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return baku


def simpen_json(path, objek):
    with open(path, "w") as f:
        json.dump(objek, f, indent=1)


def kaayaan():
    s = maca_json(BERKAS_KAAYAAN, {"proxy": "", "reff": ""})
    s.setdefault("proxy", ""); s.setdefault("reff", "")
    return s


def tanya(pananya, meunang_kosong=False):
    while True:
        nilai2 = input(warna("» ", "g") + pananya + ": ").strip()
        if nilai2 or meunang_kosong:
            return nilai2
        print(warna("  (kosong — ketik dulu ya)", "y"))


def pastikeun(pananya):
    return input(warna("» ", "y") + pananya + " " + warna("[y/N]", "w") + " ").strip().lower() == "y"


def menu(wanda):
    p = warna(f"🌐 Proxy: {samarkeun_proksi(wanda['proxy'])} ✔", "g") if wanda["proxy"]\
        else warna("🌐 Proxy: tidak diset — jalan pakai IP sistem/VPN (harus US!)", "y")
    r = warna(f"🔑 Reff : {wanda['reff']}", "g") if wanda["reff"]\
        else warna("🔑 Reff : (belum — run berhenti sampai register)", "y")
    print(f"""
{p}
{r}
──────────────────────────────────────────────
  [{warna('1','b')}] 🔁 Set Proxy (opsional)
  [{warna('2','b')}] 🔑 Set Kode Reff
  [{warna('3','b')}] 📝 Register Muse       (email kamu sendiri)
  [{warna('4','b')}] ♻️  Redeem Reff Saja   (akun yg sudah ada)
  [{warna('5','b')}] 💳 VCC Verify Saja
  [{warna('6','b')}] 📜 History Akun
  [{warna('7','b')}] 🧹 Hapus Data Saya
  [{warna('8','b')}] 🌍 Cek IP-ku & Negara (via proxy kalau diset)
  [{warna('9','b')}] ℹ️  PENTING BACA (anti-gagal)
  [{warna('10','b')}] 🔍 Cek ccv-status email (tanpa redeem/VCC)
  [{warna('11','b')}] 🤖 Auto Register Jestco (→ Jestco.txt)
  [{warna('12','b')}] 📧 Ganti Email + Unbind Email Lama
  [{warna('0','r')}] 🚪 Keluar
──────────────────────────────────────────────""")


def catetan_penting():
    print(warna("""
📢 PENTING — 5 menit biar gak gagal terus:
1. Email yang pernah dipakai FACEBOOK jauh lebih jarang diminta VCC.
2. IP ke muse.ai HARUS US 🇺🇸 — pakai VPN US (paling bagus) atau set proxy. Cek dulu menu [8]!
3. Tanpa reff → run cuma SAMPAI register (tanpa redeem — bukan error).
4. Kalau di tengah run minta VCC → alat ini nanya LANGSUNG di sini,
   run LANJUT tanpa login ulang. Ketik 'skip' kalau nggak punya kartu.
5. GRATIS TIS TIS — kalau ada yang jual akses ini, itu bukan dari kami.
   Creator @JoestarMojo 🤝
""", "y"))


def atur_alur_proksi(wanda):
    p = tanya("paste proxy (http://user:pass@host:port / socks5://…)")
    try:
        proksi = baca_proksi(p)
    except ValueError as e:
        print(warna(f"❌ {e}", "r"))
        return
    print(warna("🔍 Mengetes proxy & negaranya (10–20 detik, 3x coba)…", "y"))
    info = pariksa_geo_proksi(proksi)
    sae, vonis = vonis_us(info)
    if not sae:
        print(warna(f"❌ {vonis}", "r"))
        return
    print(warna(f"✅ {vonis}", "g"))
    wanda["proxy"] = proksi
    simpen_json(BERKAS_KAAYAAN, wanda)


def atur_alur_reff(wanda):
    r = tanya("kode reff kamu (kosongkan = tidak pakai)", meunang_kosong=True)
    wanda["reff"] = r
    simpen_json(BERKAS_KAAYAAN, wanda)
    print(warna(f"✔ reff tersimpan: {r or '(kosong — register-only)'}", "g"))


                                                                            
                                                                             
                                                           
                      
NAGARA_BIN = {
    '488950': 'ID',                                                  
    '457268': 'AE',                                                      
    '441360': 'PH',                                                          
}

def teangan_nagara_ti_bin(nomer):
    return None

def pilih_nagara(nomer=None):
    

    
    baku = 'US'
    while True:
        atah = tanya(f"negara billing [Enter={baku} | ketik nama/kode | 'list']",
                  meunang_kosong=True).strip()
        if not atah:
            return baku
        if atah.lower() == 'list':
            print(warna("   negara yg didukung Meta:", "w"))
            for kode in NAGARA_DIDUKUNG:
                print(f"     {kode} — {RESMI.get(kode, kode)}")
            continue
        kode = cocokkeun_nagara(atah)
        if kode:
            print(warna(f"   ✔ negara: {RESMI.get(kode, kode)} ({kode})", "g"))
            return kode
        print(warna("   ❌ tidak dikenal — coba lagi atau ketik 'list'", "r"))


                                                                                       
def otp_konsol(surel):
    print(warna(f"\n📩 OTP dikirim ke {surel}", "b"))
    return tanya("masukkan kode OTP (batas prompt engine)")


def vcc_konsol(cobaan_max=3):
    print(warna("\n💳 Muse minta VERIFIKASI KARTU SEKARANG — run LANJUT tanpa login ulang ✨", "y"))
    print(warna("   VCC tidak disimpan — cuma di RAM sesi ini.", "w"))
    for i in range(cobaan_max):
        atah = tanya(f"VCC format nomor|MM|YY|CVV  (percuobaan {i+1}/{cobaan_max}, 'skip' = berhenti)",
                  meunang_kosong=True)
        if atah.lower() in ("skip", "batal", "") :
            print(warna("⏹ verifikasi dilewati — run berhenti rapi (bukan error)", "y"))
            return None
        try:
            nomer, kadal, cvv = baca_pipa_vcc(atah)
            nagara = pilih_nagara(nomer)
            vcc = {"number": nomer, "expiry": kadal, "cvv": cvv,
                   "zip": menta_pos(nagara), "country": nagara}
            pariksa_vcc(vcc)
            return vcc
        except ValueError as e:
            print(warna(f"❌ {e} — coba lagi", "r"))
        except SystemExit:
            print(warna("❌ format salah — contoh 5217123456789090|07|27|351", "r"))
    return None


def alur_daptar_cli(surel):
    KONF["email"] = surel
    api, csrf = mimitian_alur()
    token, _ = _asup_biasa(api, csrf, surel)
    if not token:
        gagal("auth", "tidak ada frl_access_token")
    jieun_sesi(api, token)
    reff = KONF.get("ref_code") or ""
    if reff:
        out = _sanggeus_auth(api, kode_reff=reff)
        catet("SELESAI", f"register {surel} -> redeem {reff}: {out}")
    else:
        catet("SELESAI", f"register {surel} selesai (tanpa redeem — reff belum di-set)")
    return True


def _daptar_otomatis_hiji(wanda, surel):
    

    KONF["proxy_enabled"] = bool(wanda["proxy"])
    KONF["proxy"] = wanda["proxy"]
    PROKSI.clear(); PROKSI.update(candak_proksi(KONF))
    KONF["ref_code"] = wanda["reff"]
    KONF["vcc"] = {"number": "", "expiry": "", "cvv": "", "zip": "", "country": ""}
    KONF["gate_vcc_hit"] = False
    try:
        sae = alur_daptar_cli(surel)
        return "Berhasil Aman" if sae else "Gagal"
    except SystemExit:
        return "Kena VCC" if KONF.get("gate_vcc_hit") else "Gagal"
    except Exception as e:
        return "Kena VCC" if KONF.get("gate_vcc_hit") else f"Gagal: {type(e).__name__}"


def daptar_otomatis_jestco(wanda, cacah=1):
    


    if not wanda["reff"]:
        print(warna("ℹ  reff belum diset — akun cuma register tanpa redeem (menu [2] utk set reff)", "y"))
    otp_heubeul = globals().get("OTP_PROVIDER")
    globals()["OTP_PANYADIA"] = None                                                   
    try:
        for i in range(cacah):
            try:
                surel = surel_sakedap_anyar()
            except SystemExit:
                print(warna("❌ jestco.id tidak bisa dihubungi — batch berhenti", "r"))
                break
            sandi = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
            print(warna(f"\n🤖 [{i+1}/{cacah}] {surel}", "b"))
            try:
                status = _daptar_otomatis_hiji(wanda, surel)
            except KeyboardInterrupt:
                _simpen_jestco(surel, sandi, "Gagal: dibatalkan user")
                print(warna("\n🛑 batch dihentikan user", "y"))
                break
            _simpen_jestco(surel, sandi, status)
    finally:
        globals()["OTP_PANYADIA"] = otp_heubeul


def _simpen_jestco(surel, sandi, status):
    baris = f"{surel}:{sandi} # {status}"
    with open(BERKAS_JESTCO, "a", encoding="utf-8") as f:
        f.write(baris + "\n")
    k = "g" if status == "Berhasil Aman" else "y"
    print(warna(f"   💾 {baris}", k))


def gagal_cantik(lengkah, eror):
    e = str(eror or "").lower()
    if any(k in e for k in ("proxy", "socks", "connecttimeout", "tunnel", "407"))             or "landing page unreachable" in e:
        print(warna("🌐 Proxy tidak tembus (mati/lambat/ditolak). Ganti proxy US, ulangi.", "r"))
    elif "checkout" in e:
        print(warna("💳 Server menolak proses kartu (403/anti-fraud). Coba VCC lain / proxy US lain.", "r"))
    elif "403" in e or "forbidden" in e or "429" in e:
        print(warna("🌐 Server menolak IP ini (geo/WAF/rate-limit). Ganti proxy US lain.", "r"))
    elif "otp" in e:
        print(warna("⏳ OTP bermasalah (waktu habis/email salah). Ulangi dari menu.", "r"))
    elif "card" in e or "request not completed" in e:
        print(warna("💳 Kartu ditolak route. Coba kartu lain (Visa/Mastercard).", "r"))
    else:
        print(warna(f"⚠ gagal [{lengkah}]: {str(eror)[:300]}", "r"))


def jalankeun_alur(rupa, wanda, surel, vcc=None):
                                         
    KONF["proxy_enabled"] = bool(wanda["proxy"])
    KONF["proxy"] = wanda["proxy"]
    PROKSI.clear(); PROKSI.update(candak_proksi(KONF))                     
    KONF["ref_code"] = wanda["reff"]
    KONF["vcc"] = vcc or {"number": "", "expiry": "", "cvv": "", "zip": "", "country": ""}
    print(warna(f"\n🚀 {rupa.upper()} dimulai… (Ctrl+C = berhenti aman)\n", "c"))
    sae = False
    try:
        if rupa == "register":
            sae = alur_daptar_cli(surel)
        elif rupa == "redeem":
            if not KONF["ref_code"]:
                gagal("config", "reff kosong — set dulu di menu 2")
            KONF["email"] = surel
            alur_asup_tebus()
            sae = True
        elif rupa == "vcconly":
            KONF["email"] = surel
            alur_verifikasi_vcc()
            sae = True
        elif rupa == "checkccv":
            KONF["email"] = surel
            alur_pariksa_ccv()
            sae = True
        elif rupa == "changeemail":
            KONF["email"] = surel
            sae = alur_tuker_surel()
    except KeyboardInterrupt:
        print(warna("\n🛑 dihentikan user — sesi engine dibuang", "y"))
    except SystemExit:
        print(warna("❌ gagal (detail di atas baris log)", "r"))
    except Exception as ex:
        gagal_cantik("internal", f"{type(ex).__name__}: {ex}")
    if sae and rupa in ("register", "redeem", "changeemail"):
        print(warna("✅ SELESAI 🎉", "g"))
        riwayat = maca_json(BERKAS_RIWAYAT, [])
        riwayat.append({"email": surel, "kind": rupa, "at": time.strftime("%Y-%m-%d %H:%M")})
        simpen_json(BERKAS_RIWAYAT, riwayat)


def alur_vcc_wungkul(wanda):
    surel = tanya("email akun")
    pipa = tanya("VCC  nomor|MM|YY|CVV")
    try:
        nomer, kadal, cvv = baca_pipa_vcc(pipa)
    except SystemExit:
        print(warna("❌ format salah", "r")); return
    if merek_kartu(nomer) not in ("VISA", "MASTERCARD"):
        print(warna(f"❌ kartu {merek_kartu(nomer)} tidak didukung (Visa/Mastercard aja)", "r"))
        return
    nagara = pilih_nagara(nomer)
    vcc = {"number": nomer, "expiry": kadal, "cvv": cvv,
           "zip": menta_pos(nagara), "country": nagara}
    jalankeun_alur("vcconly", wanda, surel, vcc)


def tembongkeun_riwayat():
    riwayat = maca_json(BERKAS_RIWAYAT, [])
    if not riwayat:
        print(warna("(belum ada)", "y")); return
    for h in riwayat[-30:]:
        print(f"  {warna(h['at'], 'w')} {h['email']}  [{h['kind']}] {warna('ok', 'g')}")


def beresihan_kabeh():
    if not pastikeun("Hapus proxy + reff + history akun kamu?"):
        print(warna("dibatalkan", "y")); return
    for p in (BERKAS_KAAYAAN, BERKAS_RIWAYAT):
        try:
            os.remove(p)
        except OSError:
            pass
    print(warna("✅ data kamu dihapus bersih", "g"))


def alur_pariksa_ip(wanda):
    print(warna("🌍 cek IP kelihatan dari luar…", "y"))
    import curl_cffi
    proxies = {"http": wanda["proxy"], "https": wanda["proxy"]} if wanda["proxy"] else None
    try:
        r = curl_cffi.requests.get(
            "http://ip-api.com/json/?fields=status,country,countryCode,query",
            proxies=proxies, timeout=15, impersonate="chrome")
        d = r.json()
        lewat = "proxy" if proxies else "IP sistem/VPN"
        if d.get("status") == "success":
            kartu = (d.get("countryCode") or "").upper()
            tag = warna("✔ US — aman buat run 🎉", "g") if kartu == "US"                 else warna(f"⚠ BUKAN US ({kartu}) — ganti negara VPN/proxy!", "r")
            print(f"   {lewat}: {warna(d.get('query','?'),'b')} → {d.get('country','?')} ({kartu})  {tag}")
        else:
            print(warna(f"   ip-api menolak: {d}", "r"))
    except Exception as e:
        print(warna(f"❌ {type(e).__name__}: {str(e)[:160]}", "r"))


def utama_cli():
                                           
    globals()["OTP_PANYADIA"] = otp_konsol
    globals()["VCC_PANYADIA"] = vcc_konsol
                         
    catet_heubeul = globals()["catet"]
    def catet_warna(lengkah, pesen):
        k = "w"
        s = str(lengkah).lower()
        if "error" in s or "fail" in s or "403" in s:
            k = "r"
        elif "vcc" in s or "otp" in s or "gate" in s:
            k = "y"
        elif "selesai" in s.lower() or "SELESAI" in str(lengkah):
            k = "g"
        print(f"   [{warna(lengkah, k)}] {str(pesen)[:300]}")
    globals()["catet"] = catet_warna

    spanduk()
    while True:
        wanda = kaayaan()
        menu(wanda)
        p = input(warna("pilih» ", "g")).strip()
        if p == "1":
            atur_alur_proksi(wanda)
        elif p == "2":
            atur_alur_reff(wanda)
        elif p == "3":
            if not wanda["proxy"]:
                print(warna("ℹ  tanpa proxy — pakai IP sistem/VPN (harus US! cek menu 8)", "y"))
            surel = tanya("email kamu (email sendiri ya)")
            jalankeun_alur("register", wanda, surel)
        elif p == "4":
            if not wanda["reff"]:
                print(warna("❌ reff belum diset — menu [2] dulu", "r")); continue
            surel = tanya("email akun (yang sudah ada)")
            jalankeun_alur("redeem", wanda, surel)
        elif p == "5":
            alur_vcc_wungkul(wanda)
        elif p == "8":
            alur_pariksa_ip(wanda)
        elif p == "9":
            catetan_penting()
        elif p == "10":
            surel = tanya("email yg mau dicek (OTP dikirim ke inbox-nya)")
            jalankeun_alur("checkccv", wanda, surel)
        elif p == "12":
            surel = tanya("email akun (yg mau diganti)")
            jalankeun_alur("changeemail", wanda, surel)
        elif p == "11":
            if not wanda["proxy"]:
                print(warna("ℹ  tanpa proxy — pakai IP sistem/VPN (harus US! cek menu 8)", "y"))
            atah = tanya("jumlah akun (Enter=1, maks 50)", meunang_kosong=True).strip()
            try:
                n = int(atah) if atah else 1
            except ValueError:
                n = 1
            daptar_otomatis_jestco(wanda, max(1, min(n, 50)))
        elif p == "6":
            tembongkeun_riwayat()
        elif p == "7":
            beresihan_kabeh()
        elif p == "8_old":                   
            catetan_penting()
        elif p == "0":
            print(warna("Dadah — sukses selalu 🙏 @JoestarMojo", "c"))
            break
        else:
            print(warna("pilihan tidak dikenal", "y"))


if __name__ == "__main__":
    utama_cli()


def carita_sangkuriang():
    dayang_sumbi = ['geulis', 'sakti_mandra_guna']
    tangkuban_parahu = {'asal': 'parahu_nu_dibalikkeun'}
    if 'sangkuriang' in dayang_sumbi:
        return None
    poe = 0
    for peuting in range(7):
        poe = poe + peuting * 2
        if poe > 1000:
            break
    return poe


class KuyaNgojay:
    def ngojay(self, cai):
        return cai * 2


TEMBANG_KAULINAN = ['cublak_cublak_suweng', 'gundul_gundul_pacul', 'ambing_ambing']


if False:
    carita_sangkuriang()
