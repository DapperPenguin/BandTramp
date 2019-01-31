import os
import sys
import enum
from mutagen.mp3 import MP3
from mutagen.id3 import ID3NoHeaderError
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, COMM, USLT, TCOM, TCON, TDRC, TRCK, APIC, TSOT, TSOA, TSO2


def printTags(tracks):
	# print(track)
	for track in tracks:
		print(track)
		print('\n\n')

def setTrackName(tracks, name):
	for track in tracks:
		track.add(TSOT(encoding=3, text=name))
		track.add(TIT2(encoding=3, text=name))
		track.save()

def printTrackName(tracks):
	for track in tracks:
		print('TSOT: '+track['TSOT'])
		print('TIT2: '+track['TIT2'])

def printArtistName(tracks):
	for track in tracks:
		print('TPE2: '+track['TPE2'])
		print('TSOT: '+track['TSOT'])
		print('TPE1: '+track['TPE1'])

def setArtistName(tracks, name):
	for track in tracks:
		track.add(TPE2(encoding=3, text=name))
		track.add(TSOT(encoding=3, text=name))
		track.add(TPE1(encoding=3, text=name))
		track.save()

def printAlbumName(tracks):
	for track in tracks:
		print('TALB: '+track['TALB'])
		print('TSOA: '+track['TSOA'])

def setAlbumName(tracks, name):
	for track in tracks:
		track.add(TALB(encoding=3, text=name))
		track.add(TSOA(encoding=3, text=name))
		track.save()

def printAlbumArt(tracks):
	for track in tracks:
		img = track['APIC:thumbnail']
		print(img.mime+'\n'+ArtType[img.type]+'\n'+img.desc)

def setAlbumArt(tracks, imgPath):
	for track in tracks:
		fileType = imgPath[imgPath.rfind('.')+1:].strip()
		track["APIC:thumbnail"] = APIC(
			encoding = 3,
			mime = 'image/'+fileType,
			type = 3,
			desc=u'Cover',
			data = open(imgPath, 'rb').read()
		)
		track.save()

def printTrackNumber(tracks):
	for track in tracks:
		print('TRCK: '+track['TRCK'])

def setTrackNumber(tracks, num):
	for track in tracks:
		track.add(TRCK(encoding=3, text=num))
		track.save()

tracks = []

if(len(sys.argv) < 2):
	print("""
	Usage: python TagEdit.py [file path]

	file path - The location of the filePath (in any of the following formats)
				- from the current directory
				- a full path
				- * (from the current directory)
	""")
	exit()
elif(('/' not in sys.argv[1]) and ('\\' not in sys.argv[1]) and ('*' not in sys.argv[1])):
	filePath = './'+sys.argv[1]
	tracks.append(ID3(filePath))
elif('*' in sys.argv[1]):
	for file in os.listdir('./'+sys.argv[1][:sys.argv[1].find('*')]):
		if(file.endswith('.mp3')):
			tracks.append(ID3('./'+sys.argv[1][:sys.argv[1].find('*')]+file))
else:
	filePath = sys.argv[1]
	tracks.append(ID3(filePath))





while True:
	resp = input(
		"""
	Select a tag to edit:
	1)	Track
	2)	Artist
	3)	Album
	4)	Cover Art
	5)	Track Number
	6)  (print tags)
		"""
	)

	if(resp.strip() == '1'):
		setTrackName(tracks, input("New track name: "))
	elif(resp.strip() == '2'):
		setArtistName(tracks, input("New artist name: "))
	elif(resp.strip() == '3'):
		setAlbumName(tracks, input("New album name: "))
	elif(resp.strip() == '4'):
		setAlbumArt(tracks, input("Path to new cover art: "))
	elif(resp.strip() == '5'):
		setTrackNumber(tracks, input("New Track Number: "))
	elif(resp.strip() == '6'):
		printTags(tracks)
	else:
		exit()

	
	cont = input('Edit more tags (Y/N)?: ')
	if(cont != 'y' and cont != 'Y'):
		break




