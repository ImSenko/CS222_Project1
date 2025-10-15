import sys
import requests

API_URL = "https://en.wikipedia.org/w/api.php"

###Getting Wikipedia Revisions###
def fetch_wikipedia_rev(article_name):
    headers = {
        "User-Agent": "WikiEditsBot/1.0 (your_email@example.com)"
    }

    try:
        response = requests.get(API_URL, params={
            "action": "query",
            "format": "json",
            "prop": "revisions",
            "titles": article_name,
            "rvprop": "timestamp|user",
            "rvlimit": 30,
            "redirects": 1
        }, headers=headers, timeout=10)

        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"A network error occurred: {e}")
        sys.exit(3)

def process_response(data):
    ###Process API response and print revisions or handle errors.###
    # Handle redirects
    redirected_to = None
    if "redirects" in data.get("query", {}):
        redirected_to = data["query"]["redirects"][0]["to"]
        print(f"Redirected to {redirected_to}")

    # Get page data
    pages = data.get("query", {}).get("pages", {})
    if not pages:
        print("The specified Wikipedia article was not found.")
        sys.exit(2)