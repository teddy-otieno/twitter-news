import socket
import sys
#This is a basic server client implementationn

def main():
    print(sys.argv)
    list_of_users = sys.argv[1:]
    #TODO: Add error checking later, feature to remove, but i fell lazy today.
    for user in list_of_users:
        print(user)
        send_to_script(user)
    send_to_script('EOF')

def send_to_script(string_send):
    host = 'localhost'
    port = 9090

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send(string_send.encode('utf-8'))
    print("{}".format(str(s.recv(1024), 'utf-8')))
    s.close()


if __name__ == '__main__':
    main()
