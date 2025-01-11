import os
import time
import logging
import requests
from apprise import Apprise

# ----------------------------
# Configuration and Logging
# ----------------------------
VERSION = "0.1.2"

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Notifications via Apprise
apprise = Apprise()
apprise_urls = os.getenv("APPRISE_URLS", "").split(",")
for url in apprise_urls:
    if url:
        apprise.add(url.strip())


def send_notification(message):
    """
    Send a notification using Apprise.
    """
    if apprise.servers:
        apprise.notify(title="IP Monitor", body=message)
        logging.info("Notification sent successfully.")
    else:
        logging.warning("No Apprise notification services configured.")


# ----------------------------
# Public IP Monitoring
# ----------------------------
current_public_ip = None
failure_count = 0
MAX_FAILURES = int(
    os.getenv("MAX_FAILURES", 3)
)  # Max consecutive failures before notifying
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 60))


def get_public_ip():
    """
    Fetch the current public IP address.
    """
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=10)
        response.raise_for_status()
        return response.json().get("ip")
    except requests.RequestException as e:
        logging.error(f"Error fetching public IP: {e}")
        return None


def monitor_public_ip():
    """
    Monitor public IP address and send notifications on changes or failures.
    """
    global current_public_ip, failure_count
    logging.info(f"Starting ipmonitor version {VERSION}")

    while True:
        new_ip = get_public_ip()

        if new_ip:
            if failure_count > 0:
                logging.info("IP check recovered after failure.")
                send_notification(
                    "IP Monitor recovered: Successfully fetched public IP."
                )
                failure_count = 0  # Reset failure count after recovery

            if current_public_ip is None:
                current_public_ip = new_ip
                logging.info(f"Initial public IP detected: {current_public_ip}")
                send_notification(
                    f"ipmonitor started up. Initial public IP detected: {current_public_ip}"
                )
            elif new_ip != current_public_ip:
                logging.info(f"Public IP changed from {current_public_ip} to {new_ip}")
                send_notification(
                    f"Public IP changed from {current_public_ip} to {new_ip}"
                )
                current_public_ip = new_ip

        else:
            failure_count += 1
            logging.warning(
                f"Failed to fetch public IP. Consecutive failures: {failure_count}"
            )

            if failure_count >= MAX_FAILURES:
                logging.error(
                    "Max consecutive IP check failures reached. Sending notification."
                )
                send_notification(
                    f"IP Monitor Warning: Failed to fetch public IP for {failure_count} consecutive attempts."
                )
                failure_count = 0  # Reset after sending failure notification

        logging.info(f"Waiting for the next check in {CHECK_INTERVAL}...")
        time.sleep(CHECK_INTERVAL)


# ----------------------------
# Application Entry Point
# ----------------------------
if __name__ == "__main__":
    monitor_public_ip()
