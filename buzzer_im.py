#!/usr/bin/env python3
# buzzer, improved (release 180118-0945)
# released under GNU General Public License
# Copyright 2017, 2018 Aswin Babu K

import threading
# ATTENTION!
# configure amixer '-c' switch argument as per your soundcard
# configure keyboard event IDs
global flag
output =[]
# import all the serious stuff
import pyinotify # monitor the FS. In our case, input devices
from datetime import datetime # for creating time stamps
import signal # helps to kill the program after x seconds
import subprocess # very useful to invoke *NIX commands
import os # for debugging purposes

# function using Notifier class
def watch_notifier(directory, ignore_path, output_file):
    processed_inputs = []
    watch_manager = pyinotify.WatchManager() # add watch
    mask = pyinotify.IN_ACCESS # watch for dev file access
    
    class EventHandler(pyinotify.ProcessEvent):
        def process_IN_ACCESS(self, event): # function for file access event
            time_stamp = datetime.now().strftime('%H:%M:%S:%f') # get time
            if event.pathname not in ignore_path: # ignore the master keyboard
                if event.pathname not in processed_inputs: # ignore pressed
                    subprocess.call('aplay -q beep.wav&', shell=True) # buzz
                    subprocess.call('sleep .5 && amixer -q -c 0 set Master 0%',
                                    shell=True) # reduce volume to 0%
                    
                    # create output, print to stdout and file
                    output.append('time:' + time_stamp + '\tdevice:' + event.pathname)
                    #print(output)
                    
                    #output_file.write(output + '\n')
                    
                    processed_inputs.append(event.pathname)

    # the below code initializes watching the fs
    handler = EventHandler()
    notifier = pyinotify.Notifier(watch_manager, handler)
    wd_dict = watch_manager.add_watch(directory, mask, rec=True)
    notifier.loop()


# this function is supposed to handle things when time expires
def handler(signum, frame):
    print("Timeout") # this is printed when the program exits
    raise Exception("time expired")


# the main function
def main():
    flag=0
    mflag=0
    # below two variables exist for ease of access
     
  

    # write output to file
    output_file = open('output_file', 'a')

    # paths to be ignored
    ignore_path = ['/dev/input/by-id', '/dev/input/by-path']
    testfile = open("home.txt","r")
    temp= testfile.readline()
    ignore_path.append(temp[:-1])
    temp= testfile.readline()
    ignore_path.append(temp[:-1])
    temp = testfile.readline()
    ignore_path.append(temp[:-1])

    subprocess.call('stty -echo', shell=True) # turns off keyboard echo
    subprocess.call('amixer -q -c 0 set Master 70%', shell=True)
    subprocess.call('clear', shell=True) # clears the terminal window
    print("Time starts") # very useful for identifying individual questions

    signal.signal(signal.SIGALRM, handler) # set signal and handler function
    signal.alarm(10) # raise alarm after 10 seconds

    try:
        watch_notifier('/dev/input', ignore_path, output_file) # start watching
    except Exception:
    #   #use the beep command to generate phaser sound
        subprocess.call('aplay -q timeout.wav', shell=True)
        subprocess.call('stty echo', shell=True) # turns on echo
        subprocess.call('amixer -q -c 0 set Master 100%', shell=True) # unmute
    
    # write newline and close the file
    #output_file.write('\n')
 #   output_file.close()


# call the main function
from tkinter import *
from tkinter import messagebox
class Window(Frame):


    def __init__(self, master=None):
        Frame.__init__(self, master)                 
        self.master = master
        self.init_window()

    #Creation of init_window
    def init_window(self):

        # changing the title of our master widget      
        self.master.title("QUIZ")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        # creating a button instance
        setupButton = Button(self, text="setup",command = setup)
        startQuiz = Button(self,text = "start quiz",command = main)
        showResult = Button(self,text = "show result",command = show)
        # placing the button on my window
        setupButton.place(x=260, y=260)
        startQuiz.place(x=260 , y= 300)
        showResult.place(x=260,y=350)
 
n = open("tempdisp","w")
def setup():
    os.system("python3 test.py")
def show():
    temp ='\n'
    n = open("tempdisp","w")
    for i in range (0,len(output)):
        temp = temp +output[i][-1]+'\n'
    messagebox.showinfo("Result",temp)
    for i in range (0,len(output)):
        output.pop()
root = Tk()

#size of the window
root.geometry("600x600")

app = Window(root)
T = Text(root, height=2, width=70)
T.pack()
T.insert(END, "After pressing setup press any button on the quiz master keyboard\nthen right and left click the mouse \n")
root.mainloop()  

