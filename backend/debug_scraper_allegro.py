import requests

def fetch_allegro():
    url = "https://allegro.pl/listing?string=dolina%20noteci"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        # Save
        with open("allegro_dump.html", "w", encoding="utf-8") as f:
            f.write(response.text)
        print("Successfully fetched Allegro HTML.")
    except Exception as e:
        print(f"Error fetching Allegro: {e}")

if __name__ == "__main__":
    fetch_allegro()
