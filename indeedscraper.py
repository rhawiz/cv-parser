import os
import random
from time import sleep

from bs4 import BeautifulSoup
from utils.netutils import generate_request_header
import requests
import urllib

BASE_URL = "http://www.indeed.com/resumes?q=%s&l=%s&co=%s&start=%s"
DOWNLOAD_BASE_URL = "http://www.indeed.com%s/pdf"
categories = (
    "media", "publishing", "journalism", "medical",
    "pharmaceutical", "health care", "property", "real estate", "public", "government", "social", "retail", "buying",
    "merchandising", "fmcg", "sales", "science", "research", "banking", "financial services", "business", "management",
    "charity", "non-profit", "construction", "property", "quantity surveying", "building", "surveying", "consultancy",
    "strategy", "education", "training", "teaching", "engineering", "manufacturing", "fashion", "hospitality", "travel",
    "tourism", "hr", "recruitment", "insurance", "IT", "technology", "telecommunications", "legal", "law", "logistics",
    "transport", "supply chain", "marketing", "pr", "advertising",  # "defence", "accounting", "finance", " aerospace",
)

def scrape(category, city, country_code, count):
    root_dir = "cv/%s" % category
    print category
    if not os.path.isdir(root_dir):
        os.makedirs(root_dir)

    for start in range(0, count, 50):
        url = BASE_URL % (category, city, country_code, start)
        print "\t%s" % url
        raw_profile_list = []

        while not raw_profile_list:
            header = generate_request_header()
            response = requests.get(url, headers=header)
            html = response.text
            html_soup = BeautifulSoup(html, "html.parser")
            raw_profile_list = html_soup.find_all('li', attrs={'class': 'sre'})
            print "\t\t%s" % raw_profile_list
            sleep(random.uniform(0.1, 0.5))

        for raw_profile in raw_profile_list:
            a = raw_profile.find("a")
            href = a.get("href")
            if not href:
                start = start - 50
                print start
                break
            download_part = href[0:-5]
            download_url = DOWNLOAD_BASE_URL % download_part
            id = download_part.split("/")[-1]
            file_path = "%s/%s.pdf" % (root_dir, id)
            if not os.path.isfile(file_path):
                urllib.urlretrieve(download_url, file_path)
                print "\t\t" + download_url
            wait_time = random.uniform(0.1, 0.5)
            sleep(wait_time)


if __name__ == "__main__":
    for cat in categories:
        scrape(cat, "london", "GB", 500)
