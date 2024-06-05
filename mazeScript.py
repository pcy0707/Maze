function showWindow()
 {
   document.getElementById("myModal").style.display = "block";
 }

 function hideWindow()
 {
   document.getElementById("myModal").style.display = "none";
 }

 window.onclick = function(event)
 {
     if (event.target == document.getElementById)
     {
       document.getElementById("myModal").style.display = "none";
     }
   }

function rand(max) {
 return Math.floor(Math.random() * max);
}


function shuffle(a) {
 for (let i = a.length - 1; i > 0; i--) {
   const j = Math.floor(Math.random() * (i + 1));
   [a[i], a[j]] = [a[j], a[i]];
 }
 return a;
}


function displayVictoryMess(){
 showWindow();
}


function changeColor(color) {
 document.body.style.background = color;
}


function myFunc() {
 changeColor('lightgreen');
 setTimeout(function() {
   displayVictoryMess();
 }, 1);
}  


function endGame(){
 myFunc();
}


function Maze(Width, Height) {
 var mazeMap;
 var width = Width;
 var height = Height;
 var player1Coord, player2Coord;
 var dirs = ["n", "s", "e", "w"];
 var modDir = {
   n: {
     y: -1,
     x: 0,
     o: "s"
   },
   s: {
     y: 1,
     x: 0,
     o: "n"
   },
   e: {
     y: 0,
     x: 1,
     o: "w"
   },
   w: {
     y: 0,
     x: -1,
     o: "e"
   }
 };


 this.map = function() {
   return mazeMap;
 };
 this.player1Coord = function() {
   return player1Coord;
 };
 this.player2Coord = function() {
   return player2Coord;
 };


 function genMap() {
   mazeMap = new Array(height);
   for (y = 0; y < height; y++) {
     mazeMap[y] = new Array(width);
     for (x = 0; x < width; ++x) {
       mazeMap[y][x] = {
         n: false,
         s: false,
         e: false,
         w: false,
         visited: false,
         priorPos: null
       };
     }
   }
 }


 function defineMaze() {
   var isComp = false;
   var move = false;
   var cellsVisited = 1;
   var numLoops = 0;
   var maxLoops = 0;
   var pos = {
     x: 0,
     y: 0
   };
   var numCells = width * height;
   while (!isComp) {
     move = false;
     mazeMap[pos.x][pos.y].visited = true;


     if (numLoops >= maxLoops) {
       shuffle(dirs);
       maxLoops = Math.round(rand(height / 8));
       numLoops = 0;
     }
     numLoops++;
     for (index = 0; index < dirs.length; index++) {
       var direction = dirs[index];
       var nx = pos.x + modDir[direction].x;
       var ny = pos.y + modDir[direction].y;


       if (nx >= 0 && nx < width && ny >= 0 && ny < height) {
         //Check if the tile is already visited
         if (!mazeMap[nx][ny].visited) {
           //Carve through walls from this tile to next
           mazeMap[pos.x][pos.y][direction] = true;
           mazeMap[nx][ny][modDir[direction].o] = true;


           //Set Currentcell as next cells Prior visited
           mazeMap[nx][ny].priorPos = pos;
           //Update Cell position to newly visited location
           pos = {
             x: nx,
             y: ny
           };
           cellsVisited++;
           //Recursively call this method on the next tile
           move = true;
           break;
         }
       }
     }


     if (!move) {
       //  If it failed to find a direction,
       //  move the current position back to the prior cell and Recall the method.
       pos = mazeMap[pos.x][pos.y].priorPos;
     }
     if (numCells == cellsVisited) {
       isComp = true;
     }
   }
 }


 function defineCoord() {
     player1Coord = {
       x: 0,
       y: 0
     };
     player2Coord = {
       x: height - 1,
       y: width - 1
     };
 }


 genMap();
 defineCoord();
 defineMaze();
}


