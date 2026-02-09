document.addEventListener("DOMContentLoaded", function () {
    AOS.init({ duration: 800 });

    const btnHack = document.getElementById('btnHack');
    const terminal = document.getElementById('terminalBody');
    const statusBox = document.querySelector('.status-indicator');
    const statusDot = document.querySelector('.status-dot');

    btnHack.addEventListener('click', () => {
        if(btnHack.innerText === "Running...") return;

        // Reset
        terminal.innerHTML = `
            <div class="input-line">
                <span class="prompt">root@kali:~$</span> 
                <span class="typing">nmap -sV -A 10.0.0.5</span>
            </div>`;
        btnHack.innerText = "Running...";
        btnHack.disabled = true;
        statusBox.innerHTML = '<span class="status-dot"></span> SYSTEM SCANNING...';
        statusBox.classList.add('scanning');

        const logs = [
            { msg: "Starting Nmap 7.92...", delay: 500, type: "log-info" },
            { msg: "Scanning 10.0.0.5 [1000 ports]...", delay: 1200, type: "log-info" },
            { msg: "Discovered Open Port 80/tcp (HTTP)", delay: 2000, type: "log-success" },
            { msg: "Discovered Open Port 22/tcp (SSH)", delay: 2500, type: "log-success" },
            { msg: "Scanning for vulnerabilities...", delay: 3500, type: "log-info" },
            { msg: "[!] VULNERABILITY FOUND: SQL Injection (CVE-2023-45)", delay: 4500, type: "log-warn" },
            { msg: "Generating Report...", delay: 5500, type: "log-info" },
            { msg: "Scan Complete. 1 Threat Detected.", delay: 6000, type: "text-white" }
        ];

        logs.forEach(log => {
            setTimeout(() => {
                terminal.innerHTML += `<div class="${log.type}">> ${log.msg}</div>`;
                terminal.scrollTop = terminal.scrollHeight;
            }, log.delay);
        });

        setTimeout(() => {
            btnHack.innerText = "PATCH SYSTEM";
            btnHack.classList.remove('btn-cyber');
            btnHack.classList.add('btn-outline-danger');
            btnHack.disabled = false;
            statusBox.innerHTML = '<span class="status-dot"></span> SCAN FINISHED';
            statusBox.classList.remove('scanning');
            
            // Handle Patch Click
            btnHack.onclick = function() {
                terminal.innerHTML += `<div class="log-info">> Applying Security Patch...</div>`;
                setTimeout(() => {
                    terminal.innerHTML += `<div class="log-success">> SYSTEM SECURED.</div>`;
                    terminal.scrollTop = terminal.scrollHeight;
                    btnHack.innerText = "SECURED ✔";
                    btnHack.classList.remove('btn-outline-danger');
                    btnHack.classList.add('btn-success');
                }, 1500);
            };

        }, 6500);
    });
});