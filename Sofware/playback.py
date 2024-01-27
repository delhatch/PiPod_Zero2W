import vlc
import random
import alsaaudio
import os
import csv
import taglib

class music():
    volume = 60
    playlist = [["", "", "", ""]]
    currentSongIndex = 0
    
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
                if file.endswith('.mp3') or file.endswith('.m4a') or file.endswith('.wav') or file.endswith('.wma'):
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
                tags = audiofile.tags
            except:
                print("Error parsing tags")
                pass
            # Check to see if the "ARTIST" field is empty.
            #    If so, copy in the info from the "ALBUMARTIST" field.
            try:
                if( tags["ARTIST"] == [] ):
                    # If here, there WAS an ARTIST entry, and it was empty.
                    #print("Found an empty ARTIST field")
                    #print(tags["ARTIST"])
                    tags["ARTIST"] = ['NOT SURE ARTIST']  # Found none of these
                    #print(tags["ARTIST"])
            except:
                # If here, there was no entry for ARTIST. Empty/void/null field.
                tags["ARTIST"] = ['Not Sure ARTIST']  # Found 26 of these
            # Check to see if the "ALBUM" field is empty.
            #    If so, fill it in with "Not Sure"
            try:
                if( tags["ALBUM"] == [] ):  # This is true semi-frequently for my MP3 files
                    #pass
                    #print("Found an empty ALBUM field")
                    tags["ALBUM"] = ['NOT SURE ALBUM']  # Found 1635 of these
                    #print(tags["ALBUM"])
            except:
                tags["ALBUM"] = ['Not Sure ALBUM']   # Found 174 of these
            # Check to see if the "TITLE" field is empty.
            #    If so, fill it in with "Not Sure"
            try:
                if( tags["TITLE"] == [] ):  # Never
                    #pass
                    #print("Found an empty TITLE field")
                    tags["TITLE"] = ['NOT SURE TITLE']  # None of these
                    #print(tags["ALBUM"])
            except:
                tags["TITLE"] = ['Not Sure TITLE'] # Found 41 of these
            try:
                writer.writerow((i, tags["ARTIST"][0], tags["ALBUM"][0], tags["TITLE"][0]))
            except AttributeError:
                print("Attribute Error", i)
            except:
                print("Unknown write error",i)
                try:
                    print(tags["ARTIST"])
                except:
                    pass
                try:
                    print(tags["ALBUM"])
                except:
                    pass
                try:
                    print(tags["TITLE"])
                except:
                    pass
        print("Done")
        file.close()

        return 1
