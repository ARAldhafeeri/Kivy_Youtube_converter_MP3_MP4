#-*_coding: utf-8-*-


import os

from pytube import YouTube
import sys
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import ObjectProperty
from kivy.uix.actionbar import ActionBar
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from database import Database
from kivy.uix.image import AsyncImage
import moviepy.editor as mp
from kivy.clock import Clock
import re
from os import listdir
from kivy.uix.progressbar import ProgressBar
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty


kv = Builder.load_file("FrontEnd.kv")
database=Database("data.db")


class Downloader(Screen):
    def __init__(self, *args, **kwargs):
        super(Downloader, self).__init__(**kwargs)
        self.update_bar_trigger = Clock.create_trigger(self.update_bar)

    def clicked(self):
        self.i = 0
        self.update_bar_trigger()

    def update_bar(self, dt):
        if self.i <= 10000:
            self.ids.pb.value += self.i
            self.i += 1
            self.update_bar_trigger()

    def mp4(self):
        # user entered a link.
        try:
            self.link = self.ids.link_input.text
            self.yt = YouTube(self.link)
            self.videoname = str(self.yt.title)
            self.videoimage = self.yt.thumbnail_url
            self.yt = YouTube(self.link).streams.get_highest_resolution()
            remove_punctuation_map = dict((ord(char), None) for char in '/\*?:"<>|.')
            self.videoname = self.videoname.translate(remove_punctuation_map)
            self.filepath = os.path.join(os.getcwd(),'Downloads_mp4',self.videoname+'.mp4')
            Manager.list_of_video_names.append(self.videoname)
            Manager.list_of_video_paths.append(self.filepath)
            Manager.list_of_video_images.append(self.videoimage)
            # Insert downloaded video data into our postgresSQL database
            try:
                database.insert(Manager.list_of_video_names[0],
                Manager.list_of_video_paths[0],
                Manager.list_of_video_images[0])
            except:
                print('error cant insert data into the database')

                    # Clear our list once added the data to our database
            try:
                Manager.list_of_video_names.clear()
                Manager.list_of_video_paths.clear()
                Manager.list_of_video_images.clear()
            except:
                print('indexError')
                    #print(self.list_from_database)

            try:
                os.mkdir('Downloads_mp4')
            except:
                print('Error! Folder is already created!')

            try:
                self.yt.download(os.path.join(os.getcwd(),'Downloads_MP4'))
            except:
                print('Error!! video can not be downloaded')
        except:
                self.ids.link_input.text = 'Please enter a youtube link'

    def mp3(self):
        # user entered a link.
        try:
            self.link = self.ids.link_input.text
            self.yt = YouTube(self.link)
            self.videoname = str(self.yt.title)
            self.videoimage = self.yt.thumbnail_url
            self.yt = YouTube(self.link).streams.get_highest_resolution()
            remove_punctuation_map = dict((ord(char), None) for char in '/\*?:"<>|.')
            self.videoname = self.videoname.translate(remove_punctuation_map)
            self.filepath = os.path.join(os.getcwd(),'Downloads_MP3',self.videoname+'.mp3')
            Manager.list_of_video_names.append(self.videoname)
            Manager.list_of_video_paths.append(self.filepath)
            Manager.list_of_video_images.append(self.videoimage)
            # Insert downloaded video data into our postgresSQL databas
            database.insert(Manager.list_of_video_names[0],
            Manager.list_of_video_paths[0],
            Manager.list_of_video_images[0])


            try:
                Manager.list_of_video_names.clear()
                Manager.list_of_video_paths.clear()
                Manager.list_of_video_images.clear()
            except:
                print('indexError')
                #print(self.list_from_database)

            try:
                Manager.list_of_video_names.clear()
                Manager.list_of_video_paths.clear()
                Manager.list_of_video_images.clear()
            except:
                print('indexError')
                    #print(self.list_from_database)

            try:
                os.mkdir('Downloads_MP3')
            except:
                print("foloder already created.")


            try:
                self.yt.download(os.path.join(os.getcwd(),'Downloads_MP3'))

            except:
                print("error! can't download video")

            self.folder = os.path.join(os.getcwd(),'Downloads_MP3')
            print(self.folder)
            for self.file in [self.n for self.n in os.listdir(self.folder) if re.search('mp4',self.n)]:
                self.full_path = os.path.join(self.folder, self.file)
                self.output_path = os.path.join(self.folder, os.path.splitext(self.file)[0] + '.mp3')
                self.clip = mp.AudioFileClip(self.full_path).subclip(10,)
                    # disable if do not want any clipping
                self.clip.write_audiofile(self.output_path)

                            # except:
                            #     print('Error! conversion method did not work!')
            self.list_item_in_folder= os.listdir(self.folder)
            for self.item in self.list_item_in_folder:
                if self.item.endswith(".mp4"):
                    os.remove(os.path.join(os.getcwd(),'Downloads_MP3',self.item))

        except:
            self.ids.link_input.text = 'Please enter a youtube link'

