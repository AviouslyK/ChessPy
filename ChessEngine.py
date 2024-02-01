"""
This class stores all info about the current state of the chess game. It also determines valid moves and keeps a move log
"""

class GameState():
    def __init__(self):
        # Todo - replace with numpy arrays instead of 2D list
        # The board is an 8x8 2D list with each element having 2 characters
        # e[0] = color, e[1] = type of piece.
        self.board = [
            ['bR','bN','bB','bQ','bK','bB','bN','bR'],
            ['bP','bP','bP','bP','bP','bP','bP','bP'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['wP','wP','wP','wP','wP','wP','wP','wP'],
            ['wR','wN','wB','wQ','wK','wB','wN','wR']]

        self.whiteToMove = True
        self.moveLog = []
            