$(document).ready(function() {
    var game = new Chess();
    var whiteSquareGrey = '#ffe5ef';
    var blackSquareGrey = '#ffa591';
    var isGameStarted = false;

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
        if (move === null) {
            return 'snapback';
        } else {
            submitMove(source + target);
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

    var config = {
      draggable: true,
      position: 'start', // Initial position, can be changed later
      onDragStart: onDragStart,
      onDrop: onDrop,
      onMouseoutSquare: onMouseoutSquare,
      onMouseoverSquare: onMouseoverSquare,
      onSnapEnd: onSnapEnd
    };
  
    var board = ChessBoard('board', config);
  
    $('#gameForm').submit(function(event) {
      event.preventDefault(); // Prevent form submission
  
      var opponentMode = $('#opponentMode').val();
      var difficultyRating = $('#difficultyRating').val();
      var playAs = $('#playAs').val();
      isGameStarted = true;
      restartGame();
  
      // Make AJAX request to the backend to get the initial FEN position
      $.ajax({
        url: '/play',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
          opponentMode: opponentMode,
          difficultyRating: difficultyRating,
          playAs: playAs
        }),
        success: function(response) {
          console.log(opponentMode);
          console.log(difficultyRating);
          console.log(playAs);
          console.log('Success:', response);
          game.reset();
          var initialFEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'; // Starting position
          board.position(initialFEN);
          
          // Flip the board if the user selects to play as black
          if (playAs === '1') { // '1' corresponds to playing as black
            board.orientation('black');
            $.ajax({
              url: '/make_first_move',
              type: 'POST',
              contentType: 'application/json',
              data: JSON.stringify({}),
              success: function(response) {
                  var processedMove = response.processed_move;
                  console.log('Processed move:', processedMove);

                  // Play the processed move on the board
                  makeMove(processedMove);

                  game.move({
                      from: processedMove.substring(0, 2), // Extract the 'from' square from processedMove
                      to: processedMove.substring(3), // Extract the 'to' square from processedMove
                      promotion: 'q'
                  });

                  game.turn(game.turn() === 'w' ? 'b' : 'w');
              },
              error: function(xhr, status, error) {
                  console.error('Error:', error);
              }
          });
          } else {
            board.orientation('white');
          }
        },
        error: function(xhr, status, error) {
          console.error('Error:', error);
        }
      });
    });

    function makeMove(move) {
        board.move(move);
    }

    function submitMove(move) {

        if (!isGameStarted) {
            console.log("Please start the game first.");
            return;
        }

        // Make AJAX request to the backend to process the move
        $.ajax({
            url: '/make_move',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                move: move
            }),
            success: function(response) {
                var processedMove = response.processed_move;
                console.log('Processed move:', processedMove);
                
                // Play the processed move on the board
                makeMove(processedMove);

                game.move({
                  from: processedMove.substring(0, 2), // Extract the 'from' square from processedMove
                  to: processedMove.substring(3),   // Extract the 'to' square from processedMove
                  promotion: 'q'
                });

                game.turn(game.turn() === 'w' ? 'b' : 'w');
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
            }
        });
    }

    function restartGame() {
      $.ajax({
          type: 'POST',
          url: '/restart_game',
          contentType: 'application/json',
          success: function(response) {
              // Optionally, you can perform any additional actions after restarting the game
              console.log(response.message); // Log success message
              // Add any additional logic here, such as resetting the game board UI
          },
          error: function(xhr, status, error) {
              // Handle errors if needed
              console.error('Error restarting game:', error);
          }
      });
    }

    restartGame();
  });
