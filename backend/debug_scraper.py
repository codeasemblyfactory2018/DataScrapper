import requests
import sys

def fetch_ceneo():
    url = "https://www.ceneo.pl/;szukaj-dolina+noteci"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Save a portion of the HTML to analyze structure
        with open("ceneo_dump.html", "w", encoding="utf-8") as f:
            f.write(response.text)
        print("Successfully fetched Ceneo HTML.")
    except Exception as e:
        print(f"Error fetching Ceneo: {e}")

if __name__ == "__main__":
    fetch_ceneo()