function DrawMaze(Maze, ctx, cellsize,) {
 var map = Maze.map();
 var cellSize = cellsize;
 var drawEndMethod;
 ctx.lineWidth = cellSize / 40;


 this.redrawMaze = function(size) {
   cellSize = size;
   ctx.lineWidth = cellSize / 50;
   drawMap();
   drawEndMethod();
 };


 function drawCell(xCord, yCord, cell) {
   var x = xCord * cellSize;
   var y = yCord * cellSize;


   if (cell.n == false) {
     ctx.beginPath();
     ctx.moveTo(x, y);
     ctx.lineTo(x + cellSize, y);
     ctx.stroke();
   }
   if (cell.s === false) {
     ctx.beginPath();
     ctx.moveTo(x, y + cellSize);
     ctx.lineTo(x + cellSize, y + cellSize);
     ctx.stroke();
   }
   if (cell.e === false) {
     ctx.beginPath();
     ctx.moveTo(x + cellSize, y);
     ctx.lineTo(x + cellSize, y + cellSize);
     ctx.stroke();
   }
   if (cell.w === false) {
     ctx.beginPath();
     ctx.moveTo(x, y);
     ctx.lineTo(x, y + cellSize);
     ctx.stroke();
   }
 }


 function drawMap() {
   for (x = 0; x < map.length; x++) {
     for (y = 0; y < map[x].length; y++) {
       drawCell(x, y, map[x][y]);
     }
   }
 }


 function clear() {
   var canvasSize = cellSize * map.length;
   ctx.clearRect(0, 0, canvasSize, canvasSize);
 }


 clear();
 drawMap();
}




function Player1(maze, c, _cellsize, onComplete, sprite = null) {
 var ctx = c.getContext("2d");
 var drawSprite;
 drawSprite = drawSpriteCircle;
 if (sprite != null) {
   drawSprite = drawSpriteImg;
 }
 var player1 = this;
 var map = maze.map();
 var cellCoords = {
   x: maze.player1Coord().x,
   y: maze.player1Coord().y,
 };
 var cellSize = _cellsize;
 var halfCellSize = cellSize / 2;


 this.redrawPlayer1 = function(_cellsize) {
   cellSize = _cellsize;
   drawSpriteImg(cellCoords);
 };


 function drawSpriteCircle(coord) {
   ctx.beginPath();
   ctx.fillStyle = "red";
   ctx.arc(
     (coord.x + 1) * cellSize - halfCellSize,
     (coord.y + 1) * cellSize - halfCellSize,
     halfCellSize - 2,
     0,
     2 * Math.PI
   );
   ctx.fill();
 }


 function removeSprite(coord) {
   var offsetLeft = cellSize / 50;
   var offsetRight = cellSize / 25;
   ctx.clearRect(
     coord.x * cellSize + offsetLeft,
     coord.y * cellSize + offsetLeft,
     cellSize - offsetRight,
     cellSize - offsetRight
   );
 }


 function check(e) {
   var cell = map[cellCoords.x][cellCoords.y];
    switch (e.keyCode) {
     case 65:
     case 97: // 'a' or 'A' key
       if (cell.w == true) {
         removeSprite(cellCoords);
         cellCoords = { x: cellCoords.x - 1, y: cellCoords.y };
         drawSprite(cellCoords);
       }
       checkCollision();
       break;
     case 87:
     case 119: // 'w' or 'W' key
       if (cell.n == true) {
         removeSprite(cellCoords);
         cellCoords = { x: cellCoords.x, y: cellCoords.y - 1 };
         drawSprite(cellCoords);
       }
       checkCollision();
       break;
     case 68:
     case 100: // 'd' or 'D' key
       if (cell.e == true) {
         removeSprite(cellCoords);
         cellCoords = { x: cellCoords.x + 1, y: cellCoords.y };
         drawSprite(cellCoords);
       }
       checkCollision();
       break;
     case 83:
     case 115: // 's' or 'S' key
       if (cell.s == true) {
         removeSprite(cellCoords);
         cellCoords = { x: cellCoords.x, y: cellCoords.y + 1 };
         drawSprite(cellCoords);
       }
       checkCollision();
       break;
   }
   player1posX = cellCoords.x
   player1posY = cellCoords.y
 }


 this.bindKeyDown = function() {
   window.addEventListener("keydown", check, false);
 };


 this.unbindKeyDown = function() {
   window.removeEventListener("keydown", check, false);
 };


 drawSprite(maze.player1Coord());


 this.bindKeyDown();
}




