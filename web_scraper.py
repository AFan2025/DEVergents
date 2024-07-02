import pandas as pd
import requests
from bs4 import BeautifulSoup
from collections import Counter
import re
import argparse

ARTICLE_BODY = ['body__inner-container']
LINK_CLASS = ["SummaryItemImageLink-dshqxb cPpCwE summary-item__image-link summary-item-tracking__image-link"]

class pitchforkScraper:

    def __init__(self, start_idx, end_idx):

        #this is the base link
        self.base_link = 'https://pitchfork.com'

        #this is how articles pages are parsed
        self.articles_link = "https://pitchfork.com/reviews/tracks/?page="

        #whichever article page you want to start at in case you want to do this in batches
        self.start_idx = start_idx
        self.curr_idx = None

        #just so it doesn't run forever and we know which page it stops at 
        #in case we want to keep going without repeats
        self.end_idx = end_idx

    #parses through individual articles
    def article_parser(link):
        count_dict = {}
        
        #request to pitchfork
        song = requests.get(link)

        #status code 200 means that it was able to return something
        if song.status_code == 200:
            song_lxml = BeautifulSoup(song.text, 'lxml')
            song_rev = song_lxml.find('div',{'class':ARTICLE_BODY})

            #if it was able to find an article body html header
            if song_rev:

                #text comprehension that returns a list of all of the words
                text = song_rev.get_text(strip=True)
                text = text.lower() 
                text = re.sub(r'[^\w\s]', '', text)
                text = text.replace('\n', ' ')
                words = text.split()

                #this will return a count of all of the words
                word_counts = Counter(words)
                count_dict = dict(word_counts)

        return count_dict

    #parses through a page of articles and enters into each one of them
    def page_parser(self):
        total_dict = {}

        #for every page of articles
        for i in range(self.start_idx,self.end_idx + 1):

            #gets every article page
            pages = requests.get(self.articles_link + str(i))
            pages_lxml = BeautifulSoup(pages.text, 'lxml')

            #finds the link of every page and makes an iterable list
            tracks_pages = pages_lxml.find_all('a',{'class': LINK_CLASS})

            #for loop that iterates over every single link
            for idx, _ in enumerate(tracks_pages):
                
                #gets the link
                article = tracks_pages[idx].attrs['href']
                article_link = self.base_link + article

                #calls the other function to parse the word count of every article
                article_counts = self.article_parser(article_link)

                # Use Counter to sum dictionaries
                counter1 = Counter(total_dict)
                counter2 = Counter(article_counts)

                # Sum the counters
                counter_result = counter1 + counter2

                # Convert back to a regular dictionary if needed
                total_dict = dict(counter_result)
        return total_dict

def main(args):
    music_adjectives = pitchforkScraper(args.start,args.end)
    result = music_adjectives.page_parser()
    return result

if "__name__" == "__main__":
    parser = argparse.ArgumentParser(description="helps out")

    parser.add_argument('--start', type=int, required=True, help='the page you want to start')
    parser.add_argument('--end', type=int, required=True, help='the page you want to end at')

    args = parser.parse_args()
    main(args)

    ##the way to run this would be to call it python3 web_scraper_test.py --start (number) --end (number)



#Articles used: https://medium.com/@stephaniecaress/scraping-pitchforks-best-new-music-be563d18ea4f