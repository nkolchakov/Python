import pygame
import socket
import sys
import cPickle
import constants
import utils

from pygame_textinput import TextInput
from hangword import Hangword

textinput = TextInput(True) # create inputbox with one-letter input
textbox = pygame.font.SysFont("monospace", constants.FONT)

pygame.init()

gameExit = False

gameDisplay = pygame.display.set_mode((constants.GAME_WIDTH,constants.GAME_HEIGHT))

clock = pygame.time.Clock()

image_cache = utils.load_images()

winner = False

def play():
    global winner
    gameExit = False

    #create an INET, STREAMing socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print 'Failed to create socket'
        sys.exit()
        
    print 'Socket Created'

    host = constants.HOST
    port = constants.PORT
    
    #Connect to remote server
    s.connect((host , port))
    
    print 'Socket Connected to ' + host

    socketIp = s.getsockname()
    last_sent = constants.SENT_DEFAULT
   
    
    while not gameExit:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                gameExit = True

        gameDisplay.fill((255,255,255))
        
        try :
            if textinput.update(events):
                char_input = textinput.get_text()
                last_sent = constants.SENT_DEFAULT if char_input == "" else char_input  
                print "sent: ", last_sent
                textinput.clear()
                s.sendall(last_sent)
            else:
                s.sendall(last_sent)
        except socket.error:
            #Send failed
            print 'Send failed'
            sys.exit()
        
        #Now receive data
        reply = s.recv(4096)

        if 'end' in reply:
            msg = ''
            if not winner:
                msg = 'YOU LOSE'
            else:
                msg = 'YOU WIN'
            
            print msg
            status = textbox.render(msg, 1, (100, 100, 0))
            gameDisplay.blit(status, (150,150))
            pygame.display.update()
            continue
        # deserialize 
        print 'reply', reply
        deser_hang = cPickle.loads(reply)
        
        # check if winner
        if deser_hang.solved:
            winner = True
            # print 'WINNER'
            s.sendall('winner')
        
        # render the word with guessed letters
        word = deser_hang.get_progress()
        word_progress = textbox.render(word, 1, (100,100,0))

        # render wrong guesses
        wrongs = deser_hang.get_wrong_guesses()
        wrongs_as_str = ' '.join(wrongs)
        wrong_guesses = textbox.render(wrongs_as_str, 1, (100, 100, 0))

        # render hangman
        if len(wrongs) > constants.IMAGES_COUNT:
            play()
        curr_hangman_img = image_cache[len(wrongs)]

        gameDisplay.blit(textinput.get_surface(),(10,10))
        gameDisplay.blit(curr_hangman_img, (400,100))

        gameDisplay.blit(word_progress, (100,100))
        gameDisplay.blit(wrong_guesses, (150,150))
        pygame.display.update()

        clock.tick(constants.FPS)

play()

# pygame.quit()
# quit()