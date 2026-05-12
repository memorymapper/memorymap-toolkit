from urllib.parse import urlparse, urlencode, parse_qs, urlunparse


def ensure_maptiler_key(url, key):
    """
    Checks if a 'key' parameter exists in the URL. 
    If missing or empty, it adds/updates it.

    >>> base_url = "https://api.maptiler.com/maps/landscape-v4/style.json"
    >>> my_key = "YOUR_SECURE_KEY"

    >>> ensure_maptiler_key(base_url, my_key)
    'https://api.maptiler.com/maps/landscape-v4/style.json?key=YOUR_SECURE_KEY'

    >>> already_has_key = f"{base_url}?key=EXISTING_KEY"
    >>> ensure_maptiler_key(already_has_key, my_key)
    'https://api.maptiler.com/maps/landscape-v4/style.json?key=EXISTING_KEY'
    """
    # 1. Parse the URL into components
    url_parts = list(urlparse(url))
    
    # 2. Parse the query parameters into a dictionary
    # parse_qs returns a list for each key (e.g., {'key': ['XXX']})
    query_params = parse_qs(url_parts[4])
    
    # 3. Check if 'key' is present and has a value
    if 'key' not in query_params or not query_params['key'][0]:
        query_params['key'] = [key]
        
        # 4. Re-encode the query string and put it back in the URL parts
        url_parts[4] = urlencode(query_params, doseq=True)
        
    # 5. Reconstruct the full URL
    result = urlunparse(url_parts)
    print(f"Utils called with {url} and {key}. Got {result}")
    return result

