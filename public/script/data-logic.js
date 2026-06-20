document.addEventListener("DOMContentLoaded", function () {
    AOS.init({ duration: 800 });

    const btn = document.getElementById('btnProcess');
    const rawView = document.getElementById('rawData');
    const chartView = document.getElementById('visualData');
    const bars = document.querySelectorAll('.chart-bar');

    btn.addEventListener('click', () => {
        // 1. Loading
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
        
        // 2. Hide Table, Show Charts
        setTimeout(() => {
            rawView.style.display = 'none';
            chartView.classList.remove('d-none');
            
            // Animate Bars
            const heights = ['40%', '70%', '50%', '90%', '65%'];
            bars.forEach((bar, index) => {
                setTimeout(() => {
                    bar.style.height = heights[index];
                }, index * 100);
            });

            btn.innerHTML = '<i class="fas fa-check"></i> Analysis Complete';
            btn.classList.remove('btn-outline-cyan');
            btn.classList.add('btn-success');
        }, 1000);
    });
});