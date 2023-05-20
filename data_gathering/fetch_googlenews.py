
from pygooglenews import GoogleNews



def fetch_googlenews():
    """Fetch data from google news."""
    gn = GoogleNews()
    business = gn.search('crypto')
    return business["entries"]