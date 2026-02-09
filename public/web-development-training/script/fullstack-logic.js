document.addEventListener("DOMContentLoaded", function () {
    AOS.init({ duration: 800 });

    const btn = document.getElementById('btnFetch');
    const packet = document.getElementById('dataPacket');
    const log = document.getElementById('statusLog');
    const nodes = {
        client: document.getElementById('nodeClient'),
        server: document.getElementById('nodeServer'),
        db: document.getElementById('nodeDB')
    };

    btn.addEventListener('click', () => {
        btn.disabled = true;
        log.innerText = "> Request sent from Client...";
        nodes.client.classList.add('active');
        packet.style.opacity = '1';
        packet.style.left = '40px'; // Start

        // 1. Client -> Server
        packet.style.transition = 'left 1s linear';
        setTimeout(() => { packet.style.left = '50%'; }, 50);

        setTimeout(() => {
            nodes.server.classList.add('active');
            log.innerText = "> Server processing Logic (Node.js)...";
        }, 1000);

        // 2. Server -> DB
        setTimeout(() => {
            packet.style.left = '90%';
            log.innerText = "> Querying Database...";
        }, 2000);

        setTimeout(() => {
            nodes.db.classList.add('active');
            packet.style.backgroundColor = '#00ff41'; // Turn Green (Data found)
            log.innerHTML = "> Data Found! Returning...";
        }, 3000);

        // 3. DB -> Server -> Client (Return Trip)
        setTimeout(() => {
            packet.style.left = '50%';
            nodes.db.classList.remove('active');
        }, 4000);

        setTimeout(() => {
            packet.style.left = '40px';
            nodes.server.classList.remove('active');
            log.innerText = "> Response Received! Rendering UI...";
        }, 5000);

        setTimeout(() => {
            nodes.client.classList.remove('active');
            packet.style.opacity = '0';
            packet.style.backgroundColor = '#FFD700'; // Reset color
            btn.disabled = false;
            log.innerText = "> Cycle Complete.";
        }, 6000);
    });
});