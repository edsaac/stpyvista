import requests


def get_ipyfi():
    """
    Returns client's IP by making a request to ipyfi.org
    """
    r = requests.get("https://api.ipify.org?format=json")
    return r.json().get("ip", "__not_found__") if r.status_code == 200 else "__failed"
