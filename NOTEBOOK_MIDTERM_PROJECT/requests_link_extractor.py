from bs4 import BeautifulSoup
import requests
import re


# This is the main sitemap URL for Vogue
# https://www.vogue.com/sitemap.xml
# This is an example URL for a specific year, month, and week in the Vogue sitemap
# https://www.vogue.com/sitemap.xml?year=2023&month=11&week=4


# This is the main sitemap URL for Glamour
#  https://www.glamour.com/sitemap.xml
# This is an example URL for a specific year, month, and week in the Glamour sitemap
# https://www.glamour.com/sitemap.xml?year=2023&month=11&week=4

# Note: All extracted links are expected to belong to the year 2023
from bs4 import BeautifulSoup
import requests
import re

"""
    This module provides functions to extract sublinks using GET requests from the sitemaps listed in the robots.txt file of various websites, such as "Vogue" and "Glamour". The functions are designed for web scraping purposes, utilizing the requests library.

    Usage:
    - Call the get_links_using_requests function with the desired website name to obtain a dictionary of links grouped by brand.

    Example:
    get_links_using_requests("vogue")
"""


def get_soup(url, existing_links):
    """
    Make a GET request to the URL and return a dictionary of sublinks containing the specified keywords ("louis-vuitton", "chanel", "dior", "versace") grouped by brand.

    Parameters:
    - url (str): The URL to which the request will be made.
    - existing_links (dict): The existing dictionary of links to be updated.

    Returns:
    - Dict[brand, List[str]]: A dictionary of links grouped by brand containing the specified keywords.
    """

    # Define request headers to mimic a browser request
    request_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    # Make the GET request
    response = requests.get(url, headers=request_headers)

    if response.status_code == 200:
        # Process the XML content
        soup = BeautifulSoup(response.text, 'xml')
        # Keywords to search for in the sublinks
        keywords = ["louis-vuitton", "chanel", "dior", "versace"]

        # Dictionary of sublinks for each brand
        links_by_keyword = {keyword: [loc.text for loc in soup.find_all(
            "loc") if re.search(keyword, loc.text)] for keyword in keywords}

        # Update the existing dictionary with new links
        for keyword in links_by_keyword:
            existing_links[keyword].extend(links_by_keyword[keyword])

        return existing_links
    else:
        # If the request is not successful, return the existing links
        return existing_links


def get_links_using_requests_by_brands(website):
    """
    Use the sitemap link of the website to extract the required sublinks (from April to November 2023) for each brand ("louis-vuitton", "chanel", "dior", "versace").

    Parameters:
    - website (str): The name of the website for which links will be extracted.

    Returns:
    - Dict[brand, List[str]]: A dictionary of links for each brand meeting specific criteria.
    """

    website = website.lower()

    # Keywords to search for in the sublinks
    keywords = ["louis-vuitton", "chanel", "dior", "versace"]
    final_sublinks = {keyword: [] for keyword in keywords}

    # Iterate over months (April to November inclusive)
    for month in range(1, 12):
        # Iterate over weeks (0 to 5 inclusive)
        for week in range(6):
            # Construct the URL for the sitemap
            link = f"https://www.{website}.com/sitemap.xml?year=2023&month={
                month}&week={week}"
            # Get sublinks for the current week
            get_soup(link, final_sublinks)

    return final_sublinks


def get_links_using_requests(website):
    """
    Use the sitemap link of the website to extract the required sublinks (from April to November 2023) for each brand ("louis-vuitton", "chanel", "dior", "versace").

    Parameters:
    - website (str): The name of the website for which links will be extracted.

    Returns:
    - Dict[brand, List[str]]: A dictionary of links for each brand.
    """
    return get_links_using_requests_by_brands(website)


__all__ = ['get_links_using_requests']

# # Example usage
# print(get_links_using_requests("vogue"))
