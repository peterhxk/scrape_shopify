import re
import time
from datetime import datetime
import requests
import send_email

URL = "https://internships.shopify.com/"

NEEDLE = "Internship applications are now closed - check back on December 19, 2025 for Summer 2026 applications"

def page_has_closed_banner(html: str) -> bool:
    
    # Save HTML content to file
    with open("website.html", "w", encoding="utf-8") as f:
        f.write(html)

    return NEEDLE in html

def main():
    while True:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            r = requests.get(URL, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
            r.raise_for_status()

            closed = page_has_closed_banner(r.text)

            if not closed:
                print("🚨 CLOSED banner NOT found — likely open or page changed!")
                send_email.send_email(
                    subject="Shopify Internship Update 🚨",
                    body="The internship applications page has changed! gogogo https://internships.shopify.com/"
                )
            else:
                print(f"{current_time}: Still closed banner present.")
        except Exception as e:
            print(f"{current_time}: Error occurred: {e}")

        time.sleep(300)

if __name__ == "__main__":
    main()
