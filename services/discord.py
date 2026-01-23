import requests
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime


def send_discord_notification(job_title, company, job_url, webhook_urls, user, force_save=False):
    """"Send a Discord notification about the new job posting."""

    # Create the embed payload
    timestamp = datetime.utcnow().isoformat()

    data = {
        "username": "Job Alerts",
        "avatar_url": "https://i.imgur.com/4M34hi2.png",
        "embeds": [
            {
                "title": job_title,
                "url": job_url,
                "color": 0x00B894,
                "fields": [
                    {"name": "Company", "value": company, "inline": True},
                    {"name": "Posted By", "value": user, "inline": True},
                    {"name": "Force Saved", "value": "⚠️ Yes" if force_save else "No", "inline": True},
                ],
                "footer": {"text": "CodeHealers · Job Alerts", "icon_url": "https://i.imgur.com/4M34hi2.png"},
                "timestamp": timestamp
            }
        ]
    }

    # Function to send the request
    def send(webhook_url):
        """"Send a POST request to the Discord webhook URL."""
        res = requests.post(webhook_url, json=data)
        if res.status_code != 204:
            print(f"Failed: {res.status_code} {res.text}")

    # Use ThreadPoolExecutor to send requests concurrently
    with ThreadPoolExecutor() as executor:
        executor.map(send, webhook_urls)
