"""
Handles user input, and displays GameState object.
"""

import pygame as p
import ChessEngine

# Define some constants
WIDTH = HEIGHT = 400 # can't go too big, images aren't high res
DIMENSION = 8 # chess board is 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 # for animations
IMAGES = {}

'''
Initialize a global dictionary of images.
Will be called exactly once in the main
Only want to load images one time (very expensive operation)
'''
def loadImages():
    pieces = ['wR','wN','wB','wQ','wK','wP','bR','bN','bB','bQ','bK','bP']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

'''
main driver, handle user input and update graphics
'''

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))

    # create a game state
    gs = ChessEngine.GameState()
    print(gs.board)

    loadImages() # only do this once
    
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

'''
responsible for all graphics in current game state
'''
def drawGameState(screen, gs):
    drawBoard(screen)
    # add in piece highlighting and move suggestions later
    drawPieces(screen, gs.board)

'''
Remember top left square is always light. Keep Board+Pieces in case I want to highlight moves later
'''
def drawBoard(screen):
    colors = [p.Color(227,193,111), p.Color(184,139,74)] # or 'white' and 'gray'
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            # even/odd picks color
            color = colors[(row + col) % 2]
            p.draw.rect(screen, color, p.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != '--':
                screen.blit(IMAGES[piece], p.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()