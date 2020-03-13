import json
import os
import requests
from bs4 import BeautifulSoup
import time
import random

def crawl_youtube_id(singer, song_name):
	url = "https://www.youtube.com/results?search_query=" + singer + "+" + song_name
	request = requests.get(url)
	content = request.content
	soup = BeautifulSoup(content, "html.parser")
	meow = soup.select_one(".yt-lockup-video")
	count = 0
	while not meow:
		if count == 10:
			return "/watch?v=rSJ4jtghTDc"
#		time.sleep(random.random() * 10)
		request = requests.get(url)
		content = request.content
		soup = BeautifulSoup(content, "html.parser")
		meow = soup.select_one(".yt-lockup-video")
		count+=1
	data = meow.select("a[rel='spf-prefetch']")
	if data == []:
		return "/watch?v=rSJ4jtghTDc"
	return data[0].get("href")


def walk():
	for dirPath, dirNames, fileNames in os.walk("."):
		for f in fileNames:
			if not f.endswith('.json'):
				continue;
			print(f)
			songspath = dirPath + '/' + f
			with open(songspath, 'r') as fp:
				songs = json.load(fp)
			
			for song in songs:
				song['youtube_id'] = crawl_youtube_id(song['singer'], song['name'])


			with open(songspath, 'w') as fp:
				json.dump(songs, fp, ensure_ascii = False)
			
			print(f + ": Finish!")



if __name__ == '__main__':
	walk()
