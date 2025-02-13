import requests
import time
import os
import json

CONFIG_FILE = "config.json"
DB_FILE = "data/db.json"

def ensure_file_exists(file_path, default_content):
    dir_name = os.path.dirname(file_path)
    if dir_name and not os.path.exists(dir_name):
        os.makedirs(dir_name, exist_ok=True)
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            json.dump(default_content, f, indent=4)

ensure_file_exists(CONFIG_FILE, {
    "api_token": "your_cloudflare_api_token",
    "zone_id": "your_zone_id",
    "record_name": "your.domain.com",
    "update_interval": 30
})

def load_config():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

config = load_config()
API_TOKEN = config["api_token"]
ZONE_ID = config["zone_id"]
RECORD_NAME = config["record_name"]
UPDATE_INTERVAL = config["update_interval"]

def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json")
        response.raise_for_status()
        return response.json()["ip"]
    except requests.RequestException as e:
        print(f"Error fetching public IP: {e}")
        return None

def get_dns_record():
    url = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records"
    headers = {"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"}
    params = {"name": RECORD_NAME, "type": "A"}
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        records = response.json()["result"]
        return records[0] if records else None
    except requests.RequestException as e:
        print(f"Error fetching DNS record: {e}")
        return None

def update_dns_record(record_id, ip):
    url = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/{record_id}"
    headers = {"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"}
    data = {"type": "A", "name": RECORD_NAME, "content": ip, "ttl": 1, "proxied": False}
    try:
        response = requests.put(url, headers=headers, json=data)
        response.raise_for_status()
        if response.json()["success"]:
            print(f"DNS record updated successfully to {ip}.")
        else:
            print(f"Failed to update DNS record: {response.json()}")
    except requests.RequestException as e:
        print(f"Error updating DNS record: {e}")

def read_saved_ip():
    with open(DB_FILE, "r") as f:
        return json.load(f).get("ip", "")

def save_ip(ip):
    with open(DB_FILE, "w") as f:
        json.dump({"ip": ip}, f, indent=4)

def main():
    current_ip = get_public_ip()
    if not current_ip:
        print("Could not fetch the initial public IP. Exiting.")
        return

    print(f"Current public IP: {current_ip}")
    saved_ip = read_saved_ip()
    if saved_ip == current_ip:
        print(f"IP is already up-to-date: {current_ip}")
    else:
        dns_record = get_dns_record()
        if not dns_record:
            print("DNS record not found. Exiting.")
            return
        
        record_id = dns_record["id"]
        print(f"IP has changed or no IP saved. Updating DNS record...")
        update_dns_record(record_id, current_ip)
        save_ip(current_ip)

    while True:
        new_ip = get_public_ip()
        if new_ip and new_ip != current_ip:
            print(f"IP changed from {current_ip} to {new_ip}. Updating DNS record...")
            update_dns_record(record_id, new_ip)
            save_ip(new_ip)
            current_ip = new_ip
        time.sleep(UPDATE_INTERVAL)

if __name__ == "__main__":
    main()