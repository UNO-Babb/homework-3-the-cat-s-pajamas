
#Logic is in this python file

from flask import Flask, render_template, request, jsonify
import chess

app = Flask(__name__)
board = chess.Board()

def custom_board_setup():
    board.clear()

    # White back row with king in the middle
    for i in range(8):
        board.set_piece_at(chess.square(i, 0), chess.Piece(chess.QUEEN, chess.WHITE))
    board.set_piece_at(chess.E1, chess.Piece(chess.KING, chess.WHITE))  # E1 = white king

    # White "pawns" as queens
    for i in range(8):
        board.set_piece_at(chess.square(i, 1), chess.Piece(chess.QUEEN, chess.WHITE))

    # Black back row with king in the middle
    for i in range(8):
        board.set_piece_at(chess.square(i, 7), chess.Piece(chess.QUEEN, chess.BLACK))
    board.set_piece_at(chess.E8, chess.Piece(chess.KING, chess.BLACK))  # E8 = black king

    # Black "pawns" as queens
    for i in range(8):
        board.set_piece_at(chess.square(i, 6), chess.Piece(chess.QUEEN, chess.BLACK))

custom_board_setup()

@app.route('/')
def index():
    return render_template('index.html', fen=board.fen())

@app.route('/move', methods=['POST'])
def move():
    data = request.get_json()
    move_uci = data.get("move")
    move = chess.Move.from_uci(move_uci)

    response = {'valid': False, 'fen': board.fen()}

    if move in board.legal_moves:
        board.push(move)
        response['valid'] = True
        response['fen'] = board.fen()

        if board.is_checkmate():
            response['game_over'] = True
            response['result'] = 'Checkmate'
        elif board.is_stalemate():
            response['game_over'] = True
            response['result'] = 'Stalemate'
        elif board.is_insufficient_material():
            response['game_over'] = True
            response['result'] = 'Draw - Insufficient Material'
        elif board.can_claim_fifty_moves():
            response['game_over'] = True
            response['result'] = 'Draw - 50-move Rule'
        elif board.can_claim_threefold_repetition():
            response['game_over'] = True
            response['result'] = 'Draw - Threefold Repetition'

    return jsonify(response)

@app.route('/reset', methods=['POST'])
def reset():
    custom_board_setup()
    return jsonify({'fen': board.fen(), 'reset': True})

if __name__ == '__main__':
    app.run(debug=True, port=5003)
