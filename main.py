import requests

def size_of():
    with open("text.txt") as f:
        contents = f.read()
    return len(contents)

def google_query(query):
    url = "https://www.google.com"
    params = {'q': query}
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.content