import requests
from bs4 import BeautifulSoup
import re
from requests.exceptions import RequestException


class ScrapeVogueOrGlamour:
    """
    Class for scraping websites like Vogue or Glamour.
    """

    def __init__(self) -> None:
        pass

    def verified_article(self, link, namebrand, website):
        """
        Verify and extract information from an article.

        Parameters:
        - link (str): URL of the article.
        - namebrand (str): Brand to look for in the article.
        - website (str): Name of the website (vogue or glamour).

        Returns:
        - dict: Dictionary with the article information or None if it doesn't meet the criteria.
        """
        try:
            request_headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
            }

            # Make a GET request to the sublink
            response = requests.get(link, headers=request_headers)
            response.raise_for_status()  # Raise an exception for HTTP status codes other than 200

            # Parse the HTML
            soup = BeautifulSoup(response.text, "html.parser")

            # Find the title of the article
            title = soup.find('h1')

            # Find the containers that contain the paragraphs of the article
            if website == "vogue":
                paragraphs = soup.find_all(
                    'div', {'class': 'grid-layout__content'})
            elif website == "glamour":
                paragraphs = soup.find_all(
                    'div', {'class': 'body__inner-container'})
            else:
                raise ValueError("Error, incorrect magazine name")

            # Select only the plain text of the paragraphs
            article_text = ' '.join(
                [par.text + ' ' for p in paragraphs for par in p.find_all('p')])

            # -------------Aditional for Vogue--------------------#
            # Check if the website is "vogue" and remove a specific signature from the article text.
            article_text = article_text[:article_text.find(
                "By signing up")].strip() if website == "vogue" else article_text

            # Replace the quotation marks
            if title:
                title = title.text
                title.replace('“', '"').replace('”', '"')
                title.replace('`', "'").replace('’', "'")

            article_text = article_text.replace('“', '"').replace('”', '"')
            article_text = article_text.replace('`', "'").replace('’', "'")

            dictArticle = {}

            # Check if the keyword (brand) appears more than 2 times and if the text contains more than 100 words but less than 1100
            # If the 'namebrand' is equal to "louis vuitton," consider alternative representations of the brand, such as "LV" or "LVMH."
            article_verify_keywordN = re.findall(
                "|".join(["louis vuitton", "LV", "LVMH"]
                         ) if namebrand == "louis vuitton" else namebrand,
                article_text,
                re.IGNORECASE)

            if len(article_verify_keywordN) > 2 and len(article_text.split()) > 100 and len(article_text.split()) < 1100:
                # Add to the dictionary the details of the article
                dictArticle = {
                    "website": website,
                    "brand": namebrand,
                    "title": title,
                    "content": article_text
                }
                return dictArticle
            else:
                return None
        except RequestException as e:
            return None
        except Exception as e:
            return None


