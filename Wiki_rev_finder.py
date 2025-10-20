import sys
import requests

url = "https://en.wikipedia.org/w/api.php"

def fetch_rev(name):
    headers = {"User-Agent": "wiki-recent-script/1.0"}

    try:
        response = requests.get(url,params={
                "action": "query",
                "format": "json",
                "prop": "revisions",
                "titles": name,
                "rvprop": "timestamp|user",
                "rvlimit": "30",
                "rvdir": "newer",
                "redirects": 1,
            },
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        return response.json()

    except requests.RequestException as e:
        print(f"Error fetching data for {name}: {e}", file=sys.stderr)
        sys.exit(3)


def process_response(data):
     query = data.get("query", {})

     ###Rediredct Handling###
     redirected_to = None
     if "redirects" in query:
         redirected_to = query["redirects"][0]["to"]
         print(f"Note: Page was redirected to '{redirected_to}'")

     ###Missing Page Handling###
     pages = query.get("pages", {})
     if not pages:
            print("Error: No pages found in the response.", file=sys.stderr)
            sys.exit(2)
     page = next(iter(pages.values()))
     if "missing" in page:
            print("Error: The requested page does not exist.", file=sys.stderr)
            sys.exit(2)
        
     ###Get Revisions + In Case Page Has No Revisions###
     revisions = page.get("revisions", [])
     if not revisions:
            print("Error: No revisions found for the page.", file=sys.stderr)
            return
     ###Displaying Revisions###
     for rev in revisions:
            timestamp = rev.get("timestamp")
            user = rev.get("user")
            if timestamp and user:
                print(f"{timestamp} {user}")

def main():
     ###If No Arguments Provided###
     if len(sys.argv) < 2:
            print("No Article Provided.", file=sys.stderr)
            sys.exit(1)
     article_name = " ".join(sys.argv[1:]).strip()
     if not article_name:
            print("No Article Provided.", file=sys.stderr)
            sys.exit(1)
     data = fetch_rev(article_name)
     process_response(data)
     sys.exit(0)

if __name__ == "__main__":
     main()
     

     
     

    
         