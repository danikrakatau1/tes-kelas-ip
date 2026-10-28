#!/usr/bin/env python3
"""
Dahl API Automation Script - Batch Mode
Generate multiple accounts with fingerprint + API key
"""

import requests
import json
import random
import time
from datetime import datetime

DAHL_BASE = "https://inference.dahl.global/v1"
RESULTS_FILE = "C:/Users/user/dahl_accounts.json"

def generate_username():
    words = ['quantum', 'cosmo', 'pixel', 'stellar', 'nebula', 'orbit', 'nova', 'astral', 'cosmic', 'solar',
             'drift', 'flare', 'ember', 'frost', 'glint', 'quake', 'river', 'storm', 'tide', 'vex']
    adjs = ['bold', 'wild', 'dark', 'bright', 'swift', 'iron', 'frozen', 'shadow', 'storm', 'swift']
    nums = random.randint(100, 999)
    return f"{random.choice(words)}_{random.choice(adjs)}_{nums}"

def signup(username, max_retries=3):
    for attempt in range(max_retries):
        r = requests.post(f"{DAHL_BASE}/auth/signup", json={"username": username}, timeout=15)
        if r.status_code in [200, 201]:
            return r.json()
        elif r.status_code == 429:
            wait = 60  # Wait 1 minute on rate limit
            print(f"Rate limited. Waiting {wait}s... (attempt {attempt+1}/{max_retries})")
            time.sleep(wait)
            continue
        print(f"Signup failed: {r.status_code}")
        return None
    return None

def allocate_tokens(fingerprint, key_id):
    session = requests.Session()
    r = session.post(f"{DAHL_BASE}/auth/signin", json={"fingerprint": fingerprint}, timeout=15)
    if r.status_code != 200:
        print(f"Signin failed: {r.status_code}")
        return False
    
    r = session.post(f"{DAHL_BASE}/account/allocate", 
                     json={"key_id": key_id, "amount": 100000000}, timeout=15)
    
    if r.status_code in [200, 201]:
        print(f"[+] Allocated 100M tokens!")
        return True
    print(f"Allocate failed: {r.status_code}")
    return False

def test_api(api_key):
    r = requests.post(f"{DAHL_BASE}/chat/completions",
                     json={"model": "MiniMaxAI/MiniMax-M2.7",
                           "messages": [{"role": "user", "content": "Hello"}]},
                     headers={"Authorization": f"Bearer {api_key}"}, timeout=30)
    return r.status_code == 200

def create_account():
    print(f"\n[*] Creating account {datetime.now().strftime('%H:%M:%S')}...")
    
    username = generate_username()
    print(f"[*] Username: {username}")
    
    result = signup(username)
    if not result:
        return None
    
    user = result.get('user', {})
    fingerprint = result.get('fingerprint', 'NOT_FOUND')
    api_key_info = result.get('api_key', {})
    api_key = api_key_info.get('token', 'NOT_FOUND')
    key_id = api_key_info.get('id')
    
    print(f"[+] User: {user.get('user_id')[:20]}...")
    print(f"[+] Fingerprint: {fingerprint}")
    print(f"[+] API Key: {api_key}")
    
    if key_id:
        allocate_tokens(fingerprint, key_id)
    
    if test_api(api_key):
        print(f"[+] API TEST: SUCCESS")
    else:
        print(f"[-] API TEST: FAILED")
    
    return {"username": username, "fingerprint": fingerprint, "api_key": api_key}

def main(count=5):
    print(f"[*] Dahl API Automation - Creating {count} accounts")
    
    # Load existing accounts
    existing = []
    try:
        with open(RESULTS_FILE, 'r') as f:
            existing = json.load(f)
        print(f"[*] Loaded {len(existing)} existing accounts")
    except:
        pass
    
    accounts = existing.copy()
    for i in range(count):
        account = create_account()
        if account:
            accounts.append(account)
        
        # Wait between accounts to avoid rate limits
        if i < count - 1:
            wait_time = 15
            print(f"[*] Waiting {wait_time}s before next account...")
            time.sleep(wait_time)
    
    # Save results
    with open(RESULTS_FILE, 'w') as f:
        json.dump(accounts, f, indent=2)
    
    print(f"\n[AUTO-GUARD] COMPLETE! Created {len(accounts)} total accounts")
    print(f"[AUTO-GUARD] Results saved to: {RESULTS_FILE}")
    
    return accounts

if __name__ == "__main__":
    results = main(5)
    for acc in results:
        print(f"\n{acc['username']}: {acc['api_key']}")