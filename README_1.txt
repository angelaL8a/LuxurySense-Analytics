Workflow description (Webscraping articles)
requests_link_extractor.py, xmlLocalFile_link_extractor.py, scrape_articles.py, links_extract_main.py, selectedFinalArticles.csv

The primary objective of this workflow is to extract and analyze pertinent data from fashion websites (vogue,glamour,elle,harper's bazar), focusing on articles published in 2023 and featuring specific keywords such as "louis-vuitton," "chanel," "dior," and "versace." The comprehensive process encompasses link extraction, article scraping, and data compilation for subsequent analysis.

Workflow Stages:
1. Link Extraction:
    1.1 requests_link_extractor.py:
    This module facilitates the extraction of article links by emulating GET requests to sitemaps, specifically tailored for websites like Vogue and Glamour. For instance:

    Vogue Sitemap:
        https://www.vogue.com/sitemap.xml?year=2023&month=11&week=4
    Glamour Sitemap: 
        https://www.glamour.com/sitemap.xml?year=2023&month=11&week=4
    This module (requests_link_extractor.py) extracts links for articles published in 2023 and containing the specified keywords.

    1.2 xmlLocalFile_link_extractor.py:
    Tailored for Elle and Harper's Bazaar, this module retrieves links from locally stored XML files obtained from their respective sitemaps. Examples:

    Elle Sitemap: The 'ELLE' folder houses the XML file retrieved from the elle.com sitemap
        https://www.elle.com/en/sitemaps/content.2020-02-28T19:21:17.xml.gz
    Harper's Bazaar Sitemap: The 'HARPERS_BAZAR' folder contains the XML file retrieved from the sitemap
        https://www.harpersbazaar.com/en/sitemaps/content.2017-03-24T20:23:13.xml.gz
 
    Each function within these modules returns a dictionary where each brand (keyword) serves as a key, and the corresponding value is a list of links to articles containing that specific keyword.

    So, a total of 4 dictionaries were obtained, each from a different website.



2. Article Scraping:   
    2.1 scrape_articles.py:
    This module introduces two classes, ScrapeVogueOrGlamour and ScrapeElleOrBazar. These classes emulate GET requests to article links and meticulously verify if the articles meet predetermined criteria, including word count and publication year. Articles meeting the criteria are returned as dictionaries containing website, title, and content.

    Finally, the ArticlesMain class is responsible for returning a list of dictionaries representing the selected articles. 

3. Data Compilation:
    3.1 links_extract_main.py:
    This module orchestrates the functionalities of the aforementioned modules to obtain the list of dictionaries (articles selected). Furthermore, this module centralized all identified articles, storing them in an organized dataframe that includes essential details such as website source, title, and content. Following this centralization, the data was be systematically stored in a CSV file "selectedFinalArticles.csv". This structured approach ensures efficient data management, making subsequent analysis and information extraction more streamlined and accessible.

Considerations:
    It's crucial to acknowledge that the data within selectedFinalArticles.csv may necessitate additional refinement. The data cleaning process will be executed directly within the Jupyter notebook "REPORT.ipynb".

Order of creation:
    requests_link_extractor.py
    xmlLocalFile_link_extractor.py
    scrape_articles.py
    links_extract_main.py
    selectedFinalArticles.csv


