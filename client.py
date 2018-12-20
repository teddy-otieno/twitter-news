import socket
import sys

#This is a basic server client implementationn
def main():
    list_of_users = sys.argv[1:]   
    #TODO: Add error checking later, feature to remove, but i fell lazy today.
    for user in list_of_users:
        send_to_script(user)
    print("Updated")

def send_to_script(user):
    host = 'localhost'
    port = '9090'

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send(user.encode('utf-8'))
    print("{}".format(str(s.recv(1024), 'utf-8')))
