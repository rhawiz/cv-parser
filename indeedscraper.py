import random
from time import sleep

from bs4 import BeautifulSoup

from utils.netutils import generate_request_header
import requests
import urllib

BASE_URL = "http://www.indeed.com/resumes?q=%s&l=%s&co=%s&start=%s"
DOWNLOAD_BASE_URL = "http://www.indeed.com%s/pdf"


def scrape(area, city, country_code, page):
    url = BASE_URL % (area, city, country_code, page)

    header = generate_request_header()
    response = requests.get(url, headers=header)
    html = response.text
    html_soup = BeautifulSoup(html, "html.parser")
    raw_profile_list = html_soup.find_all('li', attrs={'class': 'sre'})

    for raw_profile in raw_profile_list:
        download_part = raw_profile.find("a").get("href")[0:-5]
        download_url = DOWNLOAD_BASE_URL % download_part
        id = download_part.split("/")[-1]
        print download_part
        urllib.urlretrieve (download_url, "cvs/%s.pdf" % id)
        wait_time = random.uniform(1.0, 5.0)
        sleep(wait_time)


if __name__ == "__main__":
    scrape("banking", "london","GB","0")
