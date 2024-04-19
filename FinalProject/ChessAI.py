import random
import Model

pieceScore = {"K": 0, "Q": 9, "R": 5, "N": 3, "B": 3, "p": 1}

knightScores = [[1, 1, 1, 1, 1, 1, 1, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 1, 1, 1, 1, 1, 1, 1]]

bishopScores = [[4, 3, 2, 1, 1, 2, 3, 4],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [4, 3, 2, 1, 1, 2, 3, 4]]

queenScores = [[1, 1, 1, 3, 1, 1, 1, 1],
               [1, 2, 3, 3, 3, 1, 1, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 1, 2, 3, 3, 1, 1, 1],
               [1, 1, 1, 3, 1, 1, 1, 1]]

rookScores = [[4, 3, 4, 4, 4, 4, 3, 4],
              [4, 4, 4, 4, 4, 4, 4, 4],
              [1, 1, 2, 3, 3, 2, 1, 1],
              [1, 2, 3, 4, 4, 3, 2, 1],
              [1, 2, 3, 4, 4, 3, 2, 1],
              [1, 1, 2, 3, 3, 2, 1, 1],
              [4, 4, 4, 4, 4, 4, 4, 4],
              [4, 3, 4, 4, 4, 4, 3, 4]]

whitePawnScores = [[8, 8, 8, 8, 8, 8, 8, 8],
                   [8, 8, 8, 8, 8, 8, 8, 8],
                   [5, 6, 6, 7, 7, 6, 6, 5],
                   [2, 3, 3, 5, 5, 3, 3, 2],
                   [1, 2, 3, 4, 4, 3, 2, 1],
                   [1, 1, 2, 3, 3, 2, 1, 1],
                   [1, 1, 1, 0, 0, 1, 1, 1],
                   [0, 0, 0, 0, 0, 0, 0, 0]]

blackPawnScores = [[0, 0, 0, 0, 0, 0, 0, 0],
                   [1, 1, 1, 0, 0, 1, 1, 1],
                   [1, 1, 2, 3, 3, 2, 1, 1],
                   [1, 2, 3, 4, 4, 3, 2, 1],
                   [2, 3, 3, 5, 5, 3, 3, 2],
                   [5, 6, 6, 7, 7, 6, 6, 5],
                   [8, 8, 8, 8, 8, 8, 8, 8],
                   [8, 8, 8, 8, 8, 8, 8, 8]]

piecePositionScores = {"N": knightScores, "B": bishopScores, "Q": queenScores, "R": rookScores, "bp": blackPawnScores, "wp": whitePawnScores}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 2

def calculate_probability(difficulty_rating):
    if difficulty_rating == 1:
        return 0.7  # 80% chance of playing a random move for lowest difficulty
    elif difficulty_rating == 2:
        return 0.5  # 70% chance of playing a random move
    elif difficulty_rating == 3:
        return 0.4  # 60% chance of playing a random move
    elif difficulty_rating == 4:
        return 0.3  # 50% chance of playing a random move
    elif difficulty_rating == 5:
        return 0.2  # 40% chance of playing a random move
    elif difficulty_rating == 6:
        return 0.1  # 30% chance of playing a random move
    elif difficulty_rating == 7:
        return 0.08  # 20% chance of playing a random move
    elif difficulty_rating == 8:
        return 0.07  # 10% chance of playing a random move for highest difficulty
    else:
        return 0.0  # No chance of playing a random move if difficulty rating is out of range

def calculate_depth(difficulty_rating):
    # Adjust depth based on difficulty rating
    if difficulty_rating in [1, 2]:
        return 2
    elif difficulty_rating in [3, 4, 5]:
        return 3
    elif difficulty_rating in [6, 7, 8]:
        return 4

    
def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]


