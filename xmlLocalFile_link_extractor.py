from bs4 import BeautifulSoup
import re

# This is the main sitemap URL for Elle
# https://www.elle.com/sitemap_index.xml
# This is an example URL for a compressed file containing links for the specified date
# https://www.elle.com/en/sitemaps/content.2020-02-28T19:21:17.xml.gz

# This is the main sitemap URL for HARPERSBAZAR
# https://www.harpersbazaar.com/sitemap_index.xml
# This is an example URL for a compressed file containing links for the specified date
# https://www.harpersbazaar.com/en/sitemaps/content.2017-03-24T20:23:13.xml.gz

# Note: All extracted links are expected to belong to the year 2023

"""
    This module contains functions to extract links from a locally downloaded XML file. The XML file is obtained from the sitemaps listed in the robots.txt file of various websites, such as "Elle" and "Harper's Bazar". The functions are designed to parse the local XML file and extract links that meet specific criteria.

    Usage:
    - Call the get_links_using_xmlLocalFile function with the path to the local XML file to obtain a dictionary of links grouped by brand.

    Example:
    get_links_using_xmlLocalFile("Elle/content.2020-02-28T19_21_17.xml")
"""


def get_soup(xml_content):
    """
    Parse the XML content and extract sublinks that meet the following criteria:
        1. The last modification date is in the range of April to November 2023.
        2. The article title contains at least one of the following keywords: "louis-vuitton", "chanel", "dior", "versace".

    Parameters:
    - xml_content (str): Content of the XML file.

    Returns:
    - Dict[brand, List[str]]: Dictionary of sublinks grouped by brand that meet the criteria.
    """
    keywords = ["louis-vuitton", "chanel", "dior", "versace"]

    # Parse the XML content with BeautifulSoup
    soup = BeautifulSoup(xml_content, 'xml')

    # Find all <url> elements
    urls = soup.find_all('url')

    # Add only the URLs that meet the specific criteria
    final_sublinks = {keyword: [] for keyword in keywords}
    for url in urls:
        # Check if the last modification was in 2023
        lastmod = url.find('lastmod')
        months = ["2023-01", "2023-02", "2023-03", "2023-04", "2023-05", "2023-06", "2023-07", "2023-08",
                  "2023-09", "2023-10", "2023-11"]
        if re.search("|".join(months), lastmod.text):
            loc = url.find('loc')
            # Check if the article title contains the keywords
            for keyword in keywords:
                if re.search(keyword, loc.text):
                    final_sublinks[keyword].append(loc.text)

    return final_sublinks


def get_links_using_xmlLocalFile(xml_path):
    """
    Open and read an XML file at the specified path, then extract the required sublinks (from April to November 2023). These links will contain the keywords ("louis-vuitton", "chanel", "dior", "versace").

    Parameters:
    - xml_path (str): Path to the XML file.

    Returns:
    - Dict[brand, List[str]]: Dictionary with the required sublinks grouped by brand.
    """
    # Read the content of the file
    with open(xml_path, 'r', encoding='utf-8') as file:
        xml_content = file.read()
        final_sublinks = get_soup(xml_content)
        return final_sublinks


__all__ = ['get_links_using_xmlLocalFile']

# # Example usage
# path_elle_xml = "ELLE/content.2020-02-28T19_21_17.xml"
# print(get_links_using_xmlLocalFile(path_elle_xml))
