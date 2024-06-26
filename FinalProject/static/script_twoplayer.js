var board = null
var game = new Chess();
// var whiteSquareGrey = '#ffdccf';
var whiteSquareGrey = '#ffe5ef';
var blackSquareGrey = '#ffa591';
var isFlipEnabled = true; // Variable to track if board flipping is enabled

// Function to toggle board flipping
function toggleBoardFlip() {
  isFlipEnabled = !isFlipEnabled; // Toggle the flip status
  $('#flipBtn').text('Flip Orientation: ' + (isFlipEnabled ? 'On' : 'Off'));
}

function removeGreySquares() {
  $('#board1 .square-55d63').css('background', '');
}

function greySquare(square) {
  var $square = $('#board1 .square-' + square);

  var background = whiteSquareGrey;
  if ($square.hasClass('black-3c85d')) {
    background = blackSquareGrey;
  }

  $square.css('background', background);
}

function onDragStart(source, piece) {
  // do not pick up pieces if the game is over
  if (game.game_over()) return false;

  // or if it's not that side's turn
  if ((game.turn() === 'w' && piece.search(/^b/) !== -1) ||
    (game.turn() === 'b' && piece.search(/^w/) !== -1)) {
    return false;
  }
}

function onDrop(source, target) {
  removeGreySquares();

  // see if the move is legal
  var move = game.move({
    from: source,
    to: target,
    promotion: 'q' // NOTE: always promote to a queen for example simplicity
  });

  // illegal move
  if (move === null) return 'snapback';
  if (isFlipEnabled && (game.turn() === 'w' || game.turn() == 'b')) {
    board.flip();
  }
}

function onMouseoverSquare(square, piece) {
  // get list of possible moves for this square
  var moves = game.moves({
    square: square,
    verbose: true
  });

  // exit if there are no moves available for this square
  if (moves.length === 0) return;

  // highlight the square they moused over
  greySquare(square);

  // highlight the possible squares for this piece
  for (var i = 0; i < moves.length; i++) {
    greySquare(moves[i].to);
  }
}

function onMouseoutSquare(square, piece) {
  removeGreySquares();
}

function onSnapEnd() {
  board.position(game.fen());
}

// Initialize the chessboard
var config = {
    draggable: true,
    position: 'start',
    onDragStart: onDragStart,
    onDrop: onDrop,
    onMouseoutSquare: onMouseoutSquare,
    onMouseoverSquare: onMouseoverSquare,
    onSnapEnd: onSnapEnd
}

var board = ChessBoard('board1', config)

$('#startBtn').on('click', function() {
    // Set the board to the starting position
    board.position('start');
  
    // Reset board orientation if it was flipped
    board.orientation('white');
    // Manually set the FEN for the starting position with white to move
    game.load('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1');
  });
  
  

$('#clearBtn').on('click', board.clear)

$('#flipBtn').on('click', toggleBoardFlip);

