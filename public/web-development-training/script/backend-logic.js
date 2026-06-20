document.addEventListener("DOMContentLoaded", function () {
    AOS.init({ duration: 800 });

    /* --- 1. MATRIX RAIN --- */
    const canvas = document.getElementById('matrixCanvas');
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    const chars = "01";
    const fontSize = 14;
    const columns = canvas.width / fontSize;
    const drops = Array(Math.floor(columns)).fill(1);

    function draw() {
        ctx.fillStyle = "rgba(0, 0, 0, 0.05)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "#0F0";
        ctx.font = fontSize + "px monospace";
        for (let i = 0; i < drops.length; i++) {
            const text = chars.charAt(Math.floor(Math.random() * chars.length));
            ctx.fillText(text, i * fontSize, drops[i] * fontSize);
            if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
            drops[i]++;
        }
    }
    setInterval(draw, 50);

    /* --- 2. API SIMULATOR --- */
    const btnSend = document.getElementById('btnSend');
    const output = document.getElementById('consoleOutput');
    const dbBox = document.getElementById('dbVisual');
    const bar = document.querySelector('.loading-bar');

    btnSend.addEventListener('click', () => {
        btnSend.disabled = true;
        output.innerHTML = `<span class='text-gray'>Connecting to localhost:3000...</span>`;
        dbBox.classList.add('d-none');
        bar.style.width = "0%";

        setTimeout(() => {
            output.innerHTML += `<br><span class='text-blue'>Server:</span> Processing request...`;
            dbBox.classList.remove('d-none'); // Show DB logic

            setTimeout(() => { bar.style.width = "100%"; }, 100); // DB Scan animation

            setTimeout(() => {
                output.innerHTML += `<br><span class='text-green'>200 OK</span><br>`;
                output.innerHTML += `{ "id": 1, "name": "John Doe", "role": "Admin" }`;
                btnSend.disabled = false;
            }, 1500);
        }, 800);
    });
});