document.addEventListener("DOMContentLoaded", function () {
    AOS.init({ duration: 800 });

    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    const ui = document.getElementById('gameUI');
    const startBtn = document.getElementById('startBtn');
    const scoreBoard = document.getElementById('scoreBoard');
    const scoreVal = document.getElementById('scoreVal');
    const gameOverScreen = document.getElementById('gameOverScreen');
    const finalScore = document.getElementById('finalScore');
    const restartBtn = document.getElementById('restartBtn');

    // Resize Canvas
    canvas.width = 800;
    canvas.height = 400;

    let gameRunning = false;
    let score = 0;
    let player = { x: 400, y: 350, width: 30, height: 30, color: '#00f3ff' };
    let bullets = [];
    let enemies = [];
    let animationId;
    let enemyInterval;

    // --- GAME FUNCTIONS ---

    function initGame() {
        ui.classList.add('d-none');
        gameOverScreen.classList.add('d-none');
        scoreBoard.classList.remove('d-none');
        gameRunning = true;
        score = 0;
        scoreVal.innerText = 0;
        bullets = [];
        enemies = [];
        player.x = canvas.width / 2;

        spawnEnemies();
        animate();
    }

    function spawnEnemies() {
        enemyInterval = setInterval(() => {
            const x = Math.random() * (canvas.width - 30);
            enemies.push({ x: x, y: -30, width: 30, height: 30, speed: Math.random() * 2 + 1 });
        }, 1000);
    }

    function animate() {
        if (!gameRunning) return;
        animationId = requestAnimationFrame(animate);
        ctx.fillStyle = 'rgba(0, 0, 0, 0.2)'; // Trails effect
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Player
        ctx.fillStyle = player.color;
        ctx.beginPath();
        ctx.moveTo(player.x, player.y);
        ctx.lineTo(player.x - 15, player.y + 30);
        ctx.lineTo(player.x + 15, player.y + 30);
        ctx.fill();

        // Bullets
        bullets.forEach((bullet, index) => {
            bullet.y -= 5;
            ctx.fillStyle = '#Fcee0a';
            ctx.fillRect(bullet.x - 2, bullet.y, 4, 10);

            // Remove off-screen
            if (bullet.y < 0) bullets.splice(index, 1);
        });

        // Enemies
        enemies.forEach((enemy, index) => {
            enemy.y += enemy.speed;
            ctx.fillStyle = '#ff003c';
            ctx.fillRect(enemy.x, enemy.y, enemy.width, enemy.height);

            // Collision: Enemy hits Player
            const dist = Math.hypot(player.x - (enemy.x + 15), player.y - enemy.y);
            if (dist - 15 - 15 < 1) {
                endGame();
            }

            // Remove off-screen
            if (enemy.y > canvas.height) enemies.splice(index, 1);

            // Collision: Bullet hits Enemy
            bullets.forEach((bullet, bIndex) => {
                if (bullet.x > enemy.x && bullet.x < enemy.x + enemy.width &&
                    bullet.y > enemy.y && bullet.y < enemy.y + enemy.height) {

                    // Explosion Effect (Simple)
                    ctx.fillStyle = '#fff';
                    ctx.fillRect(enemy.x, enemy.y, 30, 30);

                    enemies.splice(index, 1);
                    bullets.splice(bIndex, 1);
                    score += 10;
                    scoreVal.innerText = score;
                }
            });
        });
    }

    function endGame() {
        gameRunning = false;
        cancelAnimationFrame(animationId);
        clearInterval(enemyInterval);
        gameOverScreen.classList.remove('d-none');
        finalScore.innerText = score;
    }

    // --- CONTROLS ---

    canvas.addEventListener('mousemove', (e) => {
        const rect = canvas.getBoundingClientRect();
        player.x = e.clientX - rect.left;
    });

    canvas.addEventListener('click', () => {
        if (gameRunning) {
            bullets.push({ x: player.x, y: player.y });
        }
    });

    startBtn.addEventListener('click', initGame);
    restartBtn.addEventListener('click', initGame);
});