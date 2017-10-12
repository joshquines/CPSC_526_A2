import os
import subprocess
import shutil
import sys
from collections import defaultdict
import socketserver
import socket, threading


def inputActions(x):

	userInput = x
	#userCommand = 

	#Get UserCommand
	userCommand = userInput.split()
	Command = userCommand[0]

	#GET WORKING DIRECTORY (pwd)
	if command == 'pwd':
		try:
			#Get working directory
			directory = os.getcwd()
			directory = directory.decode("utf-8")
			message = "Current working directory is: " + directory

		except:
			message = "Error: Wrong number of inputs. Correct command is: pwd"

	#CHANGE WORKING DIRECTORY (cd)
	elif command == 'cd':
		try:
			newDir = userCommand[1]
			cdNewDir = os.chdir(newDir)
			newDir = cdNewDir.decode("utf-8")
			message = "Directory changed to: " + str(newDir)

		except FileNotFoundError:
			newDir = userCommand[1]
			message = "Error: Directory or File does not exist: "  + neWDir 

		except:
			message = "Error: Incorrect use of \'cd\'. Correct input is: cd <dir>"

	#LIST FILES AND FOLDERS IN CURRENT DIRECTORY (ls)
	elif command == "ls":
		try:
			theList = subprocess.check_output(command)
			message = theList.decode('utf-8')
		except:
			message = "Error: unable to list files and directories"

	#COPY A FILE (cp <filename> <newFile>)
	elif command == "cp":
		try:
			file1 = userCommand[1]
			file2 = userCommand[2]
			shutil.copy(file1, file2)
			message = "Copied " + str(file1) + "to " + str(file2)
		except FileNotFoundError:
			message = "File to copy not found"
		except:
			message = "Error: Wrong usage of \'cp\': Enter cp <filename> <newname>"

	#RENAME A FILE (cp <filname> <newName>)
	elif command == "mv":
		try:
			file1 = userCommand[1]
			renamed = userCommand[2]
			shutil.move(file1, renamed)
			message = str(file1) + " successfully copied to: " + renamed
		except FileNotFoundError:
			message = "File to rename not found"
		except:
			message = "Error: Wrong usage of \'mv\': Enter mv <filename> <newname>"

	#REMOVE A FILE (rm <filePath><filename>)
	elif command == "rm":
		try:
			file1 = userCommand[1]
			os.remove(file1)
			message = str(file1) + " has been removed"
		except FileNotFoundError:
			message = "File to be removed not found"
		except:
			message = "Error: Wrong usage of \'rm\': Enter rm <filepath><filename>"

	#RETURN CONTENTS OF THE FILE (cat)
	elif command == "cat":
		try:
			fileLocation = os.getcwd()
			filename = userCommand[1]
			with open(fileLocation + "/" + filename, 'r') as fileContent:
				message = fileContent.read()
				#msgDecode = fileContent.read()
				#message = msgDecode.decode("utf-8")
			#Alternative -- uses method from the slides
			# newCommand = "cat " + filename
			# run command and gather all output in memory
			#output = subprocess.run("cat", shell=True, stdout=subprocess.PIPE).stdout
			# convert output of the process to string
			#str = output.decode("utf-8")

		except:
			message = "Error: Could not cat"

	#TAKE A SNAPSHOT OF ALL THE FILES IN CURRENT DIRECTORY AND SAVE IT IN MEMORY (snap)
	elif command == "snap":
		try:
			fileList = defaultdict(list)
			currentDirectory = os.getcwd
			directoryFiles = os.listdir(currentDirectory)
			for files in directoryFiles:
				fileList[currentDirectory].append(files)
			message = "Snapshot of " + str(currentDirectory) + " has been saved"
		except:
			message = "Error: Unable to take screenshot"
	#COMPARE THE CONTENTS OF THE CURRENT DIRECTORY TO THE SAVED SNAPSHOT AND REPORT DIFFERENCES (diff)
	elif command == "diff":
		fileList2 = defaultdict(list)
		currentDirectory = os.getcwd
		#Do same thing for snap as fileList2
		try:
			directoryFiles = os.listdir(currentDirectory)
			for files in directoryFiles:
				fileList2[currentDirectory].append(files)

			if fileList[currentDirectory] == fileList2[currentDirectory]:
				message = "The files are the same"
			else:
				diffList = defaultdict(list)
				for x in fileList:
					if x not in fileList2:
						diffList[currentDirectory].append(str(x) + " was deleted")
				for x in fileList2:
					if x not in fileList:
						diffList[currentDirectory].append(str(x) + " was added")
				message = "These are the differences:\n\n" + ("\n".join(diffList[currentDirectory]))
		except NameError:
			message = "Error: Original snapshot does not exist"

	#OPTIONAL PICK 2


	#elif userInput startswith logout (disconnect client)

	#elif userInput startswith who (list users currently logged in)

	#elif userInput starts with net (show current network config)

	#elif userInput starts with ps (SHOW CURRENT PROCESSES)

	#elif userInput starts with nmap (run nmap with parameters <params>)

	#elif userINput starts with ext (run program <program> with parameters <params>)

	else:
		message = "Error: Command not recognized. \n\nType \'help\' to see available commands" 

	return message

