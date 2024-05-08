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

        self.moveFunctions = {'P': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}

        self.whiteToMove = True
        self.moveLog = []
    
    '''
    takes a Move and executes it.
    excludes castling, promotion, en-passant
    '''
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = '--'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove # swap active player
    
    '''
    Undo the last move made
    '''
    def undoMove(self):
        if len(self.moveLog) != 0: # make sure that there is a move to undo
            move = self.moveLog.pop() # grab and remove last element from list
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.whiteToMove = not self.whiteToMove # swap active player

    '''
    Get all legal moves
    '''
    def getValidMoves(self):
        return self.getPossibleMoves() # for now ignore checks

    '''
    All moves without considering if illegal because you're put in check
    '''
    def getPossibleMoves(self):
        moves = []
        # check every square
        for r in range(8):
            for c in range(8):
                turn = self.board[r][c][0] # 'b', 'w', or '-'
                piece = self.board[r][c][1]

                # get moves
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    self.moveFunctions[piece](r, c, moves)

        return moves


    '''
    Get all possible moves for this piece
    ''' 
    def getPawnMoves(self, r, c, moves):

        # white pawn moves
        if self.whiteToMove: 

            # advance 1 square
            if self.board[r-1][c] == '--': 
                moves.append(Move((r,c), (r-1,c), self.board))

                # advance 2 squares
                if r == 6 and self.board[r-2][c] == '--':
                    moves.append(Move((r,c), (r-2,c), self.board))
            
            # captures
            if c-1 >= 0: # can't escape board
                if self.board[r-1][c-1][0] == 'b':
                    moves.append(Move((r,c), (r-1,c-1), self.board))
            if c+1 <= 7: # can't escape board
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r,c), (r-1,c+1), self.board))

        # black pawn moves
        else:

            # advance 1 square
            if self.board[r+1][c] == '--': 
                moves.append(Move((r,c), (r+1,c), self.board))

                # advance 2 squares
                if r == 1 and self.board[r+2][c] == '--':
                    moves.append(Move((r,c), (r+2,c), self.board))
            
            # captures
            if c-1 >= 0: # can't escape board
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r,c), (r+1,c-1), self.board))
            if c+1 <= 7: # can't escape board
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r,c), (r+1,c+1), self.board))


    def getRookMoves(self, r, c, moves):

        for delta_r, delta_c in [(1, 0), (-1, 0), (0, -1), (0, 1)]: # up/down (depends on w or b) left right
            for i in range(1,7):
                new_r = r + delta_r * i
                new_c = c + delta_c * i

                # can't escape board
                if (new_r < 0) or (new_r > 7) or (new_c < 0) or (new_c > 7):
                    break

                # piece blocking
                if self.board[new_r][new_c] != '--': 
                    # add move if capturing
                    if (self.board[new_r][new_c][0] == 'b' and self.whiteToMove) or (self.board[new_r][new_c][0] == 'w' and not self.whiteToMove):
                        moves.append(Move((r,c), (new_r, new_c), self.board))
                    break

                moves.append(Move((r,c), (new_r, new_c), self.board))
    

    def getKnightMoves(self, r, c, moves):
        pass
    def getBishopMoves(self, r, c, moves):
        pass
    def getQueenMoves(self, r, c, moves):
        pass
    def getKingMoves(self, r, c, moves):
        pass

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
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol # unique identifier

    ''' Override equals method '''
    def __eq__(self,other):
        if isinstance(other,Move):
            return self.moveID == other.moveID

    # Returns rank-file notation. Todo - make more like real chess notation
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
        
    # Helper: get's rank and file for one square
    def getRankFile(self,r,c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
