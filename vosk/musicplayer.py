from os import system
import subprocess

def next_track():
    system("audacious -f")

def previous_track():
    system("audacious -f")

def launch(gui=True):
    """
    gui: shows a window (Graphical User Interface)
    """
    #system("export DISPLAY=:0") # Works without it so far
    if gui:
        system("audacious -1 -p &")
    else:
        system("audacious -1 -H &")

def stop():
    system("audacious -s")
    system("pkill audacious")

def pause():
    system("audacious -u")

def play_medieval():
    system("audacious -E '/home/phileas/Musics/Relaxing Medieval, Middle Ages Music 10 Hours-5F5dgg1eeGE.mp3'")

def play_lofi():
    system("audacious -E '/home/phileas/Musics/Backpack City.mp3'")