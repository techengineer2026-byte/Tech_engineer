document.addEventListener("DOMContentLoaded", function () {
    AOS.init({ duration: 800 });

    const btnDeploy = document.getElementById('btnDeploy');
    const logs = document.getElementById('buildLogs');
    const stages = [
        document.getElementById('stage1'),
        document.getElementById('stage2'),
        document.getElementById('stage3'),
        document.getElementById('stage4')
    ];
    const connectors = document.querySelectorAll('.connector');

    btnDeploy.addEventListener('click', () => {
        if (btnDeploy.innerText === "Deploying...") return;

        // Reset
        resetPipeline();
        btnDeploy.innerText = "Deploying...";
        btnDeploy.classList.add('disabled');

        // Start Sequence
        addLog("> git commit -m 'Fixed bug'");
        addLog("> git push origin main");
        activateStage(0);

        setTimeout(() => {
            addLog("> Jenkins: Build Triggered...");
            completeStage(0);
            fillConnector(0);
            activateStage(1);
        }, 1500);

        setTimeout(() => {
            addLog("> Docker: Building Image...");
            completeStage(1);
            fillConnector(1);
            activateStage(2);
        }, 3000);

        setTimeout(() => {
            addLog("> Running Tests... (PASS)");
            completeStage(2);
            fillConnector(2);
            activateStage(3);
        }, 4500);

        setTimeout(() => {
            addLog("> Kubernetes: Deploying to Pods...");
            completeStage(3);
            addLog("> <span style='color:#22c55e'>DEPLOYMENT SUCCESSFUL</span>");
            btnDeploy.innerText = "Deployed ✔";
            btnDeploy.classList.remove('btn-magma');
            btnDeploy.classList.add('btn-success');
        }, 6000);
    });

    function addLog(msg) {
        logs.innerHTML += msg + "<br>";
        logs.scrollTop = logs.scrollHeight;
    }

    function activateStage(index) {
        stages[index].classList.add('active');
        addLog(`> Starting Stage: ${stages[index].querySelector('small').innerText}...`);
    }

    function completeStage(index) {
        stages[index].classList.remove('active');
        stages[index].classList.add('success');
    }

    function fillConnector(index) {
        if (connectors[index]) connectors[index].classList.add('filled');
    }

    function resetPipeline() {
        logs.innerHTML = "";
        stages.forEach(s => {
            s.classList.remove('active', 'success');
        });
        connectors.forEach(c => c.classList.remove('filled'));
        btnDeploy.classList.remove('btn-success', 'disabled');
        btnDeploy.classList.add('btn-magma');
    }
});