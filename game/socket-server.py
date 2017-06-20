import socket
import sys
import cPickle
import constants
import utils

from hangword import Hangword
from thread import *
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

#Bind socket to local host and port
try:
    s.bind(('', constants.PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'

connections = []
generate_word = utils.create_word('words.txt')
 
# start listening on socket
s.listen(constants.MAX_CONNECTIONS)
print 'Socket now listening'

game_over = False
 
# function for handling connections. This will be used to create threads
def clientthread(conn):
    global game_over
    global generate_word
    # create the common word in different instances
    secret_word = Hangword(generate_word)

    while True:
        #Receiving from client
        data = conn.recv(4096)
        
        if data == 'winner':
            game_over = True
        if data != constants.SENT_DEFAULT:
            print data
        if not data:
            break
            
        if not game_over:
            secret_word.operate(data)
            serialized = cPickle.dumps(secret_word)
            conn.sendall(serialized)
        else:
            conn.sendall('end')

    #came out of loop
    conn.close()
 
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])

    # add conn to the list
    connections.append(conn)

    # wait for all of the player to come 
    if len(connections) < constants.MAX_CONNECTIONS:
        print 'waiting for a second player'
        continue
    game_over = False
    generate_word = utils.create_word('words.txt')
    # if all players are connected create the threads for each one
    for c in connections:
        #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
        print c.getpeername()
        start_new_thread(clientthread ,(c,))
    connections = []
s.close()