"""
Begin code taken from the provided Assignment 2 slides
"""
class MyTCPHandler(socketserver.BaseRequestHandler):
	BUFFER_SIZE = 4096
	def handle(self):
		while 1:
			data = self.request.recv(self.BUFFER_SIZE)
			if len(data) == self.BUFFER_SIZE:
				while 1:
					try: #error means no more data
						data += self.request.recv(self.BUFFER_SIZE, socket.MSG_DONTWAIT)
					except:
						break
			if len(data) == 0:
				break 
			data = data.decode("utf-8")
			self.request.sendall(bytearray("You said: " + data, "utf-8"))
			print("%s (%s) wrote: %s" % (self.client_address[0], threading.currentThread().getName(), data.strip()))

if __name__ == "__main__":
	HOST = "localhost"
	if len(sys.argv) > 1:
		PORT = int(sys.argv[1])
	else:
		print("Port number not specified.")
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


def main():

	#CONNECT TO CLIENT
	print("message")
	

	#Get userInput
	backdoorPassword = "p4$$w0rD"
	print("Please enter the password")
	#getUserInput
	if getUserinput != backdoorPassword:
		print("You entered the wrong password. \nTerminating connection. \nBye!")
		#kill connection




	#GET INITIAL COMMAND FROM USER
	#get userInput
	
	#START GETTING COMMNDS FROM USER
	while 1:
		print("Enter command:")
		#GET USER INPUT 
		while userInput != "off":
			returnMessage = inputActions(userinput)

			#GET USERINPUT AGAIN IF THERE WAS AN ERROR
			if returnMessage.startswith("Error: "):
				print (returnMessage + "\n....\nPlease try again or type \"help\"")
				#GET USERINPUT
				print ("You typed " + str(userInput)) #debug

			#COMMANDS THAT DON'T NEED FURTHER ACTIONS
			#THIS ELIF OFF CAN BE DELETED
			elif userInput == "off":
				print ("You typed " + str(userInput)) #debug
				#Terminate Connection
				print("Connection was closed")
				#Kill program
				break
			elif userInput == "help":
				helpMessage = "\n".join([
					"HERE ARE THE COMMANDS YOU CAN USE",
					"pwd",
					"cd <dir>",
					"ls",
					"cp <file1> <file2>",
					"mv <file1> <file2>",
					"rm <file>",
					"cat <file>",
					"snap",
					"diff",
					"help [cmd]",
					"logout",
					"off"
					])
				print(helpMessage)
				print("Enter command:")
				#GET USER INPUT 
				print ("You typed " + str(userInput)) #debug
			elif userInput == "logout":
				#terminate connection
				print("Connection was closed")
				break
			else:
				#PRINT RETURN MESSAGE
				print(returnMessage)			
				print ("Waiting for new command")
				#GET USERINPUT
				print ("You typed " + str(userInput)) #debug

		print("Connection was closed")
		# CLOSE CONNECTION
