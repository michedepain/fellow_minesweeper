import React from 'react';
 import Cell from './Cell';
 import { revealCell } from '../api';

 function GameBoard({ gameId, boardState, gameOver, gameWon, setGameState}) {

     const handleCellClick = async (row, col) => {
        console.log('gameID', gameId);
         if (gameOver || gameWon) {
             return; // Don't allow clicks if the game is over
         }
         try{
             const updatedGame = await revealCell(gameId, row, col);
             console.log('updatedGame', updatedGame);
             // Make sure gameId is preserved in the updated state
             setGameState(updatedGame);
         }catch(error){
             console.error("Failed to reveal the cell", error)
         }

     };

     if (!boardState) {
         return <div>Loading...</div>;
     }

     return (
         <div className="game-board">
             {boardState.map((row, rowIndex) => (
                 <div key={rowIndex} className="board-row">
                     {row.map((cellState, colIndex) => (
                         <Cell
                             key={colIndex}
                             value={cellState}
                             onClick={() => handleCellClick(rowIndex, colIndex)}
                             gameOver={gameOver}
                         />
                     ))}
                 </div>
             ))}
             {gameOver && <div className="game-over-message">Game Over!</div>}
             {gameWon && <div className="game-won-message">You Won!</div>}
         </div>
     );
 }

 export default GameBoard;