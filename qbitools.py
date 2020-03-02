import pickle
from qbittorrent import Client

import time
# qbt_client = qbittorrentapi.Client(host='localhost:8080', username='admin', password='adminadmin')
qb = Client("http://127.0.0.1:8080/")



qb.login("telegram", "telegrambot")

# torrent_info = qb.get_torrent("a8e19fe7d79369dc5a702f821f76d8abd655178b")

# print(int(torrent_info["pieces_have"]/torrent_info["pieces_num"]*1000)/10)
# print(torrent_info["eta"])


def download_torrent_from_file(torrentbytes):
	qb.download_from_file(torrentbytes, catagory="Python")
	torrent_hash = qb.torrents(sort="added_on")[-1]["hash"]
	return torrent_hash

def download_torrent_from_magnet(torrentlink):
	qb.download_from_link(torrentlink, label="python")
	torrent_hash = qb.torrents(sort="added_on")[-1]["hash"]
	return torrent_hash



def get_progress(hash_of_torrent):
	torrent_info = qb.get_torrent(hash_of_torrent)
	percent = int(torrent_info["pieces_have"]/torrent_info["pieces_num"]*1000)/10
	etaunix = torrent_info["eta"]
	hours = etaunix // 3600
	minutes = (etaunix % 3600) // 60

	return (percent, (hours, minutes))



	