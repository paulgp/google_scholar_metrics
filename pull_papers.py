# This script pulls the papers and cites from the top 20 journals in business and economics
# as listed on Google Scholar. It then saves the data to a csv file.

# Import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
import time 

ECON_URL = "https://scholar.google.com/citations?view_op=top_venues&hl=en&vq=bus_economics"
FINANCE_URL = "https://scholar.google.com/citations?view_op=top_venues&hl=en&vq=bus_finance"

# This function pulls the 20 journal names listed on a url, and the corresponding h5-index.
# It also pulls the url link to the journal's page on Google Scholar listed in the h5-index.
def pull_journals(url):
    # Pull the html from the url
    page = requests.get(url,  headers = {'User-agent': 'pgp'})
    soup = BeautifulSoup(page.content, 'html.parser')
    # Pull the journal names and h5-indexes
    journals = soup.find_all('td', class_='gsc_mvt_t')
    # Pull the journal links
    links = [bin for bin in soup.find_all('td', class_='gsc_mvt_n')]
    links = [link.find('a') for link in links]
    # Create a list of journal names
    journal_names = []
    for journal in journals:
        journal_names.append(journal.text)
    # Create a list of h5-indexes
    h5_indexes = []
    for journal in journals:
        h5_indexes.append(journal.find_next_sibling().text)
    # Create a list of journal links
    journal_links = []
    for link in links:
        if link is not None:
            journal_links.append("https://scholar.google.com" + link['href'])
    # Create a dataframe of the journal names, h5-indexes, and links
    df = pd.DataFrame({'Journal': journal_names, 'h5-index': h5_indexes, 'Link': journal_links})
    return df

# This function pulls the paper titles, authors, year and cites from a journal's page on Google Scholar.
def pull_papers(url, journal_name):
    # Pull the html from the url
    page = requests.get(url,  headers = {'User-agent': 'pgp'})
    soup = BeautifulSoup(page.content, 'html.parser')
    # Pull the paper titles
    titles = soup.find_all('a', class_='gsc_mp_anchor_lrge')
    # Pull the paper authors
    authors = soup.find_all('div', class_='gs_gray')[:-1][::2]
    # Pull the paper years
    years = soup.find_all('span', class_='gs_ibl gsc_mp_anchor gs_nta gs_nph')
    # Pull the paper cites
    cites = soup.find_all('a', class_='gs_ibl gsc_mp_anchor')
    cites = [cite for cite in cites if cite.text.isnumeric()]
    # Create a list of paper titles
    paper_titles = []
    for title in titles:
        paper_titles.append(title.text)
    # Create a list of paper authors
    paper_authors = []
    for author in authors:
        paper_authors.append(author.text)
    # Create a list of paper years
    paper_years = []
    for year in years:
        paper_years.append(year.text)
    # Create a list of paper cites
    paper_cites = []
    for cite in cites:
        paper_cites.append(cite.text)
    # Create a dataframe of the paper titles, authors, years, and cites
    if len(paper_titles) > 20:
        print(paper_titles)
    if len(paper_authors) > 20:
        print(paper_authors)
    if len(paper_years) > 20:
        print(paper_years)
    if len(paper_cites) > 20:
        print(paper_cites)
    df = pd.DataFrame({'Title': paper_titles, 'Authors': paper_authors, 'Year': paper_years, 'Cites': paper_cites, 'Journal': journal_name})
    return df

if __name__ == '__main__':
    df_econ = pull_journals(ECON_URL)
    df_econ.to_csv('data/econ_journals.csv')
    df_finance = pull_journals(FINANCE_URL)
    print(df_finance)
    df_finance.to_csv('data/finance_journals.csv')
    for journal, journal_name in zip([*df_econ['Link'], *df_finance['Link']], [*df_econ['Journal'], *df_finance['Journal']]):
        print(journal_name)
        df2 = pull_papers(journal, journal_name)
        print(df2)
        df2.to_csv('data/' + journal_name + '.csv', mode='a', header=False)
        time.sleep(5)


    

