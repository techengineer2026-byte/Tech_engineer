document.addEventListener("DOMContentLoaded", function () {
    AOS.init({ duration: 800 });

    const btnAnalyze = document.getElementById('btnAnalyze');
    const resultsPanel = document.getElementById('auditResults');
    const logPanel = document.getElementById('auditLog');
    const scoreNum = document.getElementById('finalScore');
    const scoreRing = document.getElementById('scoreRing');

    btnAnalyze.addEventListener('click', () => {
        // Reset
        resultsPanel.style.display = 'block';
        logPanel.innerHTML = '<div class="text-gray">> Starting Crawler...</div>';
        scoreRing.style.strokeDashoffset = 440;
        scoreNum.innerText = 0;
        btnAnalyze.innerText = "Running...";
        btnAnalyze.disabled = true;

        const tasks = [
            { msg: "Checking robots.txt...", time: 500, status: "success", text: "Found" },
            { msg: "Analyzing Page Speed...", time: 1200, status: "warning", text: "1.2s (Good)" },
            { msg: "Scanning Keywords...", time: 2000, status: "success", text: "Optimized" },
            { msg: "Checking Mobile View...", time: 2800, status: "success", text: "Responsive" },
            { msg: "Analyzing Backlinks...", time: 3500, status: "danger", text: "Low Authority" },
            { msg: "Finalizing Report...", time: 4200, status: "info", text: "Done" }
        ];

        let i = 0;
        function runTask() {
            if (i < tasks.length) {
                setTimeout(() => {
                    const t = tasks[i];
                    let color = t.status === "success" ? "text-green" : t.status === "danger" ? "text-danger" : "text-warning";

                    logPanel.innerHTML += `
                        <div class="log-item text-white fade-in">
                            <span class="text-gray">> ${t.msg}</span> 
                            <span class="${color} fw-bold float-end">${t.text}</span>
                        </div>`;

                    // Auto scroll
                    logPanel.scrollTop = logPanel.scrollHeight;

                    i++;
                    runTask();
                }, tasks[i].time - (i > 0 ? tasks[i - 1].time : 0));
            } else {
                // Final Score Animation
                setTimeout(() => {
                    const finalScore = 87;
                    const offset = 440 - (440 * finalScore) / 100;
                    scoreRing.style.strokeDashoffset = offset;

                    let currentScore = 0;
                    const scoreInterval = setInterval(() => {
                        scoreNum.innerText = currentScore;
                        if (currentScore >= finalScore) clearInterval(scoreInterval);
                        currentScore++;
                    }, 20);

                    btnAnalyze.innerText = "ANALYZE AGAIN";
                    btnAnalyze.disabled = false;
                }, 500);
            }
        }

        runTask();
    });
});