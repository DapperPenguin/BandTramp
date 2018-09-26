import requests
import re
import os
import sys
import json
from mutagen.mp3 import MP3
from bs4 import BeautifulSoup as bs
from mutagen.id3 import ID3NoHeaderError
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, COMM, USLT, TCOM, TCON, TDRC, TRCK, APIC


def getArtistName(html):
	data = bs(html, features='html.parser')
	name = data.find_all("span", {"itemprop":"byArtist"})[0].find("a").string
	return name.replace(':','׃').replace('<','﹤').replace('>','＞').replace('\"','').replace('/','∕').replace('|','').replace('*','').replace('?','')

def getAlbumName(html):
	data = bs(html, features='html.parser')
	names = data.find('head').find('title').contents[0]
	return names[:names.find('|')-1].replace(':','׃').replace('<','﹤').replace('>','＞').replace('\"','').replace('/','∕').replace('|','').replace('*','').replace('?','')

def getAlbumJSON(html):
	# get album page
	# create a BeautifulSoup object out of the album page html
	data = bs(html, features='html.parser')
	albumData = ""
	# find all script tags in data and loop through them
	for tag in data.find_all('script'):
		# if the tag contains a variable named TralbumData
		if('TralbumData' in str(tag)):
			# set albumData to the content of the TralbumData variable which will always match this regex
			albumData = re.search(r'trackinfo: \[{.*?}\]', str(tag))
			break
	# make a json object out of albumData (unwrapping the 'trackinfo' data)
	albumJSON = json.loads(albumData.group(0).replace('trackinfo: ', ''))
	# return the album JSON
	return albumJSON
	# VVV this is how you return the pretty album JSON VVV
	# return json.dumps(albumJSON, indent=4, sort_keys=True )

def getAlbumArt(link, cd, html):
	album = getURLFormattedAlbumName(link)
	artist = getURLFormattedArtistName(link)
	data = bs(html, features='html.parser')
	imageLink = str(data.findAll("a", {"class" : "popupImage"})[0]['href'])# this gets the biggest version of the image, there is a link to a smaller version in the img tag contained within [0]
	artResp = requests.get(imageLink)
	with open(cd+'/'+artist+'-'+album+'AlbumArt.jpg', 'wb') as f:
		f.write(artResp.content)
	
	return cd+'/'+artist+'-'+album+'AlbumArt.jpg'

def getTrack(cd, album, artist, art, trackJSON):
	name = trackJSON['title'].replace(':','׃').replace('<','﹤').replace('>','＞').replace('\"','').replace('/','∕').replace('|','').replace('*','').replace('?','')
	print('downloading '+name+'...')
	print(trackJSON['file']['mp3-128'])
	trackResp = requests.get(trackJSON['file']['mp3-128'])
	with open(cd+'/'+name+'.mp3', 'wb') as f:
		f.write(trackResp.content)

	try: 
	    track = ID3(cd+'/'+name+'.mp3')
	except ID3NoHeaderError:
	    print("Adding ID3 header")
	    track = ID3()

	track["TIT2"] = TIT2(encoding=3, text=trackJSON['title'])
	track["TALB"] = TALB(encoding=3, text=album)
	track["TPE2"] = TPE2(encoding=3, text=artist)
	track["TPE1"] = TPE1(encoding=3, text=artist)
	track["TRCK"] = TRCK(encoding=3, text=str(trackJSON['track_num']))
	track["APIC"] = APIC(
        encoding=3, # 3 is for utf-8
        mime='image/jpeg', # image/jpeg or image/png
        type=3, # 3 is for the cover image
        desc=u'Cover',
        data=open(art, 'rb').read()
    )

	track.save(cd+'/'+name+'.mp3')

def getAlbum(link, downloadDirectory):
	html = requests.get(link).content
	album = getAlbumName(html)
	print("\n### Downloading "+album+" ###")
	# if the artist's folder doesn't exist in the downloadDirectory
	artist = getArtistName(html)
	if(not os.path.exists(downloadDirectory+'/'+artist)):
		# make a folder for the artist
		os.mkdir(downloadDirectory+'/'+artist)
	# make the downloadDirectory this artist's folder
	downloadDirectory = downloadDirectory+'/'+artist
	# if the album's folder doesn't exist in the artist's folder
	if(not os.path.exists(downloadDirectory+'/'+album)):
		# make a folder for the album
		os.mkdir(downloadDirectory+'/'+album)
	# make the downloadDirectory that album's folder in the artist's folder  
	downloadDirectory = downloadDirectory+'/'+album
	# download album art (this is not strictly neccessary)
	art = getAlbumArt(link, downloadDirectory, html)
	# for every track object in the album JSON (which is an list)
	for track in getAlbumJSON(html):
		# download the track
		getTrack(downloadDirectory, album, artist, art, track)

def getURLFormattedArtistName(link):
	return link[8:link.find('.')]

def getURLFormattedAlbumName(link):
	return link[link.rfind('/')+1:]

# usage and arg checking
if(len(sys.argv) < 2):
	print("""
	Usage: python bandTramp.py [link] [download destination]

	link                 - the URL to the artist or album page
	download destination - the file path to the folder in which new folders should be created

	as of 8/19/2018 this program only works on albums that can be played for free in full
		""")

	exit()
elif(len(sys.argv) == 2):
	downloadDirectory = '.'
else:
	downloadDirectory = sys.argv[2]

# sets link to the given link
link = sys.argv[1]

# gets the album page response
html = requests.get(link).content
# does the html contain an inline audio player?
if(len(bs(html, features='html.parser').find_all("div", {"class":"inline_player"}))):
	# it does, so it's an album or track link
	getAlbum(link, downloadDirectory)
else:
	# it doesn't, so it's an artist link
	for alb in bs(html, features='html.parser').find("div", {"class":"leftMiddleColumns"}).find("ol").find_all("li"):
		getAlbum(link+alb.find("a")["href"], downloadDirectory)


# Meth Wax - 048: Meth Wax
# The Mountain Goats - Song for Sasha Banks