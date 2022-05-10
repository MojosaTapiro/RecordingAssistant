#! python3
# program to be run in command prompt: prints phrase to be recorded, records and saves file correctly. 

import os, csv, sys, subprocess


#sets Jackbox folder as cwd
os.chdir(os.path.realpath(__file__).replace('recordingAssistant.py', ''))
cwd = os.getcwd()
#from pipeclient import PipeClient as client, main
import pipeclient
client = pipeclient.PipeClient()

with open('example.csv', encoding='utf-8') as inf:
    reader = csv.reader(inf.readlines())

with open('tekstoj2.csv', 'w', newline = '', encoding='utf-8') as outf:
    writer = csv.writer(outf)
    for row in reader:
        condition = 1
        tryNumber = 1
        if reader.line_num == 1:
            continue
        while condition == 1:
            try:
                if row[4].lower() == 'x':
                    writer.writerow(row)
                    continue
            except IndexError:
                pass
            print('\n' + row[2] + '\n')
            print('Press Enter to start recording, then press again to stop recording.')
            if input() == '':
                client.write('Record2ndChoice:')
                print('Started recording.')
            if input() == '':
                client.write('Stop:')
                print('Stopped recording. Press Enter to save and continue, 1 to delete and retry, 2 to save and retry, 3 to play original file, 4 to skip, or 5 to exit.')
            if tryNumber == 1:
                file = os.path.join(cwd, row[0] + '.ogg')
            else:
                file = os.path.join(cwd, row[0] + '(' + str(tryNumber) + ')' + '.ogg')
            reaction = input()
            if reaction == '':
                client.write('SelectAll:')
                client.write('Export2: Filename=' + file)
                print('File saved as ' + file)
                client.write('SelectAll:')
                client.write('RemoveTracks:')
                row += 'x'
                writer.writerow(row)
                condition = 0
            elif reaction == '1':
                client.write('SelectAll:')
                client.write('RemoveTracks:')
                print('Last recording deleted.')
                continue
            elif reaction == '2':
                client.write('SelectAll:')
                client.write('Export2: Filename=' + file)
                print('File saved as ' + file)
                client.write('SelectAll:')
                client.write('RemoveTracks:')
                tryNumber += 1
                continue
            elif reaction == '3':
                subprocess.Popen(['start', os.path.join(cwd, 'AwShirt', 'TalkshowExport', 'project', 'media', row[0] + '.ogg')], shell=True)
            elif reaction == '4':
                client.write('SelectAll:')
                client.write('RemoveTracks:')
                writer.writerow(row)
                condition = 0
                continue
            elif reaction == '5':
                for row in reader:
                    writer.writerow(row)
                writer.writerows(reader)
                sys.exit()
            else:
                continue
    writer.writerows(reader)