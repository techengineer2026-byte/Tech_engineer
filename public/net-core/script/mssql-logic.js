document.addEventListener("DOMContentLoaded", function () {
    
    const toggle = document.getElementById('indexToggle');
    const bar = document.getElementById('queryProgressBar');
    const timer = document.getElementById('timerDisplay');

    // Function to run the simulation
    function runSimulation() {
        // Reset
        bar.style.width = '0%';
        bar.textContent = '';
        timer.textContent = 'Running Query...';
        
        // Check if Index is On or Off
        if(toggle.checked) {
            // --- FAST MODE (Indexed) ---
            bar.className = 'progress-bar bg-success'; // Green
            
            // Fast Animation (0.5s)
            setTimeout(() => {
                bar.style.transition = 'width 0.3s ease-out';
                bar.style.width = '100%';
            }, 100);

            setTimeout(() => {
                bar.textContent = 'Done!';
                timer.innerHTML = '<span class="text-gold">0.02 Seconds</span> (Indexed)';
            }, 400);

        } else {
            // --- SLOW MODE (Table Scan) ---
            bar.className = 'progress-bar bg-danger'; // Red
            
            // Slow Animation (2.5s)
            setTimeout(() => {
                bar.style.transition = 'width 2.5s linear';
                bar.style.width = '100%';
            }, 100);

            setTimeout(() => {
                bar.textContent = 'Scanning...';
            }, 1000);

            setTimeout(() => {
                bar.textContent = 'Done!';
                timer.innerHTML = '<span class="text-danger">5.00 Seconds</span> (Table Scan)';
            }, 2600);
        }
    }

    // Run when toggle changes
    toggle.addEventListener('change', runSimulation);

    // Run once on load
    runSimulation();
});