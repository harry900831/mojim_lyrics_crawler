import requests
import json
from bs4 import BeautifulSoup

CHINESE_ONLY = True
START_YEAR = 2000
END_YEAR = 2020

def get_album_info(url):
	response = requests.get(url)
	soup = BeautifulSoup(response.text, "lxml")
	table = soup.find(id = "page3_01")
	info = table.find_all("tr")[1].find("h2").text
	info = info[info.find("】") + 3:]
	language = info[:info.find("】") - 1]
	info = info[info.find("【") + 2:]
	date = info[:info.find("】") - 1]
	return (language, date)

def crawl_lyrics(url) :
	response = requests.get(url)
	soup = BeautifulSoup(response.text, "lxml")
	content = soup.find(id = "fsZx3")
	if not content:
		print("JIZZ NOT FOUND..... URL: " + url)
		return []
	# example: http://mojim.com/twy222225x11x4.htm
	for i in content("ol") : #example:https://mojim.com/twy104616x4x3.htm
		i.extract()

	lyrics = list()
	for line in content.stripped_strings :
		if "更多更詳盡歌詞 在" in line or "※ Mojim.com　魔鏡歌詞網" in line :
			continue
		if "：" in line : #example:https://mojim.com/twy108440x39x1.htm
			continue
		if line.find('[') != -1 or line.find(']') != -1 : #example:https://mojim.com/twy104824x14x1.htm
			continue
		if "--" in line : #example:https://mojim.com/twy102447x19x1.htm
			break;
		lyrics.append(line)

	return lyrics

def crawl_songs():
	Mojim_URL = "http://mojim.com"
	URL = "http://mojim.com/twzlist"
	for year in range(START_YEAR, END_YEAR + 1) :
		for month in range(1, 13) :
			songs_list = list()
			YEAR = str(year)
			if month < 10 :
				MONTH = "0" + str(month)
			else :
				MONTH = str(month)
			print("Begin crawling songs in " + YEAR + '-' + MONTH + ".")

			response = requests.get(URL + YEAR + '-' + MONTH + ".htm")
			soup = BeautifulSoup(response.text, "lxml")

			title = soup.find("title")
			if not (YEAR in title.text) or not (MONTH in title.text) :
				print("Unable to crawl songs in " + YEAR + '-' + MONTH + ".")
				continue

			album_list = soup.find_all("dd")
			for album in album_list :
				general_info = dict()
				album_name = album.find("h1")
				general_info["singer"] = album_name.find("a").text
				album_url = album_name.find_all("a")[1]["href"]
				general_info["language"], general_info["date"] = get_album_info(Mojim_URL + album_url)

				if CHINESE_ONLY and general_info["language"] != "國語" :
					continue;
				
				for song in album.find_all("span") :
					song_info = general_info.copy()
					song_tag = song.find("a")
					song_info["name"] = song_tag.text
					song_info["lyrics"] = crawl_lyrics(Mojim_URL + song_tag["href"])
					if song_info["lyrics"] == []:
						continue
					songs_list.append(song_info)

			with open(YEAR + '-' + MONTH + ".json", 'w') as json_file :
				json.dump(songs_list, json_file, ensure_ascii = False)

			print("Crawling songs in " + YEAR + '-' + MONTH + " has finished.")
			
			 	


if __name__ == '__main__' :
	crawl_songs()



#exception http://mojim.com/twy222770x1x4.htm


