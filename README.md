# mojim_lyrics_crawler
Mojim.com 魔鏡歌詞網 歌詞爬蟲
將所有魔境歌詞網中歌曲的的歌詞、歌手、日期、專輯語言、按照年份月份爬下來。
## crawler.py
```
CHINESE_ONLY = True 
```
只會爬魔鏡歌詞網專輯介紹中為國語專輯的歌曲，改成 False 的話就所有歌曲都爬。

## getyoutubeid.py
從歌詞.json檔案中用歌名+歌手去youtube搜尋，取得第一個搜尋結果的影片id。
若搜尋查無結果，就會回傳一個酷酷的影片id。




