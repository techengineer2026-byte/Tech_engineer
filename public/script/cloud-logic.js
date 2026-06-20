document.addEventListener("DOMContentLoaded", function () {
    AOS.init({ duration: 800 });

    const terminal = document.getElementById('cloudTerminal');

    window.toggleServer = function(id, btn) {
        const statusSpan = document.getElementById(`status${id}`);
        
        if (btn.innerText === "Launch") {
            // Start Sequence
            btn.disabled = true;
            btn.innerText = "Booting...";
            
            terminal.innerHTML += `<br>> Initializing Instance ${id}...`;
            
            setTimeout(() => {
                terminal.innerHTML += `<br>> Allocating IP Address...`;
            }, 800);

            setTimeout(() => {
                terminal.innerHTML += `<br>> <span style="color:#0ea5e9">Instance ${id} is RUNNING.</span>`;
                statusSpan.innerText = "Running";
                statusSpan.className = "text-success";
                btn.innerText = "Stop";
                btn.className = "btn btn-sm btn-outline-danger";
                btn.disabled = false;
                terminal.scrollTop = terminal.scrollHeight;
            }, 2000);

        } else {
            // Stop Sequence
            btn.disabled = true;
            btn.innerText = "Stopping...";
            terminal.innerHTML += `<br>> Terminating Instance ${id}...`;
            
            setTimeout(() => {
                statusSpan.innerText = "Stopped";
                statusSpan.className = "text-danger";
                btn.innerText = "Launch";
                btn.className = "btn btn-sm btn-outline-success";
                btn.disabled = false;
                terminal.scrollTop = terminal.scrollHeight;
            }, 1500);
        }
    }
});