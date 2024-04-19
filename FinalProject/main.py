from flask import Flask, render_template, request, jsonify, session
import os
import uuid
import shutil
from ChessEngine import GameState, Move
import ChessAI

game_state = GameState()

app = Flask(__name__)
app.secret_key = 'abcdefgh'  # Set a secret key for session management

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/single_player.html')
def single_player():
    return render_template('single_player.html')

@app.route('/two_player.html')
def two_player():
    return render_template('two_player.html')

@app.route('/play', methods=['POST'])
def play():
    
    json_data = request.get_json()
    # Get the values from the request
    
    session['opponent_mode'] = request.json.get('opponentMode')
    session['difficulty_rating'] = request.json.get('difficultyRating')
    session['play_as'] = request.json.get('playAs')
    print("Received data:", json_data)
    print(session['opponent_mode'], session['difficulty_rating'], session['play_as'])
    
    return jsonify({'message': 'Chess game parameters set successfully'})

@app.route('/make_move', methods=['POST'])
def make_move():
    move = request.json.get('move')
    print("Received move:", move)
    
    playerClicks = convert_input(move)
    move = Move(playerClicks[0], playerClicks[1], game_state.board)
    validMoves = game_state.getValidMoves()
    for i in range(len(validMoves)):
        if move == validMoves[i]:
            game_state.makeMove(validMoves[i])
    validMoves = game_state.getValidMoves()
    AIMove = ChessAI.findBestMove(game_state, validMoves, session['opponent_mode'], session['difficulty_rating'])
    if AIMove is None:
        AIMove = ChessAI.findRandomMove(validMoves)
    game_state.makeMove(AIMove)
    number_to_letter = {
    0: 'a',
    1: 'b',
    2: 'c',
    3: 'd',
    4: 'e',
    5: 'f',
    6: 'g',
    7: 'h'
    }
    number_to_number = {
    0: '8',
    1: '7',
    2: '6',
    3: '5',
    4: '4',
    5: '3',
    6: '2',
    7: '1'
    }
    output_move = ""
    output_move += number_to_letter[AIMove.startCol] + number_to_number[AIMove.startRow] + "-" + number_to_letter[AIMove.endCol] + number_to_number[AIMove.endRow]
    print("Processed move:", output_move)

    return jsonify({'processed_move': output_move}), 200

@app.route('/restart_game', methods=['POST'])
def restart_game():
    global game_state
    game_state = GameState()  # Reset game state
    return jsonify({'message': 'Game restarted successfully'}), 200

@app.route('/make_first_move', methods=['POST'])
def make_first_move():
    global game_state
    game_state = GameState()
    AIMove = ChessAI.findBestMove(game_state, game_state.getValidMoves(), session['opponent_mode'], session['difficulty_rating'])
    if AIMove is None:
        AIMove = ChessAI.findRandomMove(game_state.getValidMoves())
    game_state.makeMove(AIMove)
    number_to_letter = {
    0: 'a',
    1: 'b',
    2: 'c',
    3: 'd',
    4: 'e',
    5: 'f',
    6: 'g',
    7: 'h'
    }
    number_to_number = {
    0: '8',
    1: '7',
    2: '6',
    3: '5',
    4: '4',
    5: '3',
    6: '2',
    7: '1'
    }
    output_move = ""
    output_move += number_to_letter[AIMove.startCol] + number_to_number[AIMove.startRow] + "-" + number_to_letter[AIMove.endCol] + number_to_number[AIMove.endRow]
    print("Processed move:", output_move)

    return jsonify({'processed_move': output_move}), 200

def convert_input(input_move):
    letter_to_number = {
    'a': 0,
    'b': 1,
    'c': 2,
    'd': 3,
    'e': 4,
    'f': 5,
    'g': 6,
    'h': 7
    }
    number_to_number = {
    '8': 0,
    '7': 1,
    '6': 2,
    '5': 3,
    '4': 4,
    '3': 5,
    '2': 6,
    '1': 7
    }
    playerClicks = []
    sqSelected = (int(number_to_number[input_move[1]]), int(letter_to_number[input_move[0]]))
    playerClicks.append(sqSelected)
    sqSelected = (int(number_to_number[input_move[3]]), int(letter_to_number[input_move[2]]))
    playerClicks.append(sqSelected)
    
    return playerClicks

if __name__ == '__main__':
    app.run(debug=True)
