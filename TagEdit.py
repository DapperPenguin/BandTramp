import sys
import enum
from mutagen.mp3 import MP3
from mutagen.id3 import ID3NoHeaderError
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, COMM, USLT, TCOM, TCON, TDRC, TRCK, APIC, TSOT, TSOA


def printTags(track):
	# print(track)
	print(track)

def setTrackName(track, name):
	track.add(TSOT(encoding=3, text=name))
	track.add(TIT2(encoding=3, text=name))

def printTrackName(track):
	print('TSOT: '+track['TSOT'])
	print('TIT2: '+track['TIT2'])

def printArtistName(track):
	print('TPE2: '+track['TPE2'])
	print('TSOT: '+track['TPE2'])

def setArtistName(track, name):
	track.add(TPE2(encoding=3, text=name))
	track.add(TSOT(encoding=3, text=name))

def printAlbumName(track):
	print('TALB: '+track['TALB'])
	print('TSOA: '+track['TSOA'])

def setAlbumName(track, name):
	track.add(TALB(encoding=3, text=name))
	track.add(TSOA(encoding=3, text=name))

def printAlbumArt(track):
	img = track['APIC:thumbnail']
	print(img.mime+'\n'+ArtType[img.type]+'\n'+img.desc)

def setAlbumArt(track, imgPath):
	fileType = imgPath[imgPath.rfind('.'):].strip()
	track.add(
		APIC(
			encoding = 3,
			mime = 'image/'+fileType,
			type = 3,
			desc=u'Cover',
			data = open(imgPath).read()
		)
	)

def printTrackNumber(track):
	print('TRCK: '+track['TRCK'])

def setTrackNumber(track, num):
	track.add(TRCK(encoding=3, text=num))

if(len(sys.argv) < 2):
	print("""
	Usage: python TagEdit.py [file path]

	file path - The location of the file (can be from the current directory or a full path)

		""")

	exit()
elif(('/' not in sys.argv[1]) and ('\\' not in sys.argv[1])):
	filePath = './'+sys.argv[1]
else:
	filePath = sys.argv[1]

track = ID3(filePath)

while True:
	resp = input(
		"""
		Select a tag to edit:
	1)	Track
	2)	Artist
	3)	Album
	4)	Cover Art
	5)	Track Number
		"""
	)

	if(resp.strip() == '1'):
		setTrackName(track, input("New track name: "))
	elif(resp.strip() == '2'):
		setArtistName(track, input("New artist name: "))
	elif(resp.strip() == '3'):
		setAlbumName(track, input("New album name: "))
	elif(resp.strip() == '4'):
		setAlbumArt(track, input("Path to new cover art: "))
	elif(resp.strip() == '5'):
		setTrackNumber(track, input("New Track Number: "))

	track.save(filePath)
	cont = input('Edit more tags (Y/N)?: ')
	if(cont != 'y' and cont != 'Y'):
		break




