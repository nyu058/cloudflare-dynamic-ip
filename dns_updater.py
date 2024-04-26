import requests
import CloudFlare
import os
import time
from dotenv import load_dotenv
import logging
import argparse

logging.basicConfig( 
            format='%(asctime)s %(levelname)-8s %(message)s',
            level=logging.INFO,
            datefmt='%Y-%m-%d %H:%M:%S')


load_dotenv()

ZONE_ID = os.environ.get("ZONE_ID")

CF_API_TOKEN = os.environ.get("CF_API_TOKEN")

cf = CloudFlare.CloudFlare(token=CF_API_TOKEN)

def update_dns_records(record_names):
    """updates the cloudflare dns records given in record_names to the current ip address"""
    myip = requests.get('http://checkip.amazonaws.com').text.rstrip()
    logging.info(f"Current ip is {myip}")
    try:
        dns_records = cf.zones.dns_records.get(ZONE_ID)
    except CloudFlare.exceptions.CloudFlareAPIError as e:
        logging.error(f"Failed to fetch DNS Record: {e}")

    for record in dns_records:
        name = record["name"]
        if name in record_names:
            if record["content"] != myip:
                # update record to match current ip if different
                record_id = record["id"]
                body = {"content": myip,
                        "name":name,
                        "type":record["type"]}
                try:
                    cf.zones.dns_records.patch(ZONE_ID, record_id, data=body)
                    logging.info(f"Updated DNS record {name} to new ip {myip}")

                except CloudFlare.exceptions.CloudFlareAPIError as e:
                    logging.error(f"Failed to update DNS Record: {e}")
            else:
                logging.info(f"DNS record {name} is not changed")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Cloudflare dns updater')

    parser.add_argument('-i', '--interval', nargs='?', type=int, default=600,
                        help="specifies how ofter the dns record is checked")
    
    parser.add_argument('records', nargs='+', metavar='RECORDS',
                        help="list of dns record names to be updated")

    args = parser.parse_args()
    names = vars(args)["records"]
    interval = vars(args)["interval"]
    logging.info(f"DNS records will be checked every {interval} seconds")
    while 1:
        
        update_dns_records(names)
        time.sleep(interval)
