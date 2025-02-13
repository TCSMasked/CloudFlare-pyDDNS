# CloudFlare pyDDNS
CloudFlare pyDDNS is a lightweight, Python-based Dynamic DNS (DDNS) updater designed to automatically update a CloudFlare DNS A record with the current public IP address of your machine. This is useful for keeping a domain or subdomain pointed to a dynamic home IP address.

## Features
- **Automatic IP Detection:** Fetches the current public IP address.

- **CloudFlare API Integration:** Updates CloudFlare DNS records seamlessly.

- **Persistent Storage:** Saves the last known IP address to prevent unnecessary updates.

- **Docker Support:** Easily deployable as a Docker container.

- **Logging & Error Handling:** Provides clear error messages and logs updates.

## Prerequisites
- Python 3.8+

- A Cloudflare API token with DNS edit permissions

- Docker (**optional**, for containerized deployment)

## Installation & Usage
### 1. Clone the Repository
```sh
git clone https://github.com/tcsmasked/cloudflare-pyddns.git
cd cloudflare-pyddns
```

### 2. Install Dependencies
```
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Set up your Cloudflare credentials in the config.json file:

```
API_TOKEN=your_cloudflare_api_token
ZONE_ID=your_zone_id
RECORD_NAME=your_dns_record_name
UPDATE_INTERVAL=30
```

### 4. Run the Script
```
python ddns_updater.py
```

## Running with Docker
### 1. Build the Docker Image
```
docker build -t cloudflare-pyddns .
```

### 2. Run the container
```
docker run -d \
  --name cloudflare-pyddns \
  -v /path/to/local/storage:/app/data \
  --restart=always \
  cloudflare-pyddns
```

## How it works
- The script fetches the current public IP.
- It checks the last saved IP from current_ip.txt to avoid redundant updates.
- If the IP has changed, it updates the Cloudflare A record.
- The new IP is saved, and the process repeats at the defined interval.

## Logs & Monitoring
To view live logs from Docker:
```
docker logs -f cloudflare-pyddns
```

## 🌐 Contributions & Issues
Feel free to fork this repository and submit pull requests! If you encounter any issues, open an issue on GitHub.

🚀 Happy hosting!