from hangword import Hangword
import random
import constants
import pygame

def create_word(filename):
    lines = []
    with open(filename) as f:
        lines = f.read().split("\n")
    random_word = lines[random.randrange(0, len(lines))]
    return random_word  

def load_images():
    cache = {}
    for i in range(0, constants.IMAGES_COUNT + 1):
        cache[i] = pygame.image.load("sprites/%s.png" % (i, ) )
    return cache
    