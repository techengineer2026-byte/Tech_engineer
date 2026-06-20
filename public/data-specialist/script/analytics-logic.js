document.addEventListener("DOMContentLoaded", function () {
    AOS.init({ duration: 800 });

    const btnClean = document.getElementById('btnClean');
    const overlay = document.getElementById('cleanOverlay');
    const cleanTable = document.getElementById('cleanTable');
    const insightBox = document.getElementById('insightBox');

    btnClean.addEventListener('click', () => {
        if (btnClean.innerText === "Cleaned!") return;

        // 1. Animation State
        btnClean.innerHTML = '<i class="fas fa-cog fa-spin"></i> Processing...';

        setTimeout(() => {
            // 2. Reveal Clean Data
            overlay.style.opacity = '0';
            setTimeout(() => overlay.classList.add('d-none'), 500); // Remove after fade

            cleanTable.classList.remove('d-none');
            cleanTable.classList.add('fade-in'); // Add CSS animation class

            // 3. Show Insight
            insightBox.classList.remove('d-none');

            // 4. Update Button
            btnClean.innerHTML = 'Cleaned!';
            btnClean.classList.remove('btn-mint');
            btnClean.classList.add('btn-success');
        }, 1000);
    });
});