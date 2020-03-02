import pickle
import time
import requests
from bs4 import BeautifulSoup

from qbitools import download_torrent_from_file, get_progress, download_torrent_from_magnet

def get_search_links_ai(search_string):
    search_string = search_string.replace(" ", "+")
    query = f"https://yts.ai/movie/yifi_filter?keyword={search_string}&quality=all&genre=all&rating=0&order_by=latest'"

    results_page = requests.get(query)
    soup = BeautifulSoup(results_page.text, "html.parser")
    lnks = soup.findAll("a", class_="browse-movie-link")
    movies = []
    for i in lnks:
        page_link = i["href"]
        name = page_link.split("/")[-2].replace("-", " ").capitalize() + " " + page_link.split("/")[-1].replace("-", " ").capitalize()
        movies.append((name, page_link))
    return movies


def get_search_links(search_string):
    search_string = search_string.replace(" ", "+")
    query = f"https://yts.ai/browse-movies/{search_string}/all/all/0/latest"
    results_page = requests.get(query)
    soup = BeautifulSoup(results_page.text, "html.parser")
    lnks = soup.findAll("a", class_="browse-movie-link")
    movies = []
    for i in lnks:
        page_link = i["href"]
        name = page_link.split("/")[-1].replace("-", " ").capitalize()
        movies.append((name, page_link))
    return movies





class Movie_suggestions():


    def __init__(self, joined_list):
        self.joined_list = joined_list
        self.names = [x[0] for x in self.joined_list]
        self.url = [x[1] for x in self.joined_list]
        t = [") ".join([str(i) for i in j]) for j in enumerate(self.names)]
        self.list_of_options = "\n\n".join(t)




    




class Movie(Movie_suggestions):


    def __init__(self, name_url):
        self.name = name_url[0]
        self.url = name_url[1]


    def load_torrent(self, quality):
        url = self.url
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        a = soup.find_all("a")
        torrent_file_link = [x["href"] for x in a if quality in x.text][0]
        # self.torrent_link = torrent_file_link
        torrent_request = requests.get(torrent_file_link)
        self.torrentfilebytes = torrent_request.content

    def load_magnet(self, quality):
        url = self.url
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        lnks = soup.find_all("a")
        magnets = [i["href"] for i in lnks if f"{quality}" in i.text]
        self.torrent_link = magnets[0]
        # print(self.torrent_link)
        print(magnets[0])


    def download_from_file(self, quality):
        self.load_torrent(quality)
        self.hash = download_torrent_from_file(self.torrentfilebytes)

    def download_from_magnet(self, quality):

        self.load_magnet(quality)
        # time.sleep(2)
        self.hash = download_torrent_from_magnet(self.torrent_link)

    def get_progress(self):
        percent, eta = get_progress(self.hash)
        self.percent = percent
        self.eta = eta
        percent_message = f'{self.percent}% done'
        eta_message = f'{self.eta[0]} hour(s) and {self.eta[1]} minute(s) remaining'
        self.waiting_message = percent_message + "\n" + eta_message







def request():
    search_term = input("What would you like me to search for? ")
    # search_term = "dictator"
    working_suggestions = Movie_suggestions(get_search_links_ai(search_term))
    # lst = list(zip(range(1, len(Movie_suggestions.names)+1),
    #              Movie_suggestions.names))
    print("\n\n\n")
    for f in enumerate(working_suggestions.names):
        print(*f)
    print("\n\n\n")
    choice = int(input("select from options\n\n\n"))
    working_movie = Movie(working_suggestions.joined_list[choice])
    print(working_movie.name)

    # working_movie = Movie(new_name, new_url)
    # print(working_movie.name)
    quality = input("what quality should be downloaded\n\n\n")
    # working_movie.load_magnet(quality)
    # print(working_movie.torrent_link)
    # working_movie.load_magnet(quality)
    working_movie.download_from_magnet(quality)
    # while working_movie.percent < 100:
    #   working_movie.get_progress()
    #   print(working_movie.percent, "\n", working_movie.eta)
    #   time.sleep(5)

if __name__ == "__main__":

  request()