# Gallery screen Backend


class Gallery(Screen):

    def __init__(self,*a, **kw):
        super(Gallery, self).__init__(**kw)

    def on_pre_enter(self,*args):
        Manager.list_from_database.clear()
        try:
            for self.row in database.view():
                Manager.list_from_database.append(self.row)
        except:
            print('Database is empty!')

        print(Manager.list_from_database)
        self.Scroll_content = self.ids.scroll_view
        self.layout = GridLayout(cols=1, spacing=5,size_hint_y=2)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        for self.item in Manager.list_from_database:
            self.current_file_path = self.item[2]
            self.title = self.item[1]
            self.btn = Button(
                            text=self.title,
                            font_size=8,
                            size_hint= (.2,.05),
                            background_color=(1.0, 0.0, 0.0, 1.0)
                            )
            self.image = AsyncImage(source =self.item[3],
                                    size_hint= (.4,.2),
                                    )
            self.btn.bind(on_press=(self.call_back))
            # print(self.item[2])
            self.layout.add_widget(self.image)
            self.layout.add_widget(self.btn)
        self.Scroll_content.clear_widgets()
        self.Scroll_content.add_widget(self.layout)

    def call_back(self, instance):
        self.title = str(instance.text)
        # self.manager.current = 'myvideoplayer'
        for self.item in Manager.list_from_database:
            print(self.item)
            if self.title == self.item[1]:
                self.manager.myvideoplayer.test_on_enter(self.item[2])
                # startfile(self.item[2])
                break

# Video Player backend


class MyVideoPlayer(Screen):
    def __init__(self, **kwargs):
        super(MyVideoPlayer, self).__init__(**kwargs)

    def test_on_enter(self,file_path):
        self.file_path = file_path
        try:
            os.startfile(r"{}".format(self.file_path))
        except:
            print('Error cant open file')
        # self.player =VideoPlayer(source=self.file_path,
        #                         state='play',
        #                         options={'allow_stretch':False,'eos': 'loop'})
        # self.add_widget(self.player)

    def onBackBtn(self):
        self.manager.current = 'gallery'
        try:
            self.player.state = 'stop'
        except:
            print('Error user is not playing a video')

    def on_leave(self):
        pass


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class FileChosser(Screen):
    def __init__(self, **kwargs):
        super(FileChosser, self).__init__(**kwargs)
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)


    def get_current_path(self):
        return os.getcwd()

    def load(self, path, filename):

        print(path)
        print(filename)
        self.filename = filename[0]
        self.path = path
        os.startfile(self.filename)


# Guide Screen backend

class Guide(Screen):
    def __init_(self, **kwargs):
        super(Guide, self).__init__( **kwargs)
    filepath = os.path.join(os.getcwd(),'Downloads')

    def get_path_name(self):
        try:
            return  str(self.filepath)
        except:
            print('Error!!')

# Manager screens backend


class Manager(ScreenManager):
    downloader = ObjectProperty(None)
    guide = ObjectProperty(None)
    gallery = ObjectProperty(None)
    myvideoplayer = ObjectProperty(None)
    filechosser = ObjectProperty
    transition = FadeTransition()
    list_of_video_names = []
    list_of_video_paths = []
    list_of_video_images = []
    list_from_database = []

    def __init_(self, **kwargs):
        super(Manager, self).__init__(**kwargs)

class MyApp(App):

    def build(self):
        self.title = 'Downloader'
        return Manager()


if __name__ == '__main__':
    MyApp().run()
