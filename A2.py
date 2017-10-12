import os
import subprocess
import shutil
import sys
from collections import defaultdict
import socketserver
import socket, threading




"""
Begin code taken from the provided Assignment 2 slides
"""
class MyTCPHandler(socketserver.BaseRequestHandler):
	CONNECTED = False
	BUFFER_SIZE = 4096
	PASSWORD = "p4$$w0rD"

	def handshake(self):      
		self.request.sendall(bytearray("What's the password? \n", "utf-8"))
		#getUserInput
		userInput = self.request.recv(self.BUFFER_SIZE)

		# check the input
		if len(userInput) == self.BUFFER_SIZE:
			while 1:
				try:  # error means no more data
					userInput += self.request.recv(self.BUFFER_SIZE, socket.MSG_DONTWAIT)
				except:
					break

		# convert userInput to string 
		# [:-1] removes the newline
		attempt = userInput.decode("utf-8")[:-1]
		print("Password entered: " + attempt)

		if attempt != self.PASSWORD:
			self.request.sendall(bytearray("You entered the wrong password. \nTerminating connection. \nBye! ", "utf-8"))
			return False
		print("Correct password used")
		self.request.sendall(bytearray("Access Granted.\n", "utf-8"))
		return True

	def handle(self):
			
		print(self.client_address[0] + "is now connected")

		if not self.handshake():
			print(self.client_address[0] + "has disconnected")
			self.request.close()
			return

		self.CONNECTED = True

		while self.CONNECTED:
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
			#self.request.sendall(bytearray("You said: " + data, "utf-8"))
			print("%s wrote: %s" % (self.client_address[0], data.strip()))
			self.inputActions(data)

	def inputActions(self, x):
		userInput = x
		#userCommand = 

		#Get UserCommand
		userCommand = userInput.split()
		command = userCommand[0]

		#GET WORKING DIRECTORY (pwd)
		if command == 'pwd':
			try:
				#Get working directory
				directory = os.getcwd()
				message = "Current working directory is: " + directory + "\n"

			except:
				#tb = traceback.format_exc()
				#print (tb)
				message = "Error: Wrong number of inputs. Correct command is: pwd"

		#CHANGE WORKING DIRECTORY (cd)
		elif command == 'cd':
			try:
				newDir = userCommand[1]
				cdNewDir = os.chdir(newDir)
				#newDir = cdNewDir.decode("utf-8")
				message = "Directory changed to: " + str(newDir)

			except FileNotFoundError:
				newDir = userCommand[1]
				message = "Error: Directory or File does not exist: "  + newDir 

			except:
				tb = traceback.format_exc()
				print (tb)
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
					message = fileContent.read() + "\n"
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
				#fileList = defaultdict(list)
				currentDirectory = os.getcwd()
				fileList[currentDirectory] = [f.name for f in os.scandir() if f.is_file()]
				message = "Snapshot of " + str(currentDirectory) + " has been saved"
				print(fileList[currentDirectory])
			except:
				tb = traceback.format_exc()
				print (tb)
				message = "Error: Unable to take screenshot"

		#COMPARE THE CONTENTS OF THE CURRENT DIRECTORY TO THE SAVED SNAPSHOT AND REPORT DIFFERENCES (diff)
		elif command == "diff":
			#fileList2 = defaultdict(list)
			currentDirectory = os.getcwd()
			#Do same thing for snap as fileList2
			try:
				currentDirectory = os.getcwd()
				fileList2[str(currentDirectory)] = [f.name for f in os.scandir() if f.is_file()]

				if fileList[currentDirectory] == fileList2[currentDirectory]:
					message = "The files are the same"
				elif len(fileList[currentDirectory]) < 1:
					message = "Error: Original snapshot does not exist"
					print (message)
				else:
					#diffList = defaultdict(list)
					for x in fileList[str(currentDirectory)]:
						if x not in fileList2[str(currentDirectory)]:
							diffList[str(currentDirectory)].append(str(x) + " was deleted")
							print("first: " + x)
					for x in fileList2[str(currentDirectory)]:
						if x not in fileList[str(currentDirectory)]:
							diffList[str(currentDirectory)].append(str(x) + " was added")
							print("second: " + x)
					message = "These are the differences:\n\n" + ("\n".join(diffList[currentDirectory]))

					print (fileList[currentDirectory])
					print (fileList2[currentDirectory])

					del diffList[currentDirectory]
					del fileList2[currentDirectory]

			except NameError:
				tb = traceback.format_exc()
				print (tb)
				message = "Error: Original snapshot does not exist"

		elif command == "help":
			
			try:
				if userCommand[1] == "pwd":
					message = "pwd shows your current directory\nUsage: pwd"
				elif userCommand[1] == "cd":
					message = "cd changes directory. \nUsage: cd <dir>"	
				elif userCommand[1] == "ls":
					message = "ls lists the files and folders in current directory \nUsage: ls"
				elif userCommand[1] == "cp":
					message = "cp copies a file into another file. \nUsage: cp <file1> <file2>"	
				elif userCommand[1] == "mv":
					message = "mv renames a file. \nUsage: mv <filename> <newFilename>"
				elif userCommand[1] == "rm":
					message = "rm removes a file. \nUsage: rm <file>"
				elif userCommand[1] == "cat":
					message = "cat shows contents of a file. \nUsage: cat <file>"
				elif userCommand[1] == "snap":
					message = "snap takes saves a list of files in current directory.\n Usage: snap"
				elif userCommand[1] == "diff":
					message = "diff shows differences of files in current directory with previous snapshot.\n Usage: diff"		
				elif userCommand[1] == "help":
					message = "You know what it does. Stop asking me"
				else:
					message = "Error: Invalid command. Type \"help\" for available commands"
			except:
				helpMessage = "\n".join([
					"HERE ARE THE COMMANDS YOU CAN USE",
					"pwd",
					"cd <dir>",
					"ls",
					"cp <file1> <file2>",
					"mv <filename> <newFilename>",
					"rm <file>",
					"cat <file>",
					"snap",
					"diff",
					"help [cmd]: where cmd = one of the above commands",
					"logout",
					"off"
					])
				message = helpMessage 
		elif command == "logout":
			message = "Logging out"
			#terminate connection
			print("Connection was closed")
			self.CONNECTED = False
			self.request.close()
			return
		elif command == "off":
			self.request.sendall(bytearray("Terminating the backdoor\n", "utf -8"))
			print("Backdoor has been terminated by the " + self.client_address[0])
			self.CONNECTED = False
			self.request.close()
			sys.exit()

		#OPTIONAL PICK 2


		#elif userInput startswith who (list users currently logged in)

		#elif userInput starts with net (show current network config)

		#elif userInput starts with ps (SHOW CURRENT PROCESSES)

		#elif userInput starts with nmap (run nmap with parameters <params>)

		#elif userINput starts with ext (run program <program> with parameters <params>)

		else:
			message = "Error: Command not recognized. \n\nType \'help\' to see available commands" 

		#print(message)
		self.request.sendall(bytearray(message + "\n", "utf -8"))
		#return message

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

