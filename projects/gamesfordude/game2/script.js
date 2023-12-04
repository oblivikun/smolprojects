let gameArea = document.querySelector("#gameArea");
let player = document.querySelector("#player");
let scoreDisplay = document.querySelector("#score");
let startButton = document.querySelector("#startButton");
let playing = false;
let score = 0;

function startGame() {
  playing = true;
  score = 0;
  scoreDisplay.textContent = `Score: ${score}`;
  player.style.left = '0px';  // Start player on the left side
  startButton.disabled = true;
  spawnObstacle();
}

function spawnObstacle() {
  let obstacle = document.createElement("div");
  obstacle.classList.add("obstacle");
  
  // Randomly position the obstacle along the width of the game area
  let gameAreaWidth = gameArea.offsetWidth;
  let randomX = Math.floor(Math.random() * (gameAreaWidth - obstacle.offsetWidth));
  obstacle.style.left = `${randomX}px`;
  
  gameArea.appendChild(obstacle);
  
  // Start moving the obstacle
  moveObstacle(obstacle);
}

function moveObstacle(obstacle) {
  let speed = 5;  // Adjust this to make the game faster or slower
  let intervalId = setInterval(function() {
    let currentTop = parseInt(obstacle.style.top) || 0;
    if (currentTop > gameArea.offsetHeight) {
      // The obstacle has gone off the bottom of the screen, remove it
      clearInterval(intervalId);
      gameArea.removeChild(obstacle);
    } else if (/* check for collision with player */) {
      // The obstacle has hit the player, end the game
      clearInterval(intervalId);
      endGame();
    } else {
      // Move the obstacle down
      obstacle.style.top = `${currentTop + speed}px`;
    }
  }, 20);
}

function flipPlayer() {
  // Moves player to the opposite side of the game area
  let gameAreaWidth = gameArea.offsetWidth;
  let playerX = parseInt(player.style.left) || 0;
  if (playerX === 0) {
    player.style.left = `${gameAreaWidth - player.offsetWidth}px`;
  } else {
    player.style.left = '0px';
  }
}

function endGame() {
  playing = false;
  startButton.disabled = false;
  alert(`Game over! Your score was ${score}.`);
}

startButton.addEventListener("click", startGame);
gameArea.addEventListener("click", flipPlayer);