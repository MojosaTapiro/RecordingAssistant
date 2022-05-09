#! python3
# prints phrase to be recorded and copies respective file number to clipboard; press Enter to receive next phrase or 1 to copy file number + (number of tries) to clipboard


from encodings import utf_8
import os, pyperclip, csv, sys
import pipeclient.py

#sets Jackbox folder as cwd
os.chdir(os.path.realpath(__file__).replace('registradaHelpilo.py', ''))
cwd = os.getcwd()
import pipeclient.py

with open('tekstoj.csv', encoding='utf-8') as inf:
    reader = csv.reader(inf.readlines())

with open('tekstoj2.csv', 'w', newline = '', encoding='utf-8') as outf:
    writer = csv.writer(outf)
    for row in reader:
        if reader.line_num == 1:
            continue
        tryNumber = 2
        try:
            if row[4].lower() == 'x':
                writer.writerow(row)
                continue
        except IndexError:
            pass
        print(row[2])
        pyperclip.copy(row[0])
        while True:
            reaction = input()
            if reaction == '':
                row += 'x'
                writer.writerow(row)
                break
            elif reaction == '1':
                pyperclip.copy(row[0] + '(' + str(tryNumber)+ ')')
                tryNumber += 1#
            elif reaction == '2':
                writer.writerow(row)
                break
            elif reaction == '3':
                for row in reader:
                    writer.writerow(row)
                writer.writerows(reader)
                sys.exit()
            else:
                continue
    writer.writerows(reader.decode('UTF-8'))