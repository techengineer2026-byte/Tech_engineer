document.addEventListener("DOMContentLoaded", function () {
    
    const btnLow = document.getElementById('btnTrafficLow');
    const btnHigh = document.getElementById('btnTrafficHigh');
    const trafficFlow = document.getElementById('traffic-flow');
    const nodeContainer = document.getElementById('node-container');
    const statusText = document.getElementById('traffic-status');

    let packetInterval;
    let isHighLoad = false;

    // Function to create moving dots (packets)
    function createPacket() {
        const packet = document.createElement('div');
        packet.classList.add('packet');
        if (isHighLoad) packet.classList.add('fast');
        trafficFlow.appendChild(packet);

        // Remove after animation
        setTimeout(() => {
            packet.remove();
        }, isHighLoad ? 200 : 1000);
    }

    // Function to manage server nodes
    function updateNodes() {
        // Clear existing extra nodes (keep first one)
        const firstNode = nodeContainer.firstElementChild;
        nodeContainer.innerHTML = '';
        nodeContainer.appendChild(firstNode);

        if (isHighLoad) {
            // Add 2 more nodes
            addNode("Instance 2 (Auto-Scaled)");
            setTimeout(() => addNode("Instance 3 (Auto-Scaled)"), 400);
            
            // Max out CPU on first node
            firstNode.querySelector('.fill').style.width = '90%';
            firstNode.querySelector('.fill').style.backgroundColor = '#ef4444'; // Red
        } else {
            // Normal CPU
            firstNode.querySelector('.fill').style.width = '20%';
            firstNode.querySelector('.fill').style.backgroundColor = '#22d3ee'; // Cyan
        }
    }

    function addNode(name) {
        const node = document.createElement('div');
        node.className = 'server-node active';
        node.innerHTML = `
            <i class="fab fa-docker"></i>
            <small>${name}</small>
            <div class="cpu-bar"><div class="fill" style="width: 40%; background-color: #fbbf24"></div></div>
        `;
        nodeContainer.appendChild(node);
    }

    // Button Logic
    btnLow.addEventListener('click', () => {
        isHighLoad = false;
        btnLow.classList.add('active');
        btnHigh.classList.remove('active');
        statusText.innerText = "Traffic: Normal";
        statusText.className = "text-success";
        
        clearInterval(packetInterval);
        packetInterval = setInterval(createPacket, 800); // Slow packets
        updateNodes();
    });

    btnHigh.addEventListener('click', () => {
        isHighLoad = true;
        btnHigh.classList.add('active');
        btnLow.classList.remove('active');
        statusText.innerText = "Traffic: CRITICAL (Scaling Up...)";
        statusText.className = "text-danger blink";
        
        clearInterval(packetInterval);
        packetInterval = setInterval(createPacket, 100); // Fast packets
        updateNodes();
    });

    // Start Normal
    packetInterval = setInterval(createPacket, 800);

});