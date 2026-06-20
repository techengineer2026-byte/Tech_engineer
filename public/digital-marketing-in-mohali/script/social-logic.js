document.addEventListener("DOMContentLoaded", function () {
    AOS.init({ duration: 800 });

    const btnPost = document.getElementById('btnPost');
    const viewCount = document.getElementById('viewCount');
    const feedbackText = document.getElementById('feedbackText');
    const stream = document.getElementById('reactionStream');
    const hookSelect = document.getElementById('hookSelect');

    let isRunning = false;

    // Toggle Content Type UI
    window.setType = function (type) {
        document.querySelectorAll('.type-option').forEach(el => el.classList.remove('active'));
        event.currentTarget.classList.add('active');
    };

    btnPost.addEventListener('click', () => {
        if (isRunning) return;
        isRunning = true;

        const hook = hookSelect.value;
        let finalViews = 0;
        let message = "";

        // Logic based on hook
        if (hook === 'bored') {
            finalViews = Math.floor(Math.random() * 500); // Low views
            message = "Flopped. Boring hooks don't work.";
        } else {
            finalViews = Math.floor(Math.random() * 50000) + 10000; // High views
            message = "VIRAL! Great Hook!";
        }

        btnPost.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Posting...';
        viewCount.innerText = "0";
        feedbackText.innerText = "";

        setTimeout(() => {
            btnPost.innerHTML = 'POSTED!';

            // Animate Numbers
            let current = 0;
            const step = Math.ceil(finalViews / 100);

            const timer = setInterval(() => {
                current += step;
                if (current >= finalViews) {
                    current = finalViews;
                    clearInterval(timer);
                    isRunning = false;
                    btnPost.innerHTML = 'POST AGAIN';
                    feedbackText.innerText = message;
                    if (hook !== 'bored') feedbackText.style.color = "#00e676"; // Green
                    else feedbackText.style.color = "#ff1744"; // Red
                }
                viewCount.innerText = current.toLocaleString();

                // Spawn Emojis if viral
                if (hook !== 'bored' && Math.random() > 0.5) spawnEmoji();

            }, 20);

        }, 1000);
    });

    function spawnEmoji() {
        const emojis = ['🔥', '❤️', '😍', '🚀', '👏'];
        const el = document.createElement('div');
        el.classList.add('flying-emoji');
        el.innerText = emojis[Math.floor(Math.random() * emojis.length)];
        el.style.left = Math.random() * 80 + "%";
        el.style.animationDuration = (Math.random() * 1 + 1) + "s"; // Random speed
        stream.appendChild(el);

        // Cleanup
        setTimeout(() => el.remove(), 2000);
    }
});