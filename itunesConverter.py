import elementtree.ElementTree as ET
import re


class Track:
    def __init__(self, key):
        self.key = key
        self.artist = ""
        self.filename = ""
        self.album = "Unknown"
        self.tracknumber = "00"
        
        
class Playlist:
    def __init__(self, name):
        self.name=name
        self.tracks=[]

class Library:
    def __init__(self):
        self.tracks = dict()#Track ID
        self.playlists = dict()#Playlist Name

##def convertToType(element as ET.Element):
##    return {
##        'dict': dict(),
##        'array': [],
##        'key': element.text,
##        'integer': int(element.text),
##        'string' : element.text,
##        'date' : element.text,
##        'true' : True,
##        'false' : False,
##        'plist' : 
##    }[element.tag]

print "Loading iTunes XML Data...\n"
dontallow = ["iTunes DJ", "Baby Belle", "CD para Silvia", "Genius", "Movies", "Music", "Podcasts", "Silvia", "TV Shows", "What The H!??!!"]
dest = "C:\Users\Brian\Music\\"
source = open("Library.xml", 'r')
data = source.read()
udata = data.decode("utf-8")
asciidata=udata.encode("ascii","ignore")
elementTable=ET.fromstring(asciidata)
itunesLib = elementTable.getchildren()[0]#gets main dictionary
libraryList=itunesLib.getchildren()
library = Library()

print "Loading Tracks...\n"

for i, element in enumerate(libraryList):
    if element.text=="Tracks":
        tracksElement=libraryList[i+1]
        for trk in tracksElement.getchildren():
            if trk.tag=="dict":
                track =None
                trackInfo=trk.getchildren()
                for j, val in enumerate(trackInfo):
                    if val.text=="Track ID":
                        track = Track(trackInfo[j+1].text)
                    elif val.text=="Name":
                        track.filename = re.sub('_', ' ', trackInfo[j+1].text)
                    elif val.text=="Artist":
                        track.artist = re.sub('[/]', '-', trackInfo[j+1].text)
                    elif val.text=="Album":
                        track.album = re.sub('[/]', '-', trackInfo[j+1].text)
                    elif val.text=="Kind":
                        kind = trackInfo[j+1].text
                        if kind=="MPEG audio file":
                            track.filename =  track.filename + ".mp3"
                        elif kind=="AAC audio file":
                            track.filename =  track.filename + ".m4a"
                    elif val.text=="Track Number":
                        track.tracknumber=trackInfo[j+1].text
                library.tracks[track.key] = track

        print "Finished Loading Tracks!! Loading Playlists...\n"
              
    elif element.text=="Playlists":
        playlistElement=libraryList[i+1]
        playlist = None
        for playlistDict in playlistElement.getchildren():
            for j, playlistInfo in enumerate(playlistDict):
                if playlistInfo.text=="Name":
                    playlist = Playlist(playlistDict[j+1].text)
                elif playlistInfo.text=="Playlist Items":
                    trackz = playlistDict[j+1].getchildren()
                    for t in trackz:
                        playlist.tracks.append(t.getchildren()[1].text)
            library.playlists[playlist.name] = playlist

print "Finished Loading Tracks and Playlists!! Writing M3U File...\n"

output = None
artist = None
for key in library.playlists.keys():
   if not key in dontallow: 

    output = open(key + ".m3u", 'w')
    output.write("#Playlist: '" + key + ".m3u" + "' \n")

    for track in library.playlists[key].tracks:
        if(library.tracks.has_key(track)):
            track = library.tracks[track]
            if track.artist.endswith("."):
                artist=track.artist[0:len(track.artist)-1]
                print artist
                output.write(dest)
                output.write(artist + "\\")
            else:
                output.write(dest)
                output.write(track.artist + "\\")
            output.write(track.album + "\\")
            #output.write(track.tracknumber + " - ")
            output.write(track.artist + " - ")
            output.write(track.filename + "\n")
print "Successful M3U Conversion"
output.close()
source.close()
    

