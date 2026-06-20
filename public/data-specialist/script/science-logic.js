document.addEventListener("DOMContentLoaded", function () {
    AOS.init({ duration: 800 });

    /* --- 1. PREDICTION LAB LOGIC --- */
    const btnRun = document.getElementById('btnRun');
    const inputExp = document.getElementById('expInput');
    const outputCell = document.getElementById('outputCell');
    const predText = document.getElementById('predictionText');
    const graphLine = document.querySelector('.graph-line');
    const point = document.querySelector('.graph-point');

    btnRun.addEventListener('click', () => {
        const exp = parseInt(inputExp.value);
        if (!exp) return;

        // Reset
        outputCell.style.display = 'flex';
        predText.innerText = "Running regression model...";
        point.style.display = 'none';

        // Simulate Calculation
        setTimeout(() => {
            // Simple Logic: Base 3L + (1.5L * Years)
            const salary = 3 + (1.5 * exp);
            predText.innerText = `Predicted Salary: ₹${salary} LPA`;

            // Draw Graph
            point.style.display = 'block';
            point.style.left = (exp * 5) + "%"; // Scale x
            point.style.bottom = (exp * 4) + "%"; // Scale y

        }, 800);
    });

    /* --- 2. NEURAL NETWORK BACKGROUND --- */
    const canvas = document.getElementById('neuralCanvas');
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    let particles = [];
    for (let i = 0; i < 50; i++) {
        particles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            vx: (Math.random() - 0.5) * 0.5,
            vy: (Math.random() - 0.5) * 0.5
        });
    }

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        particles.forEach((p, i) => {
            p.x += p.vx;
            p.y += p.vy;

            // Bounce edges
            if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
            if (p.y < 0 || p.y > canvas.height) p.vy *= -1;

            ctx.fillStyle = "rgba(79, 70, 229, 0.5)";
            ctx.beginPath();
            ctx.arc(p.x, p.y, 2, 0, Math.PI * 2);
            ctx.fill();

            // Connect
            particles.slice(i + 1).forEach(p2 => {
                const dist = Math.hypot(p.x - p2.x, p.y - p2.y);
                if (dist < 150) {
                    ctx.strokeStyle = `rgba(79, 70, 229, ${1 - dist / 150})`;
                    ctx.beginPath();
                    ctx.moveTo(p.x, p.y);
                    ctx.lineTo(p2.x, p2.y);
                    ctx.stroke();
                }
            });
        });
        requestAnimationFrame(animate);
    }
    animate();
});