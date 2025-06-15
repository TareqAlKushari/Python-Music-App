import os
import pickle
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
from pygame import mixer

class player(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        #self.v = self.volume.get()
        self.master = master
        self.pack()

        mixer.init()

        if os.path.exists("G:/Music_me/Rajaa Belmir - Karari (EXCLUSIVE Music Video) 2020(MP3_160K).mp3.pickle"):
            with open("G:/Music_me/Rajaa Belmir - Karari (EXCLUSIVE Music Video) 2020(MP3_160K).mp3.pickle", "rb") as f:
                self.playlist = pickle.load(f)
        else:
            self.playlist = []

        self.current = 0
        self.paused = True
        self.played = False

        self.create_frames()
        self.track_widgets()
        self.control_widgets()
        self.tracklist_widgets()
    def create_frames(self):
        self.track = tk.LabelFrame(self, text="Song Track", font=("times new roman", 15, "bold"), bg="grey", fg="white", bd=5, relief=tk.GROOVE)
        self.track.config(width=410, height=300)
        self.track.grid(row=0, column=0, padx=10)

        self.tracklist = tk.LabelFrame(self, text=f"playlist - {str(len(self.playlist))}", font=("times new roman",15,"bold"),bg="grey",fg="white",bd=5,relief=tk.GROOVE)
        self.tracklist.config(width=190,height=400)
        self.tracklist.grid(row=0,column=1,rowspan=3,pady=5)

        self.controls = tk.LabelFrame(self,font=("times new roman",15,"bold"),bg="white",fg="white",bd=2,relief=tk.GROOVE)
        self.controls.config(width=410,height=80)
        self.controls.grid(row=2,column=0,pady=5,padx=10)

    def track_widgets(self):
        self.canvas = tk.Label(self.track, image=img)
        self.canvas.configure(width=400, height=240)
        self.canvas.grid(row=0, column=0)

        self.songtrack = tk.Label(self.track, font=("times new roman", 15, "bold"), bg="white", fg="dark blue")
        self.songtrack["text"] = "Musicxy MP3 Player"
        self.songtrack.configure(width=30, height=1)
        self.songtrack.grid(row=1, column=0)

    def control_widgets(self):
        self.loadSongs = tk.Button(self.controls, bg="green", fg="white", font=10)    #كمل ال font حق ال Button يمكن عادوه ناقص
        self.loadSongs["text"] = "Load Songs"
        self.loadSongs["command"] = self.retrieve_songs
        self.loadSongs.grid(row=0, column=0, padx=10)

        self.prev = tk.Button(self.controls, image=prev)
        self.prev["command"] = self.prev_song
        self.prev.grid(row=0, column=1)

        self.pause = tk.Button(self.controls, image=pause)
        self.pause["command"] = self.pause_song
        self.pause.grid(row=0, column=2)

        self.next = tk.Button(self.controls, image=next_)
        self.next["command"] = self.next_song
        self.next.grid(row=0, column=3)

        self.volume = tk.DoubleVar(self)
        self.slider = tk.Scale(self.controls, from_=0, to=10, orient=tk.HORIZONTAL)
        self.slider["variable"] = self.volume
        self.slider.set(8)
        mixer.music.set_volume(0.8)
        self.slider["command"] = self.change_volume
        self.slider.grid(row=0, column=4, padx=5)

    def tracklist_widgets(self):
        self.scrollbar = tk.Scrollbar(self.tracklist, orient=tk.VERTICAL)
        self.scrollbar.grid(row=0, column=1, rowspan=5, sticky="ns")

        self.list = tk.Listbox(self.tracklist, selectmode=tk.SINGLE, yscrollcommand=self.scrollbar.set, selectbackground="sky blue")
        self.enumerate_songs()
        self.list.config(height=22)
        self.list.bind("<Double-1>", self.play_song)

        self.scrollbar.config(command=self.list.yview)
        self.list.grid(row=0, column=0, rowspan=5)

    #def enumerate_songs(self):
        #for index, song in enumerate(self.playlist):
            #self.list.insert(index, os.path.basename(song))

    def retrieve_songs(self):
        self.songlist = []
        directory = filedialog.askdirectory()
        for root_, dirs, files in os.walk(directory):
            for file in files:
                if os.path.splitext(file)[1] == ".mp3":
                    path = (root_ + '/' + file).replace('//', '/')
                    self.songlist.append(path)

        with open("D:/Music/اغاني/Rajaa Belmir - Karari (EXCLUSIVE Music Video) 2020(MP3_160K).mp3.pickle", "wb") as f:
            pickle.dump(self.songlist, f)
        self.playlist = self.songlist
        self.tracklist["text"] = f"playlist - {str(len(self.playlist))}"
        self.list.delete(0, tk.END)
        self.enumerate_songs()

    def enumerate_songs(self):
        for index, song in enumerate(self.playlist):
            self.list.insert(index, os.path.basename(song))

    def play_song(self, event=None):
        if event is not None:
            self.current = self.list.curselection()[0]
            for i in range(len(self.playlist)):
                self.list.itemconfigure(i, bg="white")

        print(self.playlist[self.current])
        mixer.music.load(self.playlist[self.current])
        #self.songtrack["anchor"] = "w"
        #self.songtrack["text"] = os.path.basename(self.playlist[self.current])

        self.pause["image"] = play
        self.paused = False
        self.played = True
        self.songtrack["anchor"] = "w"
        self.songtrack["text"] = os.path.basename(self.playlist[self.current])
        self.list.activate(self.current)
        self.list.itemconfigure(self.current, bg="sky blue")

        mixer.music.play()

    def pause_song(self):
        if not self.paused:
            self.paused = True
            mixer.music.pause()
            self.pause["image"] = pause
        else:
            if self.played != False:
                pass
            else:
                self.play_song()
            self.paused = False
            mixer.music.unpause()
            self.paused["image"] = play

    def prev_song(self):
        if self.current > 0:
            self.current -= 1
        else:
            self.current = 0
        self.list.itemconfigure(self.current+1, bg="white")
        self.play_song()

    def next_song(self):
        if self.current < len(self.playlist) - 1:
            self.current += 1
        else:
            self.current = 0
            self.play_song()
        self.list.itemconfigure(self.current-1, bg="white")
        self.play_song()

    def change_volume(self, event=None):
        self.v = self.volume.get()
        mixer.music.set_volume(self.v / 10)

root = tk.Tk()
root.geometry('600x400')
root.wm_title('Musicxy MP3 Player')


def photoImage(file):
    pass


#img = photoImage(file='free_fast')
#next_ = photoImage(file='free_fast')
#prev = photoImage(file='free_fast')
#play = photoImage(file='free_fast')
#pause = photoImage(file='free_fast')

img = ImageTk.PhotoImage(Image.open("musical-note (1).png"))
next_ = ImageTk.PhotoImage(Image.open("fast-backward (2).png"))
prev = ImageTk.PhotoImage(Image.open("fast-forward (2).png"))
play = ImageTk.PhotoImage(Image.open("play.png"))
pause = ImageTk.PhotoImage(Image.open("pause (2).png"))
#stop_btn_img = ImageTk.PhotoImage(Image.open("stop (2).png"))


app = player(master=root)
app.mainloop()