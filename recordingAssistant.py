#! python3
# program that eases workflow when recording with audacity: shows phrase from csv-file to be recorded, records and saves file correctly. 

import os, csv, sys, subprocess, tkinter as tk, pipeclient, textwrap, atexit
from idlelib.tooltip import Hovertip
client = pipeclient.PipeClient()

#sets Jackbox folder as cwd
os.chdir(os.path.realpath(__file__).replace('recordingAssistant.py', ''))
cwd = os.getcwd()

root= tk.Tk()
root.geometry('500x300')
root.title('Recording Assistant - remember to open Audacity')

try: 
    client.write('Message:')
    inf = open('example.csv', encoding='utf-8')
    reader = csv.reader(inf.readlines())
    text = list(reader)

    outf = open('example.csv', 'w', newline = '', encoding='utf-8')
    writer = csv.writer(outf)

    backup = open('backup.csv', 'w', newline = '', encoding='utf-8')
    writer2 = csv.writer(backup)
    writer2.writerows(text)
except PipeClientError:
    sys.exit()

rowNumber = 2
while text[rowNumber][4].lower == 'x':
    rowNumber += 1
tries = {}
tries[rowNumber] = 1
gameFile = text[0][1]

def save(event=''):
    if tries[rowNumber] == 1:
        file = os.path.join(cwd, text[rowNumber][0] + '.ogg')
    else:
        file = os.path.join(cwd, text[rowNumber][0] + '(' + str(tries[rowNumber]) + ')' + '.ogg')
    client.write('SelectAll:')
    client.write('Export2: Filename=' + file)
    text[rowNumber][4] = 'x'
    global labelInfo
    labelInfo.destroy()
    labelInfo = tk.Label(root, text='File saved as ' + file)
    labelInfo.place(relx=0.9, rely=0.9, anchor='ne')
    tries[rowNumber] += 1

def record(event=''):
    client.write('SelectAll:')
    client.write('RemoveTracks:')
    client.write('Record1stChoice:')
    global labelInfo
    labelInfo.destroy()
    labelInfo = tk.Label(root, text='Now recording. Press \'Stop\' to stop', font='arial 8')
    labelInfo.place(relx=0.9, rely=0.9, anchor='ne')

def stop(event=''):
    client.write('Stop:')
    global labelInfo
    labelInfo.destroy()
    labelInfo = tk.Label(root, text='Stopped recording.')
    labelInfo.place(relx=0.9, rely=0.9, anchor='ne')

def next(event=''):
    global rowNumber
    rowNumber += 1
    while text[rowNumber][4] == 'x':
        rowNumber += 1
    tries[rowNumber] = 1
    global labelLine
    labelLine.destroy()
    labelLine = tk.Label(root, text=textwrap.fill(text[rowNumber][2], width=70), font = 'Arial 12')
    labelLine.place(relx=0.5, y=30, anchor='center')
    global labelInfo
    labelInfo.destroy()
    labelInfo = tk.Label(root, text='New file. Please choose an action.', font='arial 8')
    labelInfo.place(relx=0.9, rely=0.9, anchor='ne')
    global labelNumber
    labelNumber.destroy()
    labelNumber = tk.Label(root, text='File no: ' + text[rowNumber][0] + '.', font='arial 8')
    labelNumber.place(relx=0.9, rely=0.85, anchor='ne')

def back(event=''):
    global rowNumber
    rowNumber -= 1
    tries[rowNumber] = 1
    global labelLine
    labelLine.destroy()
    labelLine = tk.Label(root, text=textwrap.fill(text[rowNumber][2], width=70), font = 'Arial 12')
    labelLine.place(relx=0.5, y=30, anchor='center')
    global labelInfo
    labelInfo.destroy()
    labelInfo = tk.Label(root, text='Returned to previous file. Please choose an action.', font='arial 8')
    labelInfo.place(relx=0.9, rely=0.9, anchor='ne')
    global labelNumber
    labelNumber.destroy()
    labelNumber = tk.Label(root, text='File no: ' + text[rowNumber][0] + '.', font='arial 8')
    labelNumber.place(relx=0.9, rely=0.85, anchor='ne')

