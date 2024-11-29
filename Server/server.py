import socket
import os.path
import sys
# from Client import client

def main():
    host = "127.0.0.1"
    # port to listen to 
    port = int(sys.argv[1])
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.bind((host,port))
    # start listening     
    sock.listen(5)
    print("Initializing client")

    connectedsocket, adr = sock.accept()
    print(" Connected to client.")

    while True:
        try:
            cmnd = connectedsocket.recv(40).decode()
        except IOError:
            print("Command not recieved. Connection closed.")
            sock.close()
            connectedsocket.close()
            break

        if cmnd == "get":
            emphsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            emphsock.bind(('',0))
            connectedsocket.sendall(str(emphsock.getsockname()[1]).encode())

            emphsock.listen(1)
            emphconn, adr = emphsock.accept()

            filename = emphconn.recv(40).decode()
            print(filename)
            #get content in directory
            content = os.listdir()
            if(filename not in content):
                print("ERROR 550: No such file or directory")
                error_message = "ERROR 550: No such file or directory"
                emphconn.sendall(error_message.encode())  # Send error to client
                emphconn.close()

            else:
                file = open(filename,"r")
                try:
                    emphconn.sendall(file.read().encode())
                except IOError:
                    print("something went wrong")
                    file.close()
                    emphsock.close()
                    emphconn.close()

                print("Data has successfully been sent.")
                print(filename + " has been sent with " + str(os.stat(filename).st_size)+" bytes uploaded")
                #close all open things
                file.close()
                emphconn.close()
                emphsock.close()
                

        if cmnd == "put":

            emphsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            emphsock.bind(('',0))
            connectedsocket.sendall(str(emphsock.getsockname()[1]).encode())

            emphsock.listen(1)
            emphconn,adr = emphsock.accept()

            filename = emphconn.recv(40).decode()

            f = open(filename, "a")

            print("getting data")

            while True:
                data = emphconn.recv(40).decode()

                if not data:
                    f.close()
                    break
                else:
                    f.write(data)
            charnum = str(os.stat(filename).st_size)
            print("File has been successfully recieved.")
            print(f+" has been downloaded. The number of bytes downloaded was "+ charnum + ".")

            #close items
            f.close()
            emphconn.close()
            emphsock.close()
        
        if cmnd == "ls":
            emphsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            emphsock.bind(('',0))
            connectedsocket.sendall(str(emphsock.getsockname()[1]).encode())

            emphsock.listen(1)
            emphconn,adr = emphsock.accept()

            content = os.listdir()
            listofcontent = ""
            for item in content:
                listofcontent += item + "\n"
            print("sending")
            try:
                emphconn.sendall(listofcontent.encode())
            except IOError:
                print("Could not send items.")

            print("Succesfully send list of files in directory.")

            #close our connections
            emphconn.close()
            emphsock.close()
        
        if cmnd == "quit":
            print("Closing connection")
            connectedsocket.close()
            sock.close()
            break

if __name__ == "__main__":
    main()