from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import hashlib
import subprocess
import time
import os


def download_content(url):
    response = requests.get(url)
    return response.content


def compute_hash(content):
    return hashlib.sha256(content).hexdigest()


def analyze_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    contents = soup.find("div", {"id": div_id})
    return contents.text.encode("utf-8")


load_dotenv()
page_url = os.getenv("URL")
div_id = os.getenv("DIV_ID")

url = page_url  # Sostituisci con l'URL della pagina che vuoi monitorare
past_hash = None

while True:
    html = download_content(url)
    div = analyze_page(html)
    print(div)
    actual_hash = compute_hash(div)

    if actual_hash != past_hash:
        print("The page is changed")

        past_hash = actual_hash
        subprocess.run(
            ["notify-send", "-u", "normal", "-t", "3000",
             "[WARNING] Page changed", "Your description"],
            check=True)
    else:
        print("The page hasn't changed")
        subprocess.run(
            ["notify-send", "-u", "normal", "-t", "3000",
             "Page hasn't changed", "Your description"],
            check=True)

    time.sleep(60)
