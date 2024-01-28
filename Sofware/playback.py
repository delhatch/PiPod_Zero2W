import vlc
import random
import alsaaudio
import os
import csv
import taglib


class music():
    UseMeta = False  # If False, use MP3 filename as the source of title/artist metadata.
                     # If True,  use the metadata inside the MP3 file.
    volume = 60
    playlist = [["", "", "", ""]]
    currentSongIndex = 0
    AlbumNoKey = 0
    AlbumEmptyField = 0
    ArtistNoKey = 0
    ArtistEmptyField = 0
    TitleNoKey = 0
    TitleEmptyField = 0

    def __init__(self):
        self.vlcInstance = vlc.Instance()
        self.player = self.vlcInstance.media_player_new()
        self.alsa = alsaaudio.Mixer(alsaaudio.mixers()[0])
        self.alsa.setvolume(self.volume)

    def getStatus(self):
        status = {
            "songLength": self.player.get_length(),
            "currentTime": self.player.get_time(),
            "currentSong": self.playlist[self.currentSongIndex],
            "volume": self.alsa.getvolume()[0],
            "playlist": self.playlist
        }
        return status

    def loop(self):
        if self.player.get_state() == vlc.State.Ended and self.currentSongIndex < len(self.playlist)-1:
            self.currentSongIndex += 1
            self.play()

    def loadList(self, songList):
        self.playlist = songList
        self.currentSongIndex = 0
        self.play()

    def updateList(self, newList):
        if self.playlist[0] == ["", "", "", ""]:
            self.playlist.pop(0)
            self.playlist = newList
            self.currentSongIndex = 0
            self.play()
        else:
            self.currentSongIndex = newList.index(self.playlist[self.currentSongIndex])
            self.playlist = newList

    def play(self):
        #print(currentSong)
        self.player.set_media(self.vlcInstance.media_new_path(self.playlist[self.currentSongIndex][0]))
        print("About to play.")
        self.player.play()

    def playAtIndex(self, index):
        self.currentSongIndex = index
        self.player.set_media(self.vlcInstance.media_new_path(self.playlist[self.currentSongIndex][0]))
        self.player.play()

    def playPause(self):
        if self.player.get_state() == vlc.State.Playing:
            self.player.pause()
        elif not self.player.get_state() == vlc.State.Playing:
            self.player.play()

    def shuffle(self):
        # Before shuffling remove the already played songs to make sure these don't get played again
        tempPlaylist = self.playlist[self.currentSongIndex + 1::]
        random.shuffle(tempPlaylist)
        # Add the already played songs to the front again
        self.playlist = self.playlist[:self.currentSongIndex + 1] + tempPlaylist

    def clearQueue(self):
        self.playlist = [["", "", "", ""]]
        self.currentSongIndex = 0
        self.player.stop()

    def next(self):
        if self.currentSongIndex < len(self.playlist)-1:
            self.currentSongIndex += 1
            self.play()

    def prev(self):
        if self.currentSongIndex > 0:
            self.currentSongIndex -= 1
            self.play()

    def volumeUp(self):
        if self.volume <= 95:
            self.volume += 5
            self.alsa.setvolume(self.volume)
            print(self.volume)

    def volumeDown(self):
        if self.volume > 5:
            self.volume -= 5
            self.alsa.setvolume(self.volume)

    def updateLibrary(self):
        self.playPause()
        fileList = []
        print("Updating metadata")
        #musicPath = "/home/pi/musicPlayer/Music/"
        musicPath = "/home/drh/Music/"

        for path, dirs, files in os.walk(musicPath):
            for file in files:
                if file.endswith('.mp3') or file.endswith('.MP3') or file.endswith('.Mp3') or file.endswith('.m4a') or file.endswith('.wav') or file.endswith('.wma'):
                    fileList.append(os.path.join(path, file))
                    #print(os.path.join(path, file))
        '''
            for f in files:
                filename = os.path.join(root, f)
                if filename.endswith('.mp3'):
                    fileList.append(filename)
        '''
        file = open("info.csv", "w", newline="")
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

        # print("Saving metadate")
        for i in fileList:
            try:
                audiofile = taglib.File(i)
                song = audiofile.tags
            except:
                print("Error parsing tags")

            if self.UseMeta:  # Metadata source = metadata in the MP3 file.
                # Check to see if the "ARTIST" field is empty, or does not exist.
                #    If so, fill it in with "Not Sure"
                if( 'ARTIST' in song ):
                    if( song['ARTIST'] == [] ):  # Key exists, but points to empty field.
                        self.ArtistEmptyField += 1
                        song['ARTIST'] = ['NOT SURE ARTIST']  # Found none of these
                    else:
                        pass  # Artist field was filled in. Is legit.
                else:
                    self.ArtistNoKey += 1
                    song['ARTIST'] = ['Not Sure ARTIST']   # Found 26 of these

                # Check to see if the "TITLE" field is empty, or does not exist.
                #    If so, fill it in with "Not Sure"
                if( 'TITLE' in song ):
                    if( song['TITLE'] == [] ):  # Key exists, but points to empty field.
                        self.TitleEmptyField += 1
                        song['TITLE'] = ['NOT SURE TITLE']  # Found none of these
                    else:
                        pass  # Album field was filled in. Is legit.
                else:
                    self.TitleNoKey += 1
                    song['TITLE'] = ['Not Sure TITLE']   # Found 41 of these

            else:   # Metadata source = the MP3 filename string.
                # MP3 filenames must look exactly like this:
                #    "/home/path/user/Thisartist - Thistitle.mp3"
                artist = i.split(" -")
                newartist = artist[0].split("/")
                stringArtist = newartist[4].lstrip()
                song['ARTIST'] = [stringArtist]
                try:
                    title = i.split("- ")
                except:
                    print("Error splitting!",i)
                try:
                    newtitle = title[1].split(".")
                except:
                    print("Error splitting",i)
                stringTitle = newtitle[0].lstrip()
                song['TITLE'] = [stringTitle]

            # Check to see if the "ALBUM" field is empty, or does not exist.
            #    If so, fill it in with "Not Sure"
            if( 'ALBUM' in song ):
                if( song['ALBUM'] == [] ):  # Key exists, but points to empty field.
                    self.AlbumEmptyField += 1
                    song['ALBUM'] = ['NOT SURE ALBUM']  # Found 1635 of these
                else:
                    pass  # Album field was filled in. Is legit.
            else:
                self.AlbumNoKey += 1
                song['ALBUM'] = ['Not Sure ALBUM']   # Found 174 of these

            # At this point, the following writer call should never fail.
            try:
                writer.writerow((i, song["ARTIST"][0], song["ALBUM"][0], song["TITLE"][0]))
            except AttributeError:
                print("Attribute Error", i)
            except:
                print("Unknown write error",i)
                try:
                    print(song["ARTIST"])
                except:
                    pass
                try:
                    print(song["ALBUM"])
                except:
                    pass
                try:
                    print(song["TITLE"])
                except:
                    pass
        file.close()
        print("Done writing metadata file.")
        print("AlbumNoKey = ", self.AlbumNoKey)
        print("AlbumEmptyField = ", self.AlbumEmptyField)
        print("ArtistNoKey = ", self.ArtistNoKey)
        print("ArtistEmptyField = ", self.ArtistEmptyField)
        print("TitleNoKey = ", self.TitleNoKey)
        print("TitleEmptyField = ", self.TitleEmptyField)
        return 1
