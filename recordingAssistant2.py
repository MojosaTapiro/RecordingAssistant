#! python3
# prints phrase to be recorded and copies respective file number to clipboard; press Enter to receive next phrase or 1 to copy file number + (number of tries) to clipboard


from encodings import utf_8
import os, csv, sys, msvcrt


#sets Jackbox folder as cwd
os.chdir(os.path.realpath(__file__).replace('recordingAssistant2.py', ''))
cwd = os.getcwd()
#from pipeclient import PipeClient as client, main
import pipeclient
client = pipeclient.PipeClient()

with open('tekstoj.csv', encoding='utf-8') as inf:
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
                client.write('SelectAll:')
            if tryNumber == 1:
                file = os.path.join(cwd, row[0] + '.ogg')
            else:
                file = os.path.join(cwd, row[0] + '(' + str(tryNumber) + ')' + '.ogg')
            print('Stopped recording. Press Enter to save and continue, 1 to delete, 2 to save and retry, 3 to skip or 4 to exit.')
            input_char = msvcrt.getch()
            if input(): 
                client.write('Export2: Filename=' + file)
                print('File saved as ' + file)
                client.write('Delete:')
                row += 'x'
                writer.writerow(row)
                condition = 0
                continue
            elif input_char() == '1':
                client.write('Delete:')
                continue
            elif reaction == '2':
                client.write('Export2: Filename=' + file)
                print('File saved as ' + file)
                client.write('Delete:')
                tryNumber += 1
                continue
            elif reaction == '3':
                writer.writerow(row)
                condition = 0
                continue
            elif reaction == '4':
                for row in reader:
                    writer.writerow(row)
                writer.writerows(reader)
                sys.exit()
            else:
                continue
    writer.writerows(reader)