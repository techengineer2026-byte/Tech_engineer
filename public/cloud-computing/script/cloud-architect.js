document.addEventListener("DOMContentLoaded", function () {
    AOS.init({ duration: 800 });

    const btn = document.getElementById('launchBtn');
    const logs = document.getElementById('consoleLogs');
    const visual = document.getElementById('serverVisual');
    const osSelect = document.getElementById('osSelect');
    const nameLabel = document.getElementById('serverName');

    btn.addEventListener('click', () => {
        if(btn.innerText === "Launching...") return;

        // Reset
        btn.innerText = "Launching...";
        btn.classList.add('disabled');
        visual.classList.add('d-none');
        logs.innerHTML = "";

        const osName = osSelect.options[osSelect.selectedIndex].text;

        // Sequence
        addLog(`> Initiating Launch Sequence...`);
        addLog(`> Selecting Image: ${osName}`);

        setTimeout(() => addLog(`> Provisioning Storage (EBS)...`), 1000);
        setTimeout(() => addLog(`> Configuring Security Group (Firewall)...`), 2000);
        setTimeout(() => {
            addLog(`> Booting OS...`);
            addLog(`> Assigning Public IP: 54.211.34.12`);
        }, 3000);

        setTimeout(() => {
            addLog(`> <span style="color:#0ea5e9">INSTANCE STATE: RUNNING</span>`);
            btn.innerText = "Launch Instance";
            btn.classList.remove('disabled');
            
            // Show Visual
            nameLabel.innerText = osName + " - 01";
            visual.classList.remove('d-none');
            visual.classList.add('fade-in');
        }, 4500);
    });

    function addLog(msg) {
        logs.innerHTML += `<div>${msg}</div>`;
        logs.scrollTop = logs.scrollHeight;
    }
});