import threading 
import socket
import sys
import time


host = ''
port = 9000
locaddr = (host,port) 

action_in_proggress = False

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

tello_address = ('192.168.10.1', 8889)

sock.bind(locaddr)

def recv():
    global action_in_proggress
    count = 0
    while True: 
        try:
            data, server = sock.recvfrom(1518)
            responce = data.decode(encoding="utf-8")
            print(responce)
            action_in_proggress = False
        except Exception:
            print ('\nExit . . .\n')
            break


#recvThread create
recvThread = threading.Thread(target=recv)
recvThread.start()

def kill(angle, distance):
    global action_in_proggress
    try:
        while action_in_proggress:
            pass
        msg = "command"
        print(msg)
        msg = msg.encode(encoding="utf-8") 
        sent = sock.sendto(msg, tello_address)
        action_in_proggress = True
        while action_in_proggress:
            pass
        msg = "mon"
        print(msg)
        msg = msg.encode(encoding="utf-8") 
        sent = sock.sendto(msg, tello_address)
        action_in_proggress = True
        while action_in_proggress:
            pass
        msg = "mdirection 2"
        print(msg)
        msg = msg.encode(encoding="utf-8") 
        sent = sock.sendto(msg, tello_address)
        action_in_proggress = True
        while action_in_proggress:
            pass
        msg = "takeoff"
        print(msg)
        msg = msg.encode(encoding="utf-8") 
        sent = sock.sendto(msg, tello_address)
        action_in_proggress = True
        while action_in_proggress:
            pass
        msg = "up 80"
        print(msg)
        msg = msg.encode(encoding="utf-8") 
        sent = sock.sendto(msg, tello_address)
        action_in_proggress = True
        while action_in_proggress:
            pass
        # if angle > 0:
        #     msg = "cw " + str(angle)
        #     msg = msg.encode(encoding="utf-8") 
        #     sent = sock.sendto(msg, tello_address)
        #     action_in_proggress = True
        # elif angle < 0:
        #     msg = "ccw " + str(-1*angle)
        #     msg = msg.encode(encoding="utf-8") 
        #     sent = sock.sendto(msg, tello_address)
        #     action_in_proggress = True
        # while action_in_proggress:
        #     pass
        # msg = "forward " + str(distance)
        # msg = msg.encode(encoding="utf-8") 
        # sent = sock.sendto(msg, tello_address)
        # action_in_proggress = True
        # while action_in_proggress:
        #     pass
        # msg = "back " + str(distance)
        # msg = msg.encode(encoding="utf-8") 
        # sent = sock.sendto(msg, tello_address)
        # action_in_proggress = True
        # while action_in_proggress:
        #     pass
        # angle = -1*angle
        # if angle > 0:
        #     msg = "cw " + str(angle)
        #     msg = msg.encode(encoding="utf-8") 
        #     sent = sock.sendto(msg, tello_address)
        #     action_in_proggress = True
        # elif angle < 0:
        #     msg = "ccw " + str(-1*angle)
        #     msg = msg.encode(encoding="utf-8") 
        #     sent = sock.sendto(msg, tello_address)
        #     action_in_proggress = True
        # while action_in_proggress:
        #     pass

        msg = "go 0 0 50 40 m1"
        print(msg)
        msg = msg.encode(encoding="utf-8") 
        sent = sock.sendto(msg, tello_address)
        action_in_proggress = True
        while action_in_proggress:
           pass

        msg = "go 0 0 25 40 m1"
        print(msg)
        msg = msg.encode(encoding="utf-8") 
        sent = sock.sendto(msg, tello_address)
        action_in_proggress = True
        while action_in_proggress:
           pass

        msg = "land"
        msg = msg.encode(encoding="utf-8") 
        sent = sock.sendto(msg, tello_address)
        action_in_proggress = True
        while action_in_proggress:
            pass
        msg = "moff"
        msg = msg.encode(encoding="utf-8") 
        sent = sock.sendto(msg, tello_address)
        action_in_proggress = True

        return "Killed"

    except KeyboardInterrupt:
        print ('\n . . .\n')
        msg = "emergency"
        msg = msg.encode(encoding="utf-8") 
        sent = sock.sendto(msg, tello_address)
        sock.close()  
        return

print(kill(-30, 100))
sock.close()  

'''
while True: 
    try:
        msg = input("");

        if not msg:
            break  

        if 'end' in msg:
            print ('...')
            sock.close()  
            break

        # Send data
        msg = msg.encode(encoding="utf-8") 
        sent = sock.sendto(msg, tello_address)
    except KeyboardInterrupt:
        print ('\n . . .\n')
        sock.close()  
        break
'''