document.addEventListener("DOMContentLoaded", function () {
    
    const sendBtn = document.getElementById('sendBtn');
    const jsonOutput = document.getElementById('jsonOutput');
    const statusBadge = document.getElementById('statusBadge');
    const httpMethod = document.getElementById('httpMethod');

    // MOCK DATA
    const responses = {
        GET: `{
  <span class="j-key">"status"</span>: <span class="j-string">"success"</span>,
  <span class="j-key">"data"</span>: [
    { <span class="j-key">"id"</span>: <span class="j-num">1</span>, <span class="j-key">"name"</span>: <span class="j-string">"iPhone 15"</span>, <span class="j-key">"price"</span>: <span class="j-num">999</span> },
    { <span class="j-key">"id"</span>: <span class="j-num">2</span>, <span class="j-key">"name"</span>: <span class="j-string">"MacBook Pro"</span>, <span class="j-key">"price"</span>: <span class="j-num">1999</span> }
  ]
}`,
        POST: `{
  <span class="j-key">"status"</span>: <span class="j-string">"created"</span>,
  <span class="j-key">"message"</span>: <span class="j-string">"Product added successfully"</span>,
  <span class="j-key">"productId"</span>: <span class="j-num">105</span>
}`,
        DELETE: `{
  <span class="j-key">"status"</span>: <span class="j-string">"deleted"</span>,
  <span class="j-key">"id"</span>: <span class="j-num">1</span>
}`
    };

    sendBtn.addEventListener('click', () => {
        // 1. Loading State
        sendBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        jsonOutput.innerHTML = '<span class="text-muted">Sending request to server...</span>';
        statusBadge.className = 'badge bg-secondary';
        statusBadge.textContent = 'Sending...';

        // 2. Simulate Delay (Network Latency)
        setTimeout(() => {
            const method = httpMethod.value;
            
            // 3. Update Status
            let statusColor = 'bg-success';
            let statusText = '200 OK';
            
            if(method === 'POST') { statusText = '201 Created'; }
            if(method === 'DELETE') { statusText = '204 No Content'; }

            statusBadge.className = `badge ${statusColor}`;
            statusBadge.textContent = statusText;

            // 4. Show Result
            jsonOutput.innerHTML = responses[method];
            
            // Reset Button
            sendBtn.innerHTML = 'SEND';
        }, 800);
    });

});