def findBestMove(gs, validMoves, opponent_mode, difficulty_rating):
    global nextMove, counter
    nextMove = None
    depth = calculate_depth(difficulty_rating)
    
    if random.random() < calculate_probability(difficulty_rating):
        return findRandomMove(validMoves)
    
    if int(opponent_mode) == 2:
        nega_Moves = Model.find_model_moves(validMoves, gs.board)
    else:
        nega_Moves = validMoves
    random.shuffle(nega_Moves)
    counter = 0
    # findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove)
    #findMoveNegaMax(gs, validMoves, DEPTH, 1 if gs.whiteToMove else -1)
    findMoveNegaMaxAlphaBeta(gs, nega_Moves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    print(counter)
    return nextMove


def findMoveNegaMaxAlphaBeta(gs, modelMoves, depth, alpha, beta, turnMultiplier):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier*scoreBoard(gs)
    
    
    maxScore = -CHECKMATE
    for move in modelMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        random.shuffle(nextMoves)
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
        #pruning
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break 
    return maxScore

def scoreBoard(gs):
    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gs.staleMate:
        return STALEMATE 
    score = 0
    for row in range(len(gs.board)):
        for column in range(len(gs.board[row])):
            square = gs.board[row][column]
            if square != "--":
                piecePositionScore = 0
                protection_bonus = 0
                #score it positionally
                if square[1] != "K":
                    if square[1] == "p":
                        piecePositionScore = piecePositionScores[square][row][column]
                    else:
                        piecePositionScore = piecePositionScores[square[1]][row][column]
                
                # if isPieceProtectedByOwn(gs, row, column):
                #     protection_bonus = 0.3  # Add a bonus for being protected
                # else:
                #     protection_bonus = 0
                    
                if (square[1] == "K" and square[0] == 'w' and (gs.currentCastlingRight.wks or gs.currentCastlingRight.wqs)):
                    castling_bonus = 0.5  # Award points for potential castling
                elif (square[1] == "K" and square[0] == 'b' and (gs.currentCastlingRight.bks or gs.currentCastlingRight.bqs)):
                    castling_bonus = 0.5  # Award points for potential castling
                else:
                    castling_bonus = 0
                    
                if square[0] == 'w':
                    score += (pieceScore[square[1]] + piecePositionScore*0.1 + protection_bonus + castling_bonus)
                elif square[0] == 'b':
                    score -= (pieceScore[square[1]] + piecePositionScore*0.1 + protection_bonus + castling_bonus)
    if gs.whiteToMove:
        score += 0.05 * len(gs.getValidMoves())  # Adjust based on the number of possible moves
    else:
        score -= 0.05 * len(gs.getValidMoves())
    
    return score

# def isPieceProtectedByOwn(gs, row, column):
#     piece_color = gs.board[row][column][0]
#     for r in range(len(gs.board)):
#         for c in range(len(gs.board[r])):
#             if gs.board[r][c][0] == piece_color and (r, c) != (row, column):
#                 valid_moves = gs.getValidMoves()
#                 for move in valid_moves:
#                     if move.endRow == row and move.endCol == column:
#                         return True  # The piece is protected by another piece of the same color
#     return False  # No own piece protects the piece


# def scoreMaterial(board):
#     score = 0
#     for row in board:
#         for square in row:
#             if square[0] == 'w':
#                 score += pieceScore[square[1]]
#             elif square[0] == 'b':
#                 score -= pieceScore[square[1]]
    
#     return score












# def findRandomMove(validMoves):
#     return validMoves[random.randint(0, len(validMoves)-1)]

# def findBestMoveNoRecursion(gs, validMoves):
#     turnMultiplier = 1 if gs.whiteToMove else -1
#     opponentMinMaxScore = CHECKMATE
#     bestPlayerMove = None
#     random.shuffle(validMoves)
#     for playerMove in validMoves:
#         gs.makeMove(playerMove)
#         opponentsMoves = gs.getValidMoves()
#         if gs.staleMate:
#             opponentMaxScore = STALEMATE
#         elif gs.checkMate:
#             opponentMaxScore = -CHECKMATE
#         else:
#             opponentMaxScore = -CHECKMATE
#             for opponentsMove in opponentsMoves:
#                 gs.makeMove(opponentsMove)
#                 gs.getValidMoves()
#                 if gs.checkMate:
#                     score = -turnMultiplier*CHECKMATE
#                 elif gs.staleMate:
#                     score = STALEMATE
#                 else:
#                     score = -turnMultiplier*scoreMaterial(gs.board)
#                 if(score > opponentMaxScore):
#                     opponentMaxScore = score
#                 gs.undoMove()
#         if opponentMaxScore < opponentMinMaxScore:
#             opponentMinMaxScore = opponentMaxScore
#             bestPlayerMove = playerMove
#         gs.undoMove()
#     return bestPlayerMove

# def findMoveMinMax(gs, validMoves, depth, whiteToMove):
#     global nextMove
#     if depth == 0:
#         return scoreMaterial(gs.board)
    
#     if whiteToMove:
#         maxScore = -CHECKMATE
#         for move in validMoves:
#             gs.makeMove(move)
#             nextMoves = gs.getValidMoves()
#             random.shuffle(nextMoves)
#             score = findMoveMinMax(gs, nextMoves, depth - 1, False)
#             if score > maxScore:
#                 maxScore = score
#                 if depth == DEPTH:
#                     nextMove = move
#             gs.undoMove()
#         return maxScore
    
#     else:
#         minScore = CHECKMATE
#         for move in validMoves:
#             gs.makeMove(move)
#             nextMoves = gs.getValidMoves()
#             random.shuffle(nextMoves)
#             score = findMoveMinMax(gs, nextMoves, depth - 1, True)
#             if score < minScore:
#                 minScore = score
#                 if depth == DEPTH:
#                     nextMove = move
#             gs.undoMove()
#         return minScore
    
# def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
#     global nextMove, counter
#     counter += 1
#     if depth == 0:
#         return turnMultiplier*scoreBoard(gs)
    
#     maxScore = -CHECKMATE
#     for move in validMoves:
#         gs.makeMove(move)
#         nextMoves = gs.getValidMoves()
#         random.shuffle(nextMoves)
#         score = -findMoveNegaMax(gs, nextMoves, depth - 1, -turnMultiplier)
#         if score > maxScore:
#             maxScore = score
#             if depth == DEPTH:
#                 nextMove = move
#         gs.undoMove()
#     return maxScore
