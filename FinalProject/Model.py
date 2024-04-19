import tensorflow as tf
import pandas as pd
import numpy as np
import os
from collections import OrderedDict
from operator import itemgetter
import ChessEngine

def get_move_features(move):
    from_ = np.zeros(64)
    to_ = np.zeros(64)
    alphaToNum = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    from_square = move.startCol + ((7 - move.startRow)*8)
    to_square = move.endCol + ((7 - move.endRow)*8)
    from_[from_square] = 1
    to_[to_square] = 1
    return from_, to_
  
def get_board_features(board):
  board_features = []
  default = "None"
  for i in range(7, -1, -1):
    for j in range(7, -1, -1):
      current_piece = board[i][j]
      if current_piece[0] == "b":
        board_features.append(current_piece[1].lower())
      elif current_piece[0] == "w":
        board_features.append(current_piece[1].upper())
      else:
        board_features.append(default)
  return board_features

def get_square_names():
  square_names = ['a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1', 'a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2', 'a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3', 'a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4', 'a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5', 'a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6', 'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7', 'a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8']
  return square_names
  
def predict(df_eval, imported_model):
    col_names = df_eval.columns
    dtypes = df_eval.dtypes
    predictions = []
    for row in df_eval.iterrows():
      example = tf.train.Example()
      for i in range(len(col_names)):
        dtype = dtypes[i]
        col_name = col_names[i]
        value = row[1][col_name]
        if dtype == 'object':
          value = bytes(value, 'utf-8')
          example.features.feature[col_name].bytes_list.value.extend([value])
        elif dtype == 'float':
          example.features.feature[col_name].float_list.value.extend([value])
        elif dtype == 'int':
          example.features.feature[col_name].int64_list.value.extend([value])
      predictions.append(imported_model.signatures['predict'](examples = tf.constant([example.SerializeToString()])))
    return predictions

def get_possible_moves_data(board, validMoves):
    
    data = []
    moves = validMoves
    for move in moves:
      from_square, to_square = get_move_features(move)
      row = np.concatenate((get_board_features(board), from_square, to_square))
      data.append(row)
    
    board_feature_names = get_square_names()
    move_from_feature_names = ['from_' + square for square in board_feature_names]
    move_to_feature_names = ['to_' + square for square in board_feature_names]
    
    columns = board_feature_names + move_from_feature_names + move_to_feature_names
    
    df = pd.DataFrame(data = data, columns = columns)

    for column in move_from_feature_names:
      df[column] = df[column].astype(float)
    for column in move_to_feature_names:
      df[column] = df[column].astype(float)
    return df

def find_model_moves(validMoves, board, proportion = 0.5):
  
    moves = validMoves
    model = tf.saved_model.load("")
    df_eval = get_possible_moves_data(board, validMoves)
    predictions = predict(df_eval, model)
    good_move_probas = []
    
    for prediction in predictions:
      proto_tensor = tf.make_tensor_proto(prediction['probabilities'])
      proba = tf.make_ndarray(proto_tensor)[0][1]
      good_move_probas.append(proba)
    
    move_tuples = [(move.startRow, move.startCol, move.endRow, move.endCol, move.isenpassantMove, move.isCastleMove) for move in moves]
    dict_ = dict(zip(move_tuples, good_move_probas))
    dict_ = OrderedDict(sorted(dict_.items(), key = itemgetter(1), reverse = True))
    
    best_move_tuples = list(dict_.keys())
    
    best_moves = [ChessEngine.Move((startRow, startCol), (endRow, endCol), board, isenpassantMove, isCastleMove) for startRow, startCol, endRow, endCol, isenpassantMove, isCastleMove in best_move_tuples]
 
    return best_moves[0:int(len(best_moves)*proportion)]