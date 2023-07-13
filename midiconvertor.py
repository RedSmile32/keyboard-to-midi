import sys
import os
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import math

import pygame
import pygame.midi
import py_midicsv
import csv

import keyboard

midiListData = []
#where the midi data will be stored


def print_devices(): #prints the midi devices connected to the computer
    print("\ndevices:\n")
    for n in range(pygame.midi.get_count()):
        print (n,pygame.midi.get_device_info(n))
        
if __name__ == '__main__':
    pygame.midi.init()
    print_devices()
    
def readInput(input_device): #takes the midi input from the device until a button is pressed
    while True:
        if input_device.poll():
            event = input_device.read(1)
            midiListData.append(event)
            print(event)
        if keyboard.is_pressed('q'):
            print('ending recording')
            break

def checkStart(): #starts recording after the key w is pressed
    going = False
    while going == False:
        if keyboard.is_pressed('w'):
            going = True

#----------------------------------------------------------------

instrument = int(input("enter instrument number (0-127):\n"))
print("\npress 'w' to start recording, press 'q' to end recording. \nPlease do not press any other buttons that are not notes on the piano keyboard.")

checkStart()

if __name__ == '__main__':
    pygame.midi.init()
    try:
        my_input = pygame.midi.Input(1)
        readInput(my_input)
    except:
        print("Device not connected!")

verbatum = midiListData[0][0][1] #verbatum stores the first time a note comes out to avoid akward silences

for x in range(len(midiListData)):
    if midiListData[x][0][0][0] == 144:
        midiListData[x][0][0][0] = "Note_on_c"
    elif midiListData[x][0][0][0] == 128:
        midiListData[x][0][0][0] = "Note_off_c"
    midiListData[x][0][1] -= verbatum -500

with open('midicsv.csv', 'w', newline='') as file:
    writer = csv.writer(file)

    
    writer.writerow([0, 0, "Header", 1, 2, 480])
    writer.writerow([1, 0, "Start_track"])
    writer.writerow([1, 0, "Title_t", '"MIDI SONG"'])
    writer.writerow([1, 0, "Text_t", '"THIS IS A MIDI SONG"'])
    writer.writerow([1, 0, "Copyright_t", '"This file is in the public domain"'])
    writer.writerow([1, 0, "Time_signature", 4, 2, 24, 8])
    writer.writerow([1, 0, "Tempo", 500000])
    writer.writerow([1, 0, "End_track"])
    writer.writerow([2, 0, "Start_track"])
    writer.writerow([2, 0, "Instrument_name_t", '"Arbitrary Instrument"'])
    writer.writerow([2, 0, "Program_c", 1, instrument])
    for x in range(len(midiListData)):
        writer.writerow([2, midiListData[x][0][1], midiListData[x][0][0][0] , 1,  midiListData[x][0][0][1], midiListData[x][0][0][2]])
        #above is track, timestamp, status, data1, data2, data3
    writer.writerow([2, midiListData[len(midiListData)-1][0][1], "End_track"])
    writer.writerow([0, 0, "End_of_file"])

# Parse the CSV output into a MIDI file
midi_object = py_midicsv.csv_to_midi("midicsv.csv")


# Save the parsed MIDI file to disk
with open("midicsv.mid", "wb") as output_file:
    midi_writer = py_midicsv.FileWriter(output_file)
    midi_writer.write(midi_object)