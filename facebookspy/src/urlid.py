from urllib.parse import urlparse


def get_account_id(url: str) -> str:
    """
    Function to extract facebook account id from the given url
    """
    parsed_url = urlparse(url)
    path = parsed_url.path.strip("/")
    parts = path.split("/")
    account_name = parts[-1] if parts else None
    return account_name
