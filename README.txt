CPSC 526 Assignment #2

Steven Leong 10129668 T01
Josh Quines 10138118 T03

How to run:		python3 A2.py <port>

How to Connect: 	nc localhost <port>
	make sure its the same port number

Handshake details:
	To access the backdoor the client needs to enter the password "p4$$w0rD". If the client enters the wrong password, they will be disconnected from the server

Supported Commands:
	pwd - Return the current working directory
	cd <dir> - Change the current working directory to <dir>
	ls - List the contents of the current working directory
	cp <file1> <file2> - Copy file1 to file2
	mv <file1> <file2> - Rename file1 to file2
	rm <file> - Delete file
	cat <file> - Return contents of the file
	snap - Take a snapshot of all the files in the current directory and save it in memory. 
	diff - Compare the contents of the current directory to the saved snapshot, and report differences (deleted files, new files and changed files)
	help [cmd] - Print a list of commands, and if given an argument, print more detailed help for the command
	logout - Disconnect client (server closes the socket)
	off - Terminate the backdoor program
	who - List user[s] currently logged in
	ps - Show currently running processes
