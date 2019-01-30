import sys
import enum
from mutagen.mp3 import MP3
from mutagen.id3 import ID3NoHeaderError
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, COMM, USLT, TCOM, TCON, TDRC, TRCK, APIC, TSOT

##READ/WRITE##
# track name
# artist name
# album name
# album art
# track number

ArtType = [
	'Other',
	'32x32 pixels \'file icon\' (PNG only)',
	'Other file icon',
	'Cover (front)',
	'Cover (back)',
	'Leaflet page',
	'Media (e.g. label side of CD)',
	'Lead artist/lead performer/soloist',
	'Artist/performer',
	'Conductor',
	'Band/Orchestra',
	'Composer',
	'Lyricist/text writer',
	'Recording Location',
	'During recording',
	'During performance',
	'Movie/video screen capture',
	'Illustration',
	'Band/artist logotype',
	'Publisher/Studio logotype'
]


def printTags(track):
	# print(track)
	print(ArtType[0])

def setTrackName(track, name)
	track['TSOT'] = name
	track['TIT2'] = name

def printTrackName(track):
	print('TSOT: '+track['TSOT'])
	print('TIT2: '+track['TIT2'])

def printArtistName(track):
	print('TPE2: '+track['TPE2'])
	print('TSO2: '+track['TPE2'])

def setArtistName(track, name)
	track['TPE2'] = name
	track['TSO2'] = name

def printAlbumName(track):
	print('TALB: '+track['TALB'])
	print('TSOA: '+track['TSOA'])

def setAlbumName(track, name)
	track['TALB'] = name
	track['TSOA'] = name

def printAlbumArt(track):
	img = track['APIC:thumbnail']
	print(img.mime+'\n'+ArtType[img.type]+'\n'+img.desc)

printAlbumArt(ID3(sys.argv[1]))