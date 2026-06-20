document.addEventListener("DOMContentLoaded", function () {
    
    const input = document.getElementById('aiInput');
    const predictBtn = document.getElementById('predictBtn');
    const posBar = document.getElementById('posBar');
    const negBar = document.getElementById('negBar');
    const posScore = document.getElementById('posScore');
    const negScore = document.getElementById('negScore');
    const verdict = document.getElementById('aiVerdict');
    const headerText = document.querySelector('.console-header');

    // Simple keyword dictionary for simulation
    const positiveWords = ['amazing', 'good', 'great', 'love', 'best', 'excellent', 'happy', 'cool', 'fast', 'awesome'];
    const negativeWords = ['hate', 'bad', 'terrible', 'slow', 'worst', 'sad', 'angry', 'buggy', 'broken', 'error'];

    predictBtn.addEventListener('click', () => {
        const text = input.value.toLowerCase();
        
        // 1. Loading State
        predictBtn.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> Processing...';
        headerText.innerHTML = '<span class="text-warning">●</span> Analyzing Tensors...';
        verdict.innerText = "COMPUTING...";
        verdict.style.color = "white";

        // 2. Simulate Algorithm Delay
        setTimeout(() => {
            let posCount = 0;
            let negCount = 0;

            // Simple Logic: Count word matches
            positiveWords.forEach(w => { if(text.includes(w)) posCount++; });
            negativeWords.forEach(w => { if(text.includes(w)) negCount++; });

            // Calculate "Probability"
            let total = posCount + negCount;
            let posPct = 50; // Default neutral
            let negPct = 50;

            if (total > 0) {
                posPct = Math.round((posCount / total) * 100);
                negPct = 100 - posPct;
            } else if (text.length > 0) {
                // Random drift for unknown text to look real
                posPct = 40 + Math.floor(Math.random() * 20);
                negPct = 100 - posPct;
            } else {
                posPct = 0; negPct = 0;
            }

            // 3. Animate Bars
            posBar.style.width = posPct + "%";
            negBar.style.width = negPct + "%";
            
            // 4. Update Numbers
            animateValue(posScore, 0, posPct, 500);
            animateValue(negScore, 0, negPct, 500);

            // 5. Final Verdict
            if (posPct > 60) {
                verdict.innerText = "POSITIVE SENTIMENT";
                verdict.style.color = "#198754"; // Green
            } else if (negPct > 60) {
                verdict.innerText = "NEGATIVE SENTIMENT";
                verdict.style.color = "#dc3545"; // Red
            } else {
                verdict.innerText = "NEUTRAL / UNCERTAIN";
                verdict.style.color = "#ffc107"; // Yellow
            }

            // Reset Button
            predictBtn.innerHTML = 'Run Prediction <i class="fas fa-bolt ms-2"></i>';
            headerText.innerHTML = '<span class="text-success">●</span> Prediction Complete.';

        }, 1200);
    });

    // Helper to animate numbers count up
    function animateValue(obj, start, end, duration) {
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            obj.innerHTML = Math.floor(progress * (end - start) + start) + "%";
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        window.requestAnimationFrame(step);
    }
});