class ScrapeElleOrBazar:
    """
    Class for scraping websites like Elle or Harper's Bazaar.
    """

    def __init__(self) -> None:
        pass

    def verified_article(self, link, namebrand, website):
        """
        Verify and extract information from an article.

        Parameters:
        - link (str): URL of the article.
        - namebrand (str): Brand to look for in the article.
        - website (str): Name of the website (elle or harper's bazaar).

        Returns:
        - dict: Dictionary with the article information or None if it doesn't meet the criteria.
        """
        try:
            request_headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
            }
            # Make a GET request to the sublink
            response = requests.get(link, headers=request_headers)

            soup = BeautifulSoup(response.text, "html.parser")

            # Ensure that the publication date of the article is in 2023
            if re.findall("2023", soup.find("time").text):
                # Find the title of the article
                title = soup.find('h1')
                if title:
                    # Replace the quotation marks
                    title = title.text
                    title = title.replace('“', '"').replace('”', '"')
                    title = title.replace('`', "'").replace('’', "'")

                # Find the containers that contain the paragraphs of the article
                paragraphs = soup.find_all(
                    'div', {'class': 'article-body-content'})

                # Select only the plain text of the paragraphs
                article_text = ' '.join(
                    [par.text + ' ' for p in paragraphs for par in p.find_all('p', {'data-journey-content': "true"})])

                # Replace the quotation marks
                article_text = article_text.replace('“', '"').replace('”', '"')
                article_text = article_text.replace('`', "'").replace('’', "'")

                dictArticle = {}

                # Check if the keyword (brand) appears more than 2 times and if the text contains more than 100 words but less than 1100
                # If the 'namebrand' is equal to "louis vuitton," consider alternative representations of the brand, such as "LV" or "LVMH."
                article_verify_keywordN = re.findall(
                    "|".join(["louis vuitton", "LV", "LVMH"]
                             ) if namebrand == "louis vuitton" else namebrand,
                    article_text,
                    re.IGNORECASE)

                if len(article_verify_keywordN) > 2 and len(article_text.split()) > 100 and len(article_text.split()) < 1100:
                    # Add to the dictionary the details of the article
                    dictArticle = {
                        "website": website.lower(),
                        "brand": namebrand,
                        "title": title,
                        "content": article_text
                    }
                    return dictArticle
                else:
                    return None
            return None
        except RequestException as e:
            return None
        except Exception as e:
            return None


class ArticlesMain:
    """
    Main class for managing and extracting articles from different websites.
    """

    def __init__(self, website, dictionary):
        """
        Initialize the ArticlesMain object.

        Parameters:
        - website (str): Name of the website.
        - dictionary (dict): Dictionary containing sublinks grouped by brand.
        """
        self.website = website
        self.dictionary = dictionary
        self.scrape_vogue_or_glamour = ScrapeVogueOrGlamour()
        self.scrape_elle_or_bazar = ScrapeElleOrBazar()

    def create_list_select_sublinks(self, namebrand, sublinks):
        """
        Create a list of selected articles from sublinks.

        Parameters:
        - namebrand (str): Brand name.
        - sublinks (list): List of sublinks for the brand.

        Returns:
        - list: List of dictionaries of selected articles.
        """
        articles_selected = []
        for sub in sublinks:
            # Only take 4 articles per brand
            if len(articles_selected) == 4:
                return articles_selected

            if self.website == "vogue" or self.website == "glamour":
                # Verify that the article meets the criteria
                dict_sub = self.scrape_vogue_or_glamour.verified_article(
                    sub, namebrand, self.website)
            elif self.website == "elle" or self.website == "harper's bazar":
                dict_sub = self.scrape_elle_or_bazar.verified_article(
                    sub, namebrand, self.website)

            # Verify that it is not None
            if dict_sub is not None:
                articles_selected.append(dict_sub)
        # If there are not four articles, then return the list of collected articles
        return articles_selected

    def all_articles_selected(self, list_of_keywords=None):
        """
        Get a list of dictionaries representing the selected articles.

        Parameters:
        - list_of_keywords (list): List of keywords to recognize the brand within the provided dictionary.

        Returns:
        - list: List of dictionaries of selected articles.
        """
        # List for all final dictionaries containing the final articles selected by brand for each site
        list_of_dicts = []

        # Default list of keywords if not provided
        if list_of_keywords is None:
            list_of_keywords = ["louis-vuitton", "chanel", "dior", "versace"]

        # Iterate over each brand
        for key_brand in list_of_keywords:
            # Extract the links corresponding to each brand
            sublinks = self.dictionary[key_brand]
            # Check if there are dashes in the keyword to remove them and use it as the brand name
            namebrand = key_brand.replace("-", " ")
            # Expand the list with the generated dictionaries
            list_of_dicts.extend(
                self.create_list_select_sublinks(namebrand, sublinks))

        return list_of_dicts


__all__ = ['ArticlesMain']

# Example usage:
# dict_vogue = get_links_using_requests("vogue")
# articles_main = ArticlesMain("vogue", dict_vogue)
# print(articles_main.all_articles_selected())
