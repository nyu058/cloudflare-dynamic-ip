# cloudflare-dns
Script to check cloudflare DNS record for non-static ips. If the local IP is different than cloudflare, update cloudflare with the current IP.

## Usage
The following environment variables are required:
```
export ZONE_ID=<your dns zone id>
export CF_API_TOKEN=<your cloudflare api token>
```

To check the DNS record of example.com and www.example.com every 300 seconds
```
python dns_updater.py -i 300 example.com www.example.com
```

## Docker
An docker image is available:

```
docker run ghcr.io/nyu058/cloudflare-dynamic-ip -i 300 example.com www.example.com
```

## Kubernetes
Checkout `k8s-example.yaml` for an example kubernetes deployment 