document.addEventListener("DOMContentLoaded", function () {
    AOS.init({ duration: 800 });

    /* --- 1. MATRIX RAIN EFFECT --- */
    const canvas = document.getElementById('matrixCanvas');
    const ctx = canvas.getContext('2d');

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789@#$%^&*()*&^%";
    const fontSize = 16;
    const columns = canvas.width / fontSize;
    const drops = [];

    for (let x = 0; x < columns; x++) drops[x] = 1;

    function drawMatrix() {
        ctx.fillStyle = "rgba(13, 13, 13, 0.05)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = "#0F0"; // Green text
        ctx.font = fontSize + "px monospace";

        for (let i = 0; i < drops.length; i++) {
            const text = letters.charAt(Math.floor(Math.random() * letters.length));
            ctx.fillText(text, i * fontSize, drops[i] * fontSize);

            if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                drops[i] = 0;
            }
            drops[i]++;
        }
    }
    setInterval(drawMatrix, 33);

    /* --- 2. SORTING VISUALIZER --- */
    const container = document.getElementById('arrayContainer');
    const btnSort = document.getElementById('btnSort');
    const compCount = document.getElementById('compCount');
    let bars = [];

    // Init Bars
    function initBars() {
        container.innerHTML = "";
        bars = [];
        for (let i = 0; i < 15; i++) {
            const h = Math.floor(Math.random() * 150) + 20;
            const bar = document.createElement('div');
            bar.classList.add('bar');
            bar.style.height = h + 'px';
            container.appendChild(bar);
            bars.push({ el: bar, val: h });
        }
        compCount.innerText = "0";
    }
    initBars();

    // Bubble Sort Animation
    btnSort.addEventListener('click', async () => {
        btnSort.disabled = true;
        let count = 0;

        for (let i = 0; i < bars.length; i++) {
            for (let j = 0; j < bars.length - i - 1; j++) {

                // Highlight comparison
                bars[j].el.classList.add('active');
                bars[j + 1].el.classList.add('active');

                await new Promise(r => setTimeout(r, 100)); // Delay

                if (bars[j].val > bars[j + 1].val) {
                    // Swap heights
                    let temp = bars[j].val;
                    bars[j].val = bars[j + 1].val;
                    bars[j + 1].val = temp;

                    bars[j].el.style.height = bars[j].val + 'px';
                    bars[j + 1].el.style.height = bars[j + 1].val + 'px';
                }

                count++;
                compCount.innerText = count;

                // Remove highlight
                bars[j].el.classList.remove('active');
                bars[j + 1].el.classList.remove('active');
            }
            // Mark as sorted
            bars[bars.length - i - 1].el.classList.add('sorted');
        }
        bars[0].el.classList.add('sorted');
        btnSort.disabled = false;
        setTimeout(initBars, 2000); // Reset after 2s
    });
});