def delete(event=''):
    client.write('SelectAll:')
    client.write('RemoveTracks:')
    global labelInfo
    labelInfo.destroy()
    labelInfo = tk.Label(root, text='Recording deleted.', font='arial 8')
    labelInfo.place(relx=0.9, rely=0.9, anchor='ne')


def playOriginal(event=''):
    if sys.platform == 'win32':
        subprocess.Popen(['start', os.path.join(cwd, 'AwShirt', 'TalkshowExport', 'project', 'media', text[rowNumber][0] + '.ogg')], shell=True)
    else:
        subprocess.Popen(['open', os.path.join(cwd, 'AwShirt', 'TalkshowExport', 'project', 'media', text[rowNumber][0] + '.ogg')])
    global labelInfo
    labelInfo.destroy()
    labelInfo = tk.Label(root, text='Playing original file.', font='arial 8')
    labelInfo.place(relx=0.9, rely=0.9, anchor='ne')

def playRecording(event=''):
    client.write('Play:')
    global labelInfo
    labelInfo.destroy()
    labelInfo = tk.Label(root, text='Playing your recording.', font='arial 8')
    labelInfo.place(relx=0.9, rely=0.9, anchor='ne')

def exit(event=''):
    sys.exit()

def exit_hook():
    writer.writerows(text)

labelInfo = tk.Label(root, text='New file. Please choose an action.', font='arial 8')
labelInfo.place(relx=0.9, rely=0.9, anchor='ne')
labelNumber = tk.Label(root, text='File no: ' + text[rowNumber][0] + '.', font='arial 8')
labelNumber.place(relx=0.9, rely=0.85, anchor='ne')
labelLine = tk.Label(root, text=textwrap.fill(text[rowNumber][2], width=70), font = 'Arial 12')
labelLine.place(relx=0.5, y=10, anchor='n')

recordButton = tk.Button(root,text="Record", bg = 'red', width = '12',command=record)
recordButton.place(relx=0.1, y=70, anchor='nw')
root.bind('<r>', record)
recordTip = Hovertip(recordButton,'Or press \'r\'')

saveButton = tk.Button(root,text="Save", width = '12',command=save)
saveButton.place(relx=0.5, y=70, anchor='n')
root.bind('<Control_L><s>', save)
saveTip = Hovertip(saveButton,'Or press \'Ctrl\' + \'S\'')

playRButton = tk.Button(root,text="Play Recording", width = '12',command=playRecording)
playRButton.place(relx=0.9, y=70, anchor='ne')
root.bind('<p>', playRecording)
playRTip = Hovertip(playRButton,'Or press \'p\'')

stopButton = tk.Button(root,text="Stop", bg = 'olive', width = '12',command=stop)
stopButton.place(relx=0.1, y=120, anchor='nw')
root.bind('<t>', stop)
stopTip = Hovertip(stopButton,'Or press \'t\'')

deleteButton = tk.Button(root,text="Delete", width = '12',command=delete)
deleteButton.place(relx=0.5, y=120, anchor='n')
root.bind('<Delete>', delete)
deleteTip = Hovertip(deleteButton,'Or press \'Delete\'-key')

playOButton = tk.Button(root,text="Play Original", width = '12',command=playOriginal)
playOButton.place(relx=0.9, y=120, anchor='ne')
root.bind('<o>', playOriginal)
playOTip = Hovertip(playOButton,'Or press \'o\'')

backButton = tk.Button(root,text="Back", width = '12',command=back)
backButton.place(relx=0.1, y=170, anchor='nw')
root.bind('<Left>', back)
root.bind('<KP_Left>', back)
backTip = Hovertip(backButton,'Or press \'<-\'-key')

nextButton = tk.Button(root,text="Next", width = '12',command=next)
nextButton.place(relx=0.5, y=170, anchor='n')
root.bind('<Right>', next)
root.bind('<KP_Right>', next)
nextTip = Hovertip(nextButton,'Or press \'->\'-key')

exitButton = tk.Button(root,text="Exit", width = '12',command=exit)
exitButton.place(relx=0.9, y=170, anchor='ne')
root.bind('<Escape>', exit)
exitTip = Hovertip(exitButton,'Or press \'Esc\'-key')

atexit.register(exit_hook)

root.mainloop()