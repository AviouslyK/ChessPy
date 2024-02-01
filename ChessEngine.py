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

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = '--'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove # swap active player

'''
Holds all information about a move, and the boardstate during that move (for undos)
'''
class Move():

    # For converting to and from rank-file notation
    ranksToRows = {'1' : 7, '2' : 6, '3' : 5, '4': 4, '5' : 3, '6' : 2, '7' : 1, '8' : 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {'a' : 0, 'b' : 1, 'c' : 2, 'd': 3, 'e' : 4, 'f' : 5, 'g' : 6, 'h' : 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board): # tuple, tuple, 2D list of strings
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

    # Returns rank-file notation. Todo - make more like real chess notation
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
        
    # Helper: get's rank and file for one square
    def getRankFile(self,r,c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
