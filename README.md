# RecordingAssistant
Helps to record lines from a csv file with audacity and saves them

Primarily intended for facilitating the recording of audio files for Jackbox mods/translations.
Uses pipeclient.py (Copyright Steve Daulton 2018) as a module. (https://github.com/audacity/audacity/blob/master/scripts/piped-work/pipeclient.py)

1. To use, fill out the csv file according to the file 'format.csv'. It is important that the yellow fields are filled out. Name your file 'example'.
2. Please do at all times have a backup file that is NOT named 'backup.csv'. The program sometimes overwrites the existing csv files when abruptly closed.
3. Save all files in the SAME folder as the folder containing the game files of the game you are working on. (This only matters if you want to use the function 'play Original file').
4. (When using the program for the first time, you must enable the mod-script-pipe in audacity: 
      - Run Audacity
      - Go into Edit > Preferences > Modules
      - Choose mod-script-pipe (which should show New) and change that to Enabled. 
      - Restart Audacity
      - Check that it now does show Enabled.)
5. Every time you are using the RecordingAssistant, open Audacity manually before opening the RecordingAssistant!
6. Open recordingAssistantExe.exe (or alternatively run recordingAssistant.py in the Command Prompt window).
7. Start recording!