function Player2(maze, c, _cellsize, onComplete, sprite = null) {
 var ctx = c.getContext("2d");
 var drawSprite;
 drawSprite = drawSpriteCircle;
 if (sprite != null) {
   drawSprite = drawSpriteImg;
 }
 var player2 = this;
 var map = maze.map();
 var cellCoords = {
   x: maze.player2Coord().x,
   y: maze.player2Coord().y
 };
 var cellSize = _cellsize;
 var halfCellSize = cellSize / 2;


 this.redrawPlayer2 = function(_cellsize) {
   cellSize = _cellsize;
   drawSpriteImg(cellCoords);
 };


 function drawSpriteCircle(coord) {
   ctx.beginPath();
   ctx.fillStyle = "blue"; // Change color to differentiate from Player1
   ctx.arc(
     (coord.x + 1) * cellSize - halfCellSize,
     (coord.y + 1) * cellSize - halfCellSize,
     halfCellSize - 2,
     0,
     2 * Math.PI
   );
   ctx.fill();
 }


 function removeSprite(coord) {
   var offsetLeft = cellSize / 50;
   var offsetRight = cellSize / 25;
   ctx.clearRect(
     coord.x * cellSize + offsetLeft,
     coord.y * cellSize + offsetLeft,
     cellSize - offsetRight,
     cellSize - offsetRight
   );
 }


 function check(e) {
   var cell = map[cellCoords.x][cellCoords.y];
    switch (e.keyCode) {
     case 37: // left arrow key
       if (cell.w == true) {
         removeSprite(cellCoords);
         cellCoords = { x: cellCoords.x - 1, y: cellCoords.y };
         drawSprite(cellCoords);
       }
       checkCollision();
       break;
     case 38: // up arrow key
       if (cell.n == true) {
         removeSprite(cellCoords);
         cellCoords = { x: cellCoords.x, y: cellCoords.y - 1 };
         drawSprite(cellCoords);
       }
       checkCollision();
       break;
     case 39: // right arrow key
       if (cell.e == true) {
         removeSprite(cellCoords);
         cellCoords = { x: cellCoords.x + 1, y: cellCoords.y };
         drawSprite(cellCoords);
       }
       checkCollision();
       break;
     case 40: // down arrow key
       if (cell.s == true) {
         removeSprite(cellCoords);
         cellCoords = { x: cellCoords.x, y: cellCoords.y + 1 };
         drawSprite(cellCoords);
       }
       checkCollision();
       break;
   }
   player2posX = cellCoords.x
   player2posY = cellCoords.y
 }






 this.bindKeyDown = function() {
   window.addEventListener("keydown", check, false);
 };


 this.unbindKeyDown = function() {
   window.removeEventListener("keydown", check, false);
 };


 drawSprite(maze.player2Coord());


 this.bindKeyDown();
}


function checkCollision() {
 if (player1posX === player2posX && player1posY === player2posY) {
   endGame();
 }
}


var mazeCanvas = document.getElementById("mazeCanvas");
var ctx = mazeCanvas.getContext("2d");
var sprite;
var maze, draw, player1, player2;
var cellSize;
var difficulty;
// sprite.src = 'media/sprite.png';


function makeMaze() {
 if (player1 != undefined) { //There was a glitch there the ball phases through the wall and this fixes that
   player1.unbindKeyDown();
   player1 = null;
 }
 if (player2 != undefined) {
   player2.unbindKeyDown();
   player2 = null;
 }
 var e = document.getElementById("diffSelect");
 difficulty = e.options[e.selectedIndex].value;
 cellSize = mazeCanvas.width / difficulty;
 maze = new Maze(difficulty, difficulty);
 draw = new DrawMaze(maze, ctx, cellSize);
 player1 = new Player1(maze, mazeCanvas, cellSize, displayVictoryMess, sprite);
 player2 = new Player2(maze, mazeCanvas, cellSize, displayVictoryMess, sprite); // Add Player2 initialization
 if (document.getElementById("mazeContainer").style.opacity < "100") {
   document.getElementById("mazeContainer").style.opacity = "100";
 }
}







