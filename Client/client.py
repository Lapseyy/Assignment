import socket
import os 
import sys
# from Server import server
def main():
    host = sys.argv[1]
    port = int(sys.argv[2])
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((host,port))

    while True:
        cmnd = input("ftp> ").split()

        if len(cmnd) ==1 :
            choice = cmnd[0]
        elif len(cmnd) == 2:
            choice = cmnd[0]
            file = cmnd[1]
        else:
            print("Please only insert a maximum of two prompts.")
            choice = null, file = null

        if choice == "get":
            sock.send(bytes("get","utf-8"))
            #get ephemeral address  
            emphadr = int(sock.recv(40).decode())
            #make ephemeral socket
            emphsock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            emphsock.connect((host,emphadr))
            emphsock.send(file.encode())
            
            
            print("retrieving data")
            data_recvd = []
            #count = 1
            while True:
                
                data = emphsock.recv(40).decode()
                # print("Run",count,data)
                #count+=1
                if data:
                    if(data.startswith('ERROR 550')):
                        #if there is an error
                        print("File Transfer Failed")
                    else:
                        # hold data in the list
                        data_recvd.append(data)
                else:
                    if data_recvd:
                        f = open(file,"a")
                        print("writing data")
                        f.write("".join(data_recvd)) 
                        f.close()
                        print(file +" has been successfuly downloaded.\n" + str(os.stat(file).st_size) + " bytes have been downloaded.")
                    break
            emphsock.close()

        if choice == "put":
            files = os.listdir()
            
            if file not in files:
                file = input("File was not found in your directory. Please enter correct file name.")
           
            else:
                sock.send(bytes("put","utf-8"))
                emphadr = int(sock.recv(40).decode())
                #make ephemeral socket
                emphsock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                emphsock.connect((host,emphadr))
                #check if file exists
                #if it was in directory send file
                emphsock.send(file.encode())

                f = open(file,"r")

                try:
                    emphsock.sendall(f.read().encode())
                except IOError:
                    print("Could not send file to server")
                    f.close()
                    emphsock.close()

                print(file+ " has been sent successfully. "+ str(os.stat(file).st_size) +" bytes have been sent.")
                f.close()
                emphsock.close()

        if choice == "ls":
            sock.send(bytes('ls','utf-8'))
            emphadr = int(sock.recv(40).decode())
            #make ephemeral socket
            emphsock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            emphsock.connect((host,emphadr))
            list = ""

            while True:
                data = emphsock.recv(40).decode()

                if not data:
                    break
                else:
                    list += data

            for item in list.split("\n"):
                print(item)

            print("Successfully printed items in server directory.")
            emphsock.close()

        if choice == "quit":
            sock.send(choice.encode())
            sock.close()
            print("Connection has been closed.")
            break

if __name__ == "__main__":
    main()
