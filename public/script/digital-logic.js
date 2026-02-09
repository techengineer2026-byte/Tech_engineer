document.addEventListener("DOMContentLoaded", function () {
    AOS.init({ duration: 800 });

    const slider = document.getElementById('budgetSlider');
    const budgetVal = document.getElementById('budgetValue');
    const reachNum = document.getElementById('reachNum');
    const clickNum = document.getElementById('clickNum');
    const bars = document.querySelectorAll('.graph-bar');

    let currentPlatform = 'ig'; // 'ig' or 'google'

    window.setPlatform = function(platform) {
        currentPlatform = platform;
        const btns = document.querySelectorAll('.p-btn');
        btns.forEach(b => b.classList.remove('active'));
        event.currentTarget.classList.add('active');
        updateStats(); // Recalculate based on platform
    }

    slider.addEventListener('input', () => {
        budgetVal.innerText = `₹${parseInt(slider.value).toLocaleString()}`;
        updateStats();
    });

    function updateStats() {
        const budget = parseInt(slider.value);
        let multiplier = currentPlatform === 'ig' ? 12 : 8; // IG reaches more people cheaply, Google is pricier but targeted
        let clickRate = currentPlatform === 'ig' ? 0.02 : 0.05; // Google has higher CTR

        const reach = Math.floor(budget * multiplier);
        const clicks = Math.floor(reach * clickRate);

        // Animate Numbers
        reachNum.innerText = reach.toLocaleString();
        clickNum.innerText = clicks.toLocaleString();

        // Update Graph Bars visually based on budget
        bars.forEach((bar) => {
            // Randomize slightly for "live" feel
            const height = Math.min(100, (budget / 100) + Math.random() * 20); 
            bar.style.height = `${height}%`;
        });
    }

    // Init
    updateStats();
});