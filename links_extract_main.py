# Import necessary modules
from requests_link_extractor import get_links_using_requests
from xmlLocalFile_link_extractor import get_links_using_xmlLocalFile
import pandas as pd
from scrape_articles import ArticlesMain

# This module orchestrates the entire data extraction and compilation process.

# VOGUE
dict_vogue = get_links_using_requests("vogue")
articles_main_vogue = ArticlesMain("vogue", dict_vogue).all_articles_selected()

# GLAMOUR
dictGlamour = get_links_using_requests("glamour")
articles_main_glamour = ArticlesMain(
    "glamour", dictGlamour).all_articles_selected()

# Elle
path_elle_xml = "ELLE/content.2020-02-28T19_21_17.xml"
dictElle = get_links_using_xmlLocalFile(path_elle_xml)
articles_main_elle = ArticlesMain("elle", dictElle).all_articles_selected()


# # Harper's Bazar
path_harpersBazar_xml = "HARPERS_BAZAR/content.2017-03-24T20_23_13.xml"
dictHarpersBazar = get_links_using_xmlLocalFile(path_harpersBazar_xml)
articles_main_bazar = ArticlesMain(
    "harper's bazar", dictHarpersBazar).all_articles_selected()


# combine articles
list_of_articles = []
list_of_articles.extend(articles_main_vogue)
list_of_articles.extend(articles_main_glamour)
list_of_articles.extend(articles_main_elle)
list_of_articles.extend(articles_main_bazar)

# create DataFrame and save to CSV
df = pd.DataFrame(list_of_articles)
print(df)
df.to_csv("selectedFinalArticles.csv", index